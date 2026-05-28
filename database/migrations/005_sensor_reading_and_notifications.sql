
CREATE TABLE IF NOT EXISTS sensor_reading (
    id UUID PRIMARY KEY,
    producer_id UUID NOT NULL,
    producer_type VARCHAR(50) NOT NULL,
    crop_type VARCHAR(100),
    province_state VARCHAR(100) NOT NULL,
    data_precision VARCHAR(20) NOT NULL,
    recorded_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS sensor_measurement (
    id UUID PRIMARY KEY,
    reading_id UUID NOT NULL REFERENCES sensor_reading(id),
    sensor_type VARCHAR(50) NOT NULL,
    value NUMERIC(10, 4) NOT NULL,
    unit VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS crop_notification (
    id UUID PRIMARY KEY,
    producer_id UUID NOT NULL,
    topic VARCHAR(100) NOT NULL,
    message TEXT NOT NULL,
    language VARCHAR(20) NOT NULL,
    confidence NUMERIC(4, 3),
    data_precision VARCHAR(20) NOT NULL,
    sent_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_sensor_reading_producer_time
    ON sensor_reading (producer_id, recorded_at DESC);

CREATE INDEX IF NOT EXISTS idx_crop_notification_producer_topic_time
    ON crop_notification (producer_id, topic, sent_at DESC);