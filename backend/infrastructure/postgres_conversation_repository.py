from domain.chat_message import ChatMessage
from domain.chat_session import ChatSession
from uuid import UUID
from typing import Optional
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor
import structlog

logger = structlog.get_logger()

class PostgresConversationRepository:

    def __init__(self, pool: ThreadedConnectionPool):
        self._pool = pool

    def create(self, session: ChatSession) -> None:
        conn = None
        try:
            conn = self._pool.getconn()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "INSERT INTO chat_session (id, title, producer_id, is_deleted) VALUES (%s, %s, %s, %s)",
                    (str(session.id), session.title, session.producer_id, session.is_deleted)
                )
            conn.commit()
            logger.info("chat_session created", session_id=str(session.id))
        except Exception:
            if conn:
                conn.rollback()
            logger.exception("create failed", session_id=str(session.id))
            raise
        finally:
            if conn:
                self._pool.putconn(conn)

    def find_all_by_user(self, user_id: str) -> list[ChatSession]:
        conn = None
        try:
            conn = self._pool.getconn()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT id, title, producer_id, is_deleted FROM chat_session "
                    "WHERE producer_id = %s AND is_deleted = false ORDER BY created_at DESC",
                    (user_id,)
                )
                rows = cur.fetchall()
                return [ChatSession(id=r["id"], title=r["title"], producer_id=r["producer_id"], is_deleted=r["is_deleted"]) for r in rows]
        except Exception:
            logger.exception("find_all_by_user failed", user_id=user_id)
            return []
        finally:
            if conn:
                self._pool.putconn(conn)

    def delete(self, session_id: UUID, user_id: str) -> None:
        conn = None
        try:
            conn = self._pool.getconn()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "UPDATE chat_session SET is_deleted = true WHERE id = %s AND producer_id = %s",
                    (str(session_id), user_id)
                )
            conn.commit()
            logger.info("chat_session deleted", session_id=str(session_id))
        except Exception:
            if conn:
                conn.rollback()
            logger.exception("delete failed", session_id=str(session_id))
            raise
        finally:
            if conn:
                self._pool.putconn(conn)

    def find_messages_by_session(self, session_id: UUID) -> list[ChatMessage]:
        conn = None
        try:
            conn = self._pool.getconn()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT chat_session_id, content, attachment_url, system_generated, language "
                    "FROM chat_message WHERE chat_session_id = %s ORDER BY created_at ASC",
                    (str(session_id),)
                )
                rows = cur.fetchall()
                return [ChatMessage(chat_session_id=r["chat_session_id"], content=r["content"],
                                    attachment_url=r["attachment_url"], system_generated=r["system_generated"],
                                    language=r["language"]) for r in rows]
        except Exception:
            logger.exception("find_messages_by_session failed", session_id=str(session_id))
            return []
        finally:
            if conn:
                self._pool.putconn(conn)

    def save_message(self, message: ChatMessage) -> None:
        conn = None
        try:
            conn = self._pool.getconn()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "INSERT INTO chat_message (chat_session_id, content, attachment_url, system_generated, language) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (str(message.chat_session_id), message.content, message.attachment_url, message.system_generated, message.language)
                )
            conn.commit()
            logger.info("chat_message saved", session_id=str(message.chat_session_id))
        except Exception:
            if conn:
                conn.rollback()
            logger.exception("save_message failed", session_id=str(message.chat_session_id))
            raise
        finally:
            if conn:
                self._pool.putconn(conn)
