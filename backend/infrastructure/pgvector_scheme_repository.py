from psycopg2.pool import ThreadedConnectionPool
from domain.regional_context import RegionalContext
from domain.scheme_chunk import SchemeChunk
from openai import OpenAI
import structlog

logger = structlog.get_logger()

class PgVectorSchemeRepository:

    def __init__(self, pool: ThreadedConnectionPool, openai_client: OpenAI):
        self._pool = pool
        self._openai_client = openai_client

    def _embed(self, text: str) -> list[float]:
        response = self._openai_client.embeddings.create(model="text-embedding-3-small", input=text)
        return response.data[0].embedding
    
    def search(self, query, regional_context: RegionalContext, top_k: int) -> list[SchemeChunk]:
        embedding = self._embed(query)
        vector_str = str(embedding)
        conn = None
        try:
            conn = self._pool.getconn()
            with conn.cursor() as cur:
                cur.execute(""" SELECT scheme_name, content, country, province, source_url,
                                1 - (embedding <=> %s::vector) AS similarity_score
                            FROM rag_documents
                            WHERE country = %s
                            AND (province IS NULL OR province = %s)
                            ORDER BY embedding <=> %s::vector
                            LIMIT %s""", (vector_str, regional_context.country, regional_context.province_state, vector_str, top_k))
                res = cur.fetchall()
                return [SchemeChunk(row[0], row[1], row[2], row[3], row[4], row[5]) for row in res]
        except Exception:
            logger.exception("search_failed")
            raise
        finally:
            if conn:
                self._pool.putconn(conn)
            