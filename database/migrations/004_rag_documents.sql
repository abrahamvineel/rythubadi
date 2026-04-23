CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS rag_documents (
    id UUID PRIMARY KEY,
    scheme_name TEXT NOT NULL,
    content TEXT NOT NULL,
    country TEXT NOT NULL,
    province TEXT,
    source_url TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    embedding vector(1536),
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX ON rag_documents USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX ON rag_documents (country, province);
