CREATE TABLE IF NOT EXISTS feed_event (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    producer_id  UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    severity     TEXT NOT NULL CHECK (severity IN ('info', 'warning', 'alert')),
    agent        TEXT NOT NULL,
    agent_emoji  TEXT NOT NULL DEFAULT '🌾',
    title        TEXT NOT NULL,
    body         TEXT NOT NULL,
    subject_type TEXT,
    subject_id   TEXT,
    subject_name TEXT,
    location_id  UUID REFERENCES farm_location(id) ON DELETE SET NULL,
    reply_count  INT NOT NULL DEFAULT 0,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Fetch newest events per producer fast
CREATE INDEX IF NOT EXISTS feed_event_producer_created_idx
    ON feed_event(producer_id, created_at DESC);
