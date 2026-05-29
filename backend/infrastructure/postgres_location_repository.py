from uuid import UUID
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor
from domain.farm_location import FarmLocation
from domain.producer_type import ProducerType
from domain.exceptions import UnauthorisedOperationError


class PostgresLocationRepository:

    def __init__(self, pool: ThreadedConnectionPool):
        self.pool = pool

    def find_by_producer(self, producer_id: UUID) -> list[FarmLocation]:
        conn = self.pool.getconn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT * FROM farm_location WHERE producer_id = %s ORDER BY created_at ASC",
                    (str(producer_id),),
                )
                rows = cur.fetchall()
            return [
                FarmLocation(
                    id=UUID(row["id"]),
                    producer_id=UUID(row["producer_id"]),
                    name=row["name"],
                    latitude=float(row["latitude"]),
                    longitude=float(row["longitude"]),
                    producer_types=frozenset(ProducerType[t] for t in row["producer_types"]),
                )
                for row in rows
            ]
        finally:
            self.pool.putconn(conn)

    def save(self, location: FarmLocation) -> None:
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cur:
                type_names = [t.name for t in location.producer_types]
                cur.execute(
                    """
                    INSERT INTO farm_location (id, producer_id, name, latitude, longitude, producer_types)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (str(location.id), str(location.producer_id), location.name,
                     location.latitude, location.longitude, type_names),
                )
            conn.commit()
        finally:
            self.pool.putconn(conn)

    def delete(self, location_id: UUID, producer_id: UUID) -> None:
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cur:
                # Ownership enforced at query level — wrong producer_id simply matches 0 rows
                cur.execute(
                    "DELETE FROM farm_location WHERE id = %s AND producer_id = %s",
                    (str(location_id), str(producer_id)),
                )
                if cur.rowcount == 0:
                    raise UnauthorisedOperationError("Location not found or access denied")
            conn.commit()
        finally:
            self.pool.putconn(conn)
