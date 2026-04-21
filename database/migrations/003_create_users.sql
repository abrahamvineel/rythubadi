DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY,
    email TEXT UNIQUE,
    phone_number TEXT UNIQUE,
    CHECK (email IS NOT NULL OR phone_number IS NOT NULL),
    name TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    language VARCHAR(5) NOT NULL DEFAULT 'EN',
    province_state VARCHAR(255) NOT NULL DEFAULT 'general',
    country VARCHAR(10) NOT NULL DEFAULT 'CA',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);
