-- Active: 1738317919126@@127.0.0.1@5432@comments@public
CREATE TABLE test (
    name VARCHAR(50),
    age INT
);
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

