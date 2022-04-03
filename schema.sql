CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    name TEXT
);
CREATE TABLE instructions (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes,
    instruction TEXT
);
CREATE TABLE ingredients (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes,
    ingredient TEXT,
    amount TEXT
);
