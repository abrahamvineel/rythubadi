
CREATE TABLE IF NOT EXISTS chat_session (
    id UUID PRIMARY KEY,
    title TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    producer_id UUID NOT NULL,
    is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS chat_message (
    id BIGSERIAL PRIMARY KEY,
    chat_session_id UUID NOT NULL REFERENCES chat_session(id) ON DELETE CASCADE,
    content TEXT,
    attachment_url VARCHAR(512),
    system_generated BOOLEAN DEFAULT FALSE,
    language VARCHAR,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);
