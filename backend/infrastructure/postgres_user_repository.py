from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor
from domain.user import User
from domain.language import Language
from domain.regional_context import RegionalContext
from typing import Optional
import structlog

logger = structlog.get_logger()

class PostgresUserRepository:

    def __init__(self, pool: ThreadedConnectionPool):
        self.pool = pool

    def save(self, user: User) -> None:
        conn = None
        try:
            conn = self.pool.getconn()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("INSERT INTO users"
                " (id, email, phone_number, name, password_hash, language, province_state, country) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (str(user.id), user.email, user.phone_number, user.name, user.password_hash,
                 user.language.value, user.province_state.province_state, user.province_state.country))
            conn.commit()
            logger.info("User created", user_id=str(user.id))
        except Exception:
            logger.exception("User creation failed", user_id=str(user.id))
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                self.pool.putconn(conn)

    def find_by_email(self, email: str) -> Optional[User]:
        conn = None
        try:
            conn = self.pool.getconn()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT id, email, phone_number, name, password_hash, language, province_state, country FROM users WHERE email = %s", (email,))
                res = cur.fetchone()
                if res is None:
                    return None
                return User(id=res["id"], email=res["email"], phone_number=res["phone_number"],
                            name=res["name"], password_hash=res["password_hash"],
                            language=Language(res["language"]),
                            province_state=RegionalContext(res["province_state"], res["country"]))
        except Exception:
            logger.exception("find_by_email failed", email=str(email))
        finally:
            if conn:
                self.pool.putconn(conn)

    def find_by_phone_number(self, phone: str) -> Optional[User]:
        conn = None
        try:
            conn = self.pool.getconn()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT id, email, phone_number, name, password_hash, language, province_state, country FROM users WHERE phone_number = %s", (phone,))
                res = cur.fetchone()
                if res is None:
                    return None
                return User(id=res["id"], email=res["email"], phone_number=res["phone_number"],
                            name=res["name"], password_hash=res["password_hash"],
                            language=Language(res["language"]),
                            province_state=RegionalContext(res["province_state"], res["country"]))
        except Exception:
            logger.exception("find_by_phone_number failed", phone=str(phone))
        finally:
            if conn:
                self.pool.putconn(conn)
