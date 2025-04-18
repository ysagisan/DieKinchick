CREATE TABLE IF NOT EXISTS films_information (
    id SERIAL PRIMARY KEY,
    kinopoiskId INT NOT NULL,
    name TEXT NOT NULL,
    year INT,
    genre TEXT,
    rating REAL,
    webUrl TEXT,
    description TEXT
);