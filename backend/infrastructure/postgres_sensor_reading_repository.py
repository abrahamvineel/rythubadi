from domain.sensor_reading import SensorReading
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor
from uuid import UUID, uuid4
import structlog

logger = structlog.get_logger()

class PostgresSensorReadingRepository:

    def __init__(self, pool: ThreadedConnectionPool):
        self._pool = pool

    def save(self, reading: SensorReading) -> None:
        conn = None
        try:
            conn = self._pool.getconn()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                reading_id = uuid4()
                cur.execute(
                    "INSERT INTO sensor_reading "
                    "(id, producer_id, producer_type, crop_type, province_state, data_precision, recorded_at) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (
                        str(reading_id),
                        str(reading.producer_id),
                        reading.producer_type.value,
                        reading.crop_type,
                        reading.province_state,
                        reading.data_precision.value,
                        reading.recorded_at,
                    )
                )
                for measurement in reading.measurements:
                    cur.execute(
                        "INSERT INTO sensor_measurement (id, reading_id, sensor_type, value, unit) "
                        "VALUES (%s, %s, %s, %s, %s)",
                        (
                            str(uuid4()),
                            str(reading_id),
                            measurement.sensor_type.value,
                            measurement.value,
                            measurement.unit,
                        )
                    )
            conn.commit()
            logger.info("sensor_reading_saved", producer_id=str(reading.producer_id))
        except Exception:
            if conn:
                conn.rollback()
            logger.exception("sensor_reading_save_failed", producer_id=str(reading.producer_id))
            raise
        finally:
            if conn:
                self._pool.putconn(conn)

    def find_recent(self, producer_id: UUID, limit: int) -> list[SensorReading]:
        return []

    def was_notified_recently(self, producer_id: UUID, topic: str, hours: int) -> bool:
        conn = None
        try:
            conn = self._pool.getconn()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT 1 FROM crop_notification "
                    "WHERE producer_id = %s AND topic = %s "
                    "AND sent_at > NOW() - (%s * INTERVAL '1 hour') "
                    "LIMIT 1",
                    (str(producer_id), topic, hours)
                )
                return cur.fetchone() is not None
        except Exception:
            logger.exception("was_notified_recently_failed", producer_id=str(producer_id))
            return False
        finally:
            if conn:
                self._pool.putconn(conn)