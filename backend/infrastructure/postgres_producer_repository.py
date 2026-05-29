from uuid import UUID
from typing import Optional
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor
from domain.producer_profile import ProducerProfile
from domain.producer_type import ProducerType


class PostgresProducerRepository:

    def __init__(self, pool: ThreadedConnectionPool):
        self.pool = pool

    def save(self, profile: ProducerProfile) -> None:
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cur:
                type_names = [t.name for t in profile.producer_types]
                cur.execute(
                    """
                    INSERT INTO producer_profile (producer_id, name, producer_types)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (producer_id) DO UPDATE
                        SET name = EXCLUDED.name,
                            producer_types = EXCLUDED.producer_types,
                            updated_at = NOW()
                    """,
                    (str(profile.producer_id), profile.name, type_names),
                )
            conn.commit()
        finally:
            self.pool.putconn(conn)

    def find_by_id(self, producer_id: UUID) -> Optional[ProducerProfile]:
        conn = self.pool.getconn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT * FROM producer_profile WHERE producer_id = %s",
                    (str(producer_id),),
                )
                row = cur.fetchone()
            if row is None:
                return None
            return ProducerProfile(
                producer_id=UUID(row["producer_id"]),
                producer_types=frozenset(ProducerType[t] for t in row["producer_types"]),
                name=row["name"],
            )
        finally:
            self.pool.putconn(conn)

    def add_types(self, producer_id: UUID, new_types: frozenset[ProducerType]) -> ProducerProfile:
        conn = self.pool.getconn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                new_type_names = [t.name for t in new_types]
                cur.execute(
                    """
                    UPDATE producer_profile
                    SET producer_types = (
                        SELECT array_agg(DISTINCT elem)
                        FROM unnest(producer_types || %s::text[]) AS elem
                    ),
                    updated_at = NOW()
                    WHERE producer_id = %s
                    RETURNING *
                    """,
                    (new_type_names, str(producer_id)),
                )
                row = cur.fetchone()
            conn.commit()
            return ProducerProfile(
                producer_id=UUID(row["producer_id"]),
                producer_types=frozenset(ProducerType[t] for t in row["producer_types"]),
                name=row["name"],
            )
        finally:
            self.pool.putconn(conn)
