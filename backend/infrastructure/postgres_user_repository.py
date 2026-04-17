from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor
from domain.user import User
from typing import Optional
import structlog 

logger = structlog.get_logger()

class PostgresUserRepository:

    def __init__(self, pool: ThreadedConnectionPool):
        self.pool = pool

    def save(self, user: User) -> None:
        conn = self.pool.getconn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("INSERT INTO users"
                " (id, email, phone_number, name, password_hash, created_at) " \
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (user.id, user.email, user.phone_number, user.name, user.password_hash, user.created_at))
            conn.commit()
            logger.info("User created", user_id=str(user.id))
        except Exception:
            logger.exception("User creation failed", user_id=str(user.id))
            conn.rollback()
        finally:
            self.pool.putconn(conn)

    def find_by_email(self, email: str) -> Optional[User]:
        conn = self.pool.getconn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT id, email, phone_number, name, password_hash, created_at FROM users WHERE email = %s", (email,))
                res = cur.fetchone()
                if res is None:
                    return None
                return User(id=res["id"], email=res["email"], phone_number=res["phone_number"],
                            name=res["name"], password_hash=res["password_hash"], created_at=res["created_at"])
        except Exception:
            logger.exception("find_by_email failed", email=str(email))
        finally:
            self.pool.putconn(conn)

    def find_by_phone_number(self, phone: str) -> Optional[User]:
        conn = self.pool.getconn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT id, email, phone_number, name, password_hash, created_at FROM users WHERE phone_number = %s", (phone,))
                res = cur.fetchone()
                if res is None:
                    return None
                return User(id=res["id"], email=res["email"], phone_number=res["phone_number"],
                            name=res["name"], password_hash=res["password_hash"], created_at=res["created_at"])
        except Exception:
            logger.exception("find_by_phone_number failed", phone=str(phone))
        finally:
            self.pool.putconn(conn)
