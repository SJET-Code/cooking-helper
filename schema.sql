CREATE TABLE recepies (
    id SERIAL PRIMARY KEY,
    name TEXT
);
CREATE TABLE ingredients (
    id SERIAL PRIMARY KEY,
    recepie_id INTEGER REFERENCES recepies,
    ingredient TEXT,
    amount INTEGER
);
