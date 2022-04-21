from db import db


def create_recipe(recipe, instruction, ingredients, amounts, user_id):
    sql = "INSERT INTO recipes (name, user_id) VALUES (:recipe, :user_id) RETURNING id"
    result = db.session.execute(sql, {"recipe": recipe, "user_id": user_id})
    recipe_id = result.fetchone()[0]
    for i in range(len(instruction)):
        if instruction[i] != "":
            sql = """INSERT INTO instructions (recipe_id, instruction)
            VALUES (:recipe_id, :instruction)"""
            db.session.execute(sql, {"recipe_id": recipe_id,
                                     "instruction": instruction[i]})
    for i in range(len(ingredients)):
        if ingredients[i] != "":
            sql = """INSERT INTO ingredients (recipe_id, ingredient, amount)
             VALUES (:recipe_id, :ingredient, :amount)"""
            db.session.execute(sql, {"recipe_id": recipe_id,
                                     "ingredient": ingredients[i], "amount": amounts[i]})
    db.session.commit()
    return recipe_id


def delete_recipe(recipe_id):
    sql = "DELETE FROM recipes WHERE id=:recipe_id"
    db.session.execute(sql, {"recipe_id": recipe_id})
    db.session.commit()


def get_recipes(argument=None):
    if not argument:
        sql = """SELECT r.id, r.name, u.username, (SELECT COUNT(*) FROM likes WHERE recipe_id=r.id) likecount 
        FROM recipes r LEFT JOIN users u ON r.user_id = u.id ORDER BY r.id DESC LIMIT 20;"""
        result = db.session.execute(sql)
        return result.fetchall()
    if argument=="mostlikes":
        sql = """SELECT r.id, r.name, u.username, (SELECT COUNT(*) FROM likes WHERE recipe_id=r.id) likecount 
        FROM recipes r LEFT JOIN users u ON r.user_id = u.id ORDER BY likecount DESC LIMIT 20;"""
        result = db.session.execute(sql)
        return result.fetchall()
    if type(argument) == list and len(argument) != 0:
        recipe_ids = "("
        for i in range(len(argument)):
            if i == len(argument)-1:
                recipe_ids += str(argument[i][0])+")"
            else:
                recipe_ids += str(argument[i][0])+","
        sql = "SELECT id, name FROM recipes WHERE id in "+recipe_ids+" ORDER BY id DESC"
        result = db.session.execute(sql)
        return result.fetchall()
    return []


def get_recipe_info(id):
    sql = """SELECT r.name, u.username, u.id FROM recipes r LEFT JOIN users u ON r.user_id = u.id 
    WHERE r.id=:id;"""
    result = db.session.execute(sql, {"id": id})
    recipe_info = result.fetchone()
    sql = "SELECT id, instruction FROM instructions WHERE recipe_id=:id"
    result = db.session.execute(sql, {"id": id})
    instructions = result.fetchall()
    sql = "SELECT id, ingredient, amount FROM ingredients WHERE recipe_id=:id"
    result = db.session.execute(sql, {"id": id})
    ingredients = result.fetchall()
    return (recipe_info, instructions, ingredients)


def update_recipe(recipe_id, new_instructions, new_ingredients, new_amounts):
    old_recipe = get_recipe_info(recipe_id)
    old_instruction = old_recipe[1]
    old_ingredients = old_recipe[2]
    for i in range(len(new_instructions)):
        if i > len(old_instruction)-1:
            if new_instructions[i] != "":
                sql = """INSERT INTO instructions (recipe_id, instruction) 
                VALUES (:recipe_id, :instruction)"""
                db.session.execute(sql, {"recipe_id": recipe_id,
                                         "instruction": new_instructions[i]})
        elif new_instructions[i] != "":
            sql = "UPDATE instructions SET instruction = :new_instruction WHERE id=:id;"
            db.session.execute(sql, {"new_instruction": new_instructions[i],
                                     "id": old_instruction[i][0]})
        elif new_instructions[i] == "":
            sql = "DELETE FROM instructions WHERE id=:id;"
            db.session.execute(sql, {"id": old_instruction[i][0]})
    for i in range(len(new_ingredients)):
        if i > len(old_ingredients)-1:
            if new_ingredients[i] != "":
                sql = """INSERT INTO ingredients (recipe_id, ingredient, amount) 
                VALUES (:recipe_id, :ingredient, :amount)"""
                db.session.execute(sql, {"recipe_id": recipe_id,
                                         "ingredient": new_ingredients[i], "amount": new_amounts[i]})
        elif new_ingredients[i] != "":
            sql = """UPDATE ingredients SET ingredient = :new_ingredient, 
            amount = :new_amount WHERE id=:id;"""
            db.session.execute(sql, {"new_ingredient": new_ingredients[i],
                                     "new_amount": new_amounts[i], "id": old_ingredients[i][0]})
        elif new_ingredients[i] == "":
            sql = "DELETE FROM ingredients WHERE id=:id;"
            db.session.execute(sql, {"id": old_ingredients[i][0]})
    db.session.commit()


def get_liked(user_id):
    sql = "SELECT recipe_id FROM likes WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id": user_id})
    return result.fetchall()


def like_recipe(user_id, recipe_id):
    sql = "INSERT INTO likes (recipe_id, user_id) VALUES (:recipe_id, :user_id)"
    db.session.execute(sql, {"recipe_id": recipe_id, "user_id": user_id})
    db.session.commit()


def unlike_recipe(user_id, recipe_id):
    sql = "DELETE FROM likes WHERE recipe_id=:recipe_id AND user_id=:user_id"
    db.session.execute(sql, {"recipe_id": recipe_id, "user_id": user_id})
    db.session.commit()


def create_cp(user_id, cp_name, recipe_list):
    sql = "INSERT INTO cooking_plans (user_id, name) VALUES (:user_id, :cp_name) RETURNING id"
    result = db.session.execute(sql, {"user_id": user_id, "cp_name": cp_name})
    cp_id = result.fetchone()[0]
    for recipe in recipe_list:
        sql = "INSERT INTO cp_recipes (cp_id, recipe_id) VALUES (:cp_id, :recipe)"
        db.session.execute(sql, {"cp_id": cp_id, "recipe": recipe})
    db.session.commit()
    return cp_id


def delete_cp(cp_id):
    sql = "DELETE FROM cooking_plans WHERE id=:cp_id;"
    db.session.execute(sql, {"cp_id": cp_id})
    db.session.commit()


def get_cooking_plans(user_id):
    sql = """SELECT a.id, a.name, c.name FROM cooking_plans a LEFT JOIN cp_recipes b 
    ON a.id = b.cp_id LEFT JOIN recipes c ON b.recipe_id = c.id WHERE a.user_id=:user_id;"""
    result = db.session.execute(sql, {"user_id": user_id})
    cooking_plans = result.fetchall()
    cp_dict = {}
    for i in range(len(cooking_plans)):
        if (cooking_plans[i][0], cooking_plans[i][1]) not in cp_dict:
            cp_dict[(cooking_plans[i][0], cooking_plans[i][1])] = [
                cooking_plans[i][2]]
        else:
            cp_dict[(cooking_plans[i][0], cooking_plans[i][1])
                    ].append(cooking_plans[i][2])
    return cp_dict


def get_cp_ingredients(cp_id):
    sql = """SELECT i.ingredient, i.amount, i.id FROM cp_recipes c, ingredients i 
    WHERE c.cp_id=:cp_id AND i.recipe_id=c.recipe_id AND i.id not in (SELECT ingredient_id FROM cp_hidden WHERE cp_id=:cp_id) ORDER BY i.ingredient"""
    result = db.session.execute(sql, {"cp_id": cp_id})
    return result.fetchall()


def get_cp_info(id):
    sql = "SELECT user_id, name FROM cooking_plans WHERE id=:id;"
    result = db.session.execute(sql, {"id": id})
    return result.fetchall()


def get_cp_recipes(id):
    sql = """SELECT r.name, r.id FROM recipes r LEFT JOIN cp_recipes c 
    ON r.id=c.recipe_id WHERE c.cp_id=:id;"""
    result = db.session.execute(sql, {"id": id})
    return result.fetchall()

def check_like(user_id, recipe_id):
    sql = "SELECT id FROM likes WHERE user_id=:user_id AND recipe_id=:recipe_id"
    result = db.session.execute(sql, {"user_id": user_id, "recipe_id": recipe_id})
    return len(result.fetchall()) != 0

def get_recipe_likes(recipe_id):
    sql = "SELECT COUNT(*) FROM likes WHERE recipe_id=:recipe_id"
    result = db.session.execute(sql, {"recipe_id": recipe_id})
    return result.fetchone()[0]

def edit_cp(cp_id, cp_name, recipe_ids):
    sql = "UPDATE cooking_plans SET name = :cp_name WHERE id = :cp_id;"
    db.session.execute(sql, {"cp_name": cp_name, "cp_id": cp_id})
    sql = "DELETE FROM cp_recipes WHERE cp_id = :cp_id;"
    db.session.execute(sql, {"cp_id": cp_id})
    for recipe in recipe_ids:
        sql = "INSERT INTO cp_recipes (cp_id, recipe_id) VALUES (:cp_id, :recipe)"
        db.session.execute(sql, {"cp_id": cp_id, "recipe": recipe})
    db.session.commit()

def hide_cp_ingredients(cp_id, ingredient_ids):
    for ingredient_id in ingredient_ids:
        sql = """INSERT INTO cp_hidden (cp_id, ingredient_id) VALUES (:cp_id, :ingredient_id);"""
        db.session.execute(sql, {"cp_id": cp_id, "ingredient_id": ingredient_id})
    db.session.commit()

def unhide_cp_ingredients(cp_id):
    sql = """DELETE FROM cp_hidden WHERE cp_id=:cp_id;"""
    db.session.execute(sql, {"cp_id": cp_id})
    db.session.commit()