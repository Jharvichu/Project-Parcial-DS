CREATE TABLE IF NOT EXISTS incident_status (
    id SERIAL PRIMARY KEY,
    label VARCHAR(50) NOT NULL
);

INSERT INTO incident_status (label)
VALUES
    ('nuevo'),
    ('en_revision'),
    ('cerrado')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS incident (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    incident_type VARCHAR(100) NOT NULL,
    zone VARCHAR(100) NOT NULL,
    location VARCHAR(255) NOT NULL,
    description TEXT,
    photo_url VARCHAR(255),
    video_url VARCHAR(255),
    occurred_at TIMESTAMP NOT NULL,
    status_id INTEGER REFERENCES incident_status(id) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);