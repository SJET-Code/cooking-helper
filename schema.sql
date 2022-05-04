DROP TABLE users CASCADE;
DROP TABLE recipes CASCADE;
DROP TABLE instructions CASCADE;
DROP TABLE ingredients CASCADE;
DROP TABLE likes CASCADE;
DROP TABLE cooking_plans CASCADE;
DROP TABLE cp_recipes CASCADE;
DROP TABLE cp_hidden CASCADE;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);
CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
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
    amount INTEGER,
    unit TEXT
);
CREATE TABLE likes (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes,
    user_id INTEGER REFERENCES users
);
CREATE TABLE cooking_plans (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    name TEXT
);
CREATE TABLE cp_recipes (
    id SERIAL PRIMARY KEY,
    cp_id INTEGER REFERENCES cooking_plans,
    recipe_id INTEGER REFERENCES recipes
);
CREATE TABLE cp_hidden (
    id SERIAL PRIMARY KEY,
    cp_id INTEGER REFERENCES cooking_plans,
    ingredient_id INTEGER REFERENCES ingredients
);
ALTER TABLE instructions
DROP CONSTRAINT instructions_recipe_id_fkey, 
ADD CONSTRAINT instructions_recipe_id_fkey
FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON DELETE CASCADE;
ALTER TABLE ingredients
DROP CONSTRAINT ingredients_recipe_id_fkey, 
ADD CONSTRAINT ingredients_recipe_id_fkey
FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON DELETE CASCADE;
ALTER TABLE cp_recipes
DROP CONSTRAINT cp_recipes_recipe_id_fkey,
ADD CONSTRAINT cp_recipes_recipe_id_fkey
FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON DELETE CASCADE;
ALTER TABLE likes
DROP CONSTRAINT likes_recipe_id_fkey,
ADD CONSTRAINT likes_recipe_id_fkey
FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON DELETE CASCADE;
ALTER TABLE cp_recipes
DROP CONSTRAINT cp_recipes_cp_id_fkey,
ADD CONSTRAINT cp_recipes_cp_id_fkey
FOREIGN KEY (cp_id) REFERENCES cooking_plans (id) ON DELETE CASCADE;
ALTER TABLE cp_hidden
DROP CONSTRAINT cp_hidden_cp_id_fkey,
ADD CONSTRAINT cp_hidden_cp_id_fkey
FOREIGN KEY (cp_id) REFERENCES cooking_plans (id) ON DELETE CASCADE;
ALTER TABLE cp_hidden
DROP CONSTRAINT cp_hidden_ingredient_id_fkey,
ADD CONSTRAINT cp_hidden_ingredient_id_fkey
FOREIGN KEY (ingredient_id) REFERENCES ingredients (id) ON DELETE CASCADE;