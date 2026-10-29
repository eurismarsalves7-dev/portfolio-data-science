CREATE TABLE IF NOT EXISTS authorized_vehicles (
    id SERIAL PRIMARY KEY,
    plate VARCHAR(7) UNIQUE NOT NULL,
    responsible_name VARCHAR(120) NOT NULL,
    student_name VARCHAR(120) NOT NULL,
    class_name VARCHAR(40) NOT NULL,
    room VARCHAR(40),
    authorized BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS idx_authorized_vehicles_plate
    ON authorized_vehicles (plate);

CREATE TABLE IF NOT EXISTS access_events (
    id SERIAL PRIMARY KEY,
    plate VARCHAR(7),
    status VARCHAR(60) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_access_events_plate
    ON access_events (plate);
