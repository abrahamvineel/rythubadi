from domain.market_listing import MarketListing
from typing import Optional, Iterator
from uuid import UUID
from contextlib import contextmanager
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor
from infrastructure.market_listing_mapper import domain_to_row, row_to_domain
import structlog 
from  datetime import datetime

logger = structlog.get_logger()

class PostgresMarketListingRepository:
    
    def __init__(self, pool: ThreadedConnectionPool):
        self.pool = pool

    def save(self, listing: MarketListing) -> None:
        conn = self.pool.getconn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                row = domain_to_row(listing)
                cur.execute("INSERT INTO market_listing (listing_id, listing_mode, price, product_category, perishability_level, producer_id, is_active, photo_url)" \
                " VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (row["listing_id"], row["listing_mode"], row["price"], row["product_category"], row["perishability_level"], row["producer_id"], row["is_active"], row["photo_url"]))
            conn.commit()
            logger.info("Market listing added", listing_id=str(listing.listing_id))
        except Exception:
            logger.exception("save_failed", listing_id=str(listing.listing_id))
            conn.rollback()
        finally:
            self.pool.putconn(conn)

    def find_by_id(self, listing_id: UUID) -> Optional[MarketListing]:
        conn = self.pool.getconn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT listing_id, listing_mode, price, product_category, perishability_level, created_at, producer_id, is_active, photo_url" \
                " FROM market_listing WHERE listing_id = %s", (listing_id,))
                res = cur.fetchone()
                if res is None:
                    return None
                return row_to_domain(res)
        except Exception:
            logger.exception("find_by_id failed", listing_id=str(listing_id))
            conn.rollback()
        finally:
            self.pool.putconn(conn)

    def find_by_producer_id(self, producer_id: UUID) -> list[MarketListing]:
        conn = self.pool.getconn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT listing_id, listing_mode, price, product_category, perishability_level, created_at, producer_id, is_active, photo_url" \
                " FROM market_listing WHERE producer_id = %s", (producer_id,))
                res = cur.fetchall()
                return [row_to_domain(row) for row in res]
        except Exception:
            logger.exception("find_by_producer_id failed", producer_id=str(producer_id))
            conn.rollback()
        finally:
            self.pool.putconn(conn)
    
    def find_active(self, limit: int, created_at: Optional[datetime], listing_id: Optional[UUID]) -> list[MarketListing]:
        conn = self.pool.getconn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                if created_at is None:
                    cur.execute("SELECT listing_id, listing_mode, price, product_category, perishability_level, created_at, producer_id, is_active, photo_url" \
                    " FROM market_listing WHERE is_active = true " \
                    "ORDER BY created_at DESC, listing_id DESC LIMIT %s", (limit, ))
                else:
                    cur.execute("SELECT listing_id, listing_mode, price, product_category, perishability_level, created_at, producer_id, is_active, photo_url" \
                    " FROM market_listing WHERE is_active = true AND (created_at < %s OR (created_at = %s AND listing_id < %s))" \
                    "ORDER BY created_at DESC, listing_id DESC LIMIT %s", (created_at, created_at, listing_id, limit))                    
                res = cur.fetchall()
                return [row_to_domain(row) for row in res]
        except Exception:
            logger.exception("find_active failed")
            conn.rollback()
        finally:
            self.pool.putconn(conn)

    def find_all_active(self) -> list[MarketListing]:
        conn = self.pool.getconn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT listing_id, listing_mode, price, product_category, perishability_level, created_at, producer_id, is_active, photo_url" \
                " FROM market_listing WHERE is_active = true ")
                res = cur.fetchall()
                return [row_to_domain(row) for row in res]
        except Exception:
            logger.exception("find_all_active failed")
            conn.rollback()
        finally:
            self.pool.putconn(conn)
    
    def deactivate(self, listing_id: UUID) -> None:
        conn = self.pool.getconn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute('UPDATE market_listing SET is_active = false WHERE listing_id = %s', (listing_id,))
            conn.commit()
        except Exception:
            logger.exception("deactivate failed", listing_id=str(listing_id))
            conn.rollback()
        finally:
            self.pool.putconn(conn)

    @contextmanager
    def transaction(self) -> Iterator[None]:
        conn = self.pool.getconn()
        try:
            yield 
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            self.pool.putconn(conn)
