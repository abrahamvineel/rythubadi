from domain.market_listing import MarketListing
from typing import Optional, Iterator
from uuid import UUID
from contextlib import contextmanager
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor
from market_listing_mapper import domain_to_row

class PostgresMarketListingRepository:
    
    def __init__(self, pool: ThreadedConnectionPool):
        self.pool = pool

    def save(self, listing: MarketListing) -> None:
        conn = self.pool.getconn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("INSERT INTO market_listing VALUES()")
            conn.commit()
        except Exception:
            conn.rollback()
        finally:
            self.pool.putconn(conn)

    def find_by_id(self, listing_id: UUID) -> Optional[MarketListing]:
        pass

    def find_by_producer_id(self, producer_id: UUID) -> list[MarketListing]:
        pass
    
    def find_active(self, page: int, page_size: int) -> list[MarketListing]:
        pass
    
    def find_all_active(self) -> list[MarketListing]:
        pass

    def deactivate(self, listing_id: UUID) -> None:
        pass

    @contextmanager
    def transaction(self) -> Iterator[None]:
        try:
            yield 
            #commit
        except:
            #rollback
            raise
