from uuid import UUID
from datetime import datetime
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor
from domain.feed_event import FeedEvent


class PostgresFeedEventRepository:

    def __init__(self, pool: ThreadedConnectionPool):
        self.pool = pool

    def find_by_producer(self, producer_id: UUID, limit: int = 50) -> list[FeedEvent]:
        conn = self.pool.getconn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT * FROM feed_event
                    WHERE producer_id = %s
                    ORDER BY created_at DESC
                    LIMIT %s
                    """,
                    (str(producer_id), limit),
                )
                rows = cur.fetchall()
            return [self._to_domain(row) for row in rows]
        finally:
            self.pool.putconn(conn)

    def save(self, event: FeedEvent) -> None:
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO feed_event
                        (id, producer_id, severity, agent, agent_emoji,
                         title, body, subject_type, subject_id, subject_name,
                         location_id, reply_count)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        str(event.id),
                        str(event.producer_id),
                        event.severity,
                        event.agent,
                        event.agent_emoji,
                        event.title,
                        event.body,
                        event.subject_type,
                        event.subject_id,
                        event.subject_name,
                        str(event.location_id) if event.location_id else None,
                        event.reply_count,
                    ),
                )
            conn.commit()
        finally:
            self.pool.putconn(conn)

    def _to_domain(self, row: dict) -> FeedEvent:
        return FeedEvent(
            id=UUID(str(row["id"])),
            producer_id=UUID(str(row["producer_id"])),
            severity=row["severity"],
            agent=row["agent"],
            agent_emoji=row["agent_emoji"],
            title=row["title"],
            body=row["body"],
            subject_type=row["subject_type"],
            subject_id=row["subject_id"],
            subject_name=row["subject_name"],
            location_id=UUID(str(row["location_id"])) if row["location_id"] else None,
            reply_count=row["reply_count"],
            created_at=row["created_at"] if isinstance(row["created_at"], datetime)
                       else datetime.fromisoformat(str(row["created_at"])),
        )
