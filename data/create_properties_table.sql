CREATE TABLE IF NOT EXISTS properties (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    price VARCHAR(50),
    sqm_price VARCHAR(50),
    area VARCHAR(50),
    city VARCHAR(50),
    link VARCHAR(255)
);
