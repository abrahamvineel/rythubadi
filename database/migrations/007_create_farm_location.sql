CREATE TABLE IF NOT EXISTS farm_location (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    producer_id    UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name           TEXT NOT NULL,
    latitude       NUMERIC(9,6) NOT NULL,
    longitude      NUMERIC(9,6) NOT NULL,
    producer_types TEXT[] NOT NULL,
    created_at     TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS farm_location_producer_idx ON farm_location(producer_id);
