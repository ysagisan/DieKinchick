CREATE TABLE IF NOT EXISTS films_information (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    year INT,
    genre TEXT,
    rating REAL,
    description TEXT
);