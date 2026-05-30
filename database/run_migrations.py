"""
Run all SQL migrations in database/migrations/ in numeric order.

Tracks applied migrations in a schema_migrations table so re-running
this script is safe — already-applied files are skipped.

Usage:
    python database/run_migrations.py
"""
import os
import sys
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    print("ERROR: DATABASE_URL env var is not set.")
    sys.exit(1)

MIGRATIONS_DIR = Path(__file__).parent / "migrations"


def ensure_tracking_table(conn) -> None:
    """Create schema_migrations if it doesn't exist."""
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS schema_migrations (
                filename   TEXT PRIMARY KEY,
                applied_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
    conn.commit()


def already_applied(conn, filename: str) -> bool:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT 1 FROM schema_migrations WHERE filename = %s", (filename,)
        )
        return cur.fetchone() is not None


def record_applied(conn, filename: str) -> None:
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO schema_migrations (filename) VALUES (%s)", (filename,)
        )
    conn.commit()


def run_migrations() -> None:
    conn = psycopg2.connect(DATABASE_URL)
    try:
        ensure_tracking_table(conn)

        sql_files = sorted(MIGRATIONS_DIR.glob("*.sql"))
        if not sql_files:
            print("No migration files found.")
            return

        applied = skipped = 0
        for path in sql_files:
            filename = path.name
            if already_applied(conn, filename):
                print(f"  skip  {filename}")
                skipped += 1
                continue

            sql = path.read_text(encoding="utf-8")
            print(f"  apply {filename} ... ", end="", flush=True)
            try:
                with conn.cursor() as cur:
                    cur.execute(sql)
                conn.commit()
                record_applied(conn, filename)
                print("ok")
                applied += 1
            except (psycopg2.errors.DuplicateObject, psycopg2.errors.DuplicateTable):
                # Type / index / table already exists — migration was applied
                # before the tracking table existed. Mark it and move on.
                conn.rollback()
                record_applied(conn, filename)
                print("already existed — marked as applied")
                skipped += 1
            except (psycopg2.errors.UndefinedFile,
                    psycopg2.errors.FeatureNotSupported) as exc:
                # A required Postgres extension (e.g. pgvector) is not installed.
                # Warn and skip — the app runs without it in local dev.
                conn.rollback()
                print(f"SKIPPED — extension not available")
                print(f"  {exc.pgerror.strip()}")
                print("  Install pgvector to enable RAG / SchemeAdvisor features.")
            except Exception as exc:
                conn.rollback()
                print(f"FAILED\n  {exc}")
                sys.exit(1)

        print(f"\nDone — {applied} applied, {skipped} already up to date.")
    finally:
        conn.close()


if __name__ == "__main__":
    run_migrations()
