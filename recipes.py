"""Functions to interact with recipe data"""
from db import db


def create_recipe(recipe, instruction, ingredients, amounts, units, user_id):
    sql = "INSERT INTO recipes (name, user_id) VALUES (:recipe, :user_id) RETURNING id"
    result = db.session.execute(sql, {"recipe": recipe, "user_id": user_id})
    recipe_id = result.fetchone()[0]
    for step in instruction:
        if step != "":
            sql = """INSERT INTO instructions (recipe_id, instruction)
            VALUES (:recipe_id, :instruction)"""
            db.session.execute(sql, {"recipe_id": recipe_id,
                                     "instruction": step})
    for i, ingredient in enumerate(ingredients):
        if ingredient != "" and amounts[i] != "":
            sql = """INSERT INTO ingredients (recipe_id, ingredient, amount, unit)
             VALUES (:recipe_id, :ingredient, :amount, :unit)"""
            db.session.execute(sql, {"recipe_id": recipe_id,
                                     "ingredient": ingredient, "amount": amounts[i],
                                     "unit": units[i]})
    db.session.commit()
    return recipe_id


def delete_recipe(recipe_id):
    sql = "DELETE FROM recipes WHERE id=:recipe_id"
    db.session.execute(sql, {"recipe_id": recipe_id})
    db.session.commit()


def get_recipes(argument=None):
    if not argument:
        sql = """SELECT r.id, r.name, u.username, (SELECT COUNT(*) FROM likes
        WHERE recipe_id=r.id) likecount FROM recipes r LEFT JOIN users u ON
        r.user_id = u.id ORDER BY r.id DESC LIMIT 20;"""
        result = db.session.execute(sql)
        return result.fetchall()
    if argument == "mostlikes":
        sql = """SELECT r.id, r.name, u.username, (SELECT COUNT(*) FROM likes
        WHERE recipe_id=r.id) likecount FROM recipes r LEFT JOIN users u ON
        r.user_id = u.id ORDER BY likecount DESC LIMIT 20;"""
        result = db.session.execute(sql)
        return result.fetchall()
    return []


def get_users_liked_recipes(user_id):
    sql = """SELECT r.id, r.name
    FROM recipes r LEFT JOIN likes l ON r.id = l.recipe_id
    WHERE l.user_id = :user_id ORDER BY r.name DESC"""
    result = db.session.execute(sql, {"user_id": user_id})
    return result.fetchall()


def get_recipe_info(recipe_id):
    sql = """SELECT r.name, u.username, u.id FROM recipes r LEFT JOIN users u ON r.user_id = u.id
    WHERE r.id=:id;"""
    result = db.session.execute(sql, {"id": recipe_id})
    recipe_info = result.fetchone()
    sql = "SELECT id, instruction FROM instructions WHERE recipe_id=:id"
    result = db.session.execute(sql, {"id": recipe_id})
    instructions = result.fetchall()
    sql = "SELECT id, ingredient, amount, unit FROM ingredients WHERE recipe_id=:id"
    result = db.session.execute(sql, {"id": recipe_id})
    ingredients = result.fetchall()
    return (recipe_info, instructions, ingredients)


def update_recipe(recipe_id, new_instructions, new_ingredients, new_amounts, new_units):
    old_recipe = get_recipe_info(recipe_id)
    old_instruction = old_recipe[1]
    old_ingredients = old_recipe[2]
    for i, instruction in enumerate(new_instructions):
        if i > len(old_instruction)-1:
            if instruction != "":
                sql = """INSERT INTO instructions (recipe_id, instruction)
                VALUES (:recipe_id, :instruction)"""
                db.session.execute(sql, {"recipe_id": recipe_id,
                                         "instruction": instruction})
        elif instruction != "":
            sql = "UPDATE instructions SET instruction = :new_instruction WHERE id=:id;"
            db.session.execute(sql, {"new_instruction": instruction,
                                     "id": old_instruction[i][0]})
        elif instruction == "":
            sql = "DELETE FROM instructions WHERE id=:id;"
            db.session.execute(sql, {"id": old_instruction[i][0]})
    for i, ingredient in enumerate(new_ingredients):
        if i > len(old_ingredients)-1:
            if ingredient != "" and new_amounts[i] != "":
                sql = """INSERT INTO ingredients (recipe_id, ingredient, amount, unit)
                VALUES (:recipe_id, :ingredient, :amount, :unit)"""
                db.session.execute(sql, {"recipe_id": recipe_id,
                                         "ingredient": ingredient, "amount": int(new_amounts[i]),
                                         "unit": new_units[i]})
        elif ingredient != "" and new_amounts[i] != "":
            sql = """UPDATE ingredients SET ingredient = :new_ingredient,
            amount = :new_amount, unit = :new_unit WHERE id=:id;"""
            db.session.execute(sql, {"new_ingredient": ingredient,
                                     "new_amount": new_amounts[i], "new_unit": new_units[i],
                                     "id": old_ingredients[i][0]})
        elif ingredient == "":
            sql = "DELETE FROM ingredients WHERE id=:id;"
            db.session.execute(sql, {"id": old_ingredients[i][0]})
    db.session.commit()


def validate_recipe_edit(instructions, ingredients, amounts):
    input_errors = []
    not_valid = True
    for text in instructions:
        if text != "":
            not_valid = False
            break
    if not_valid:
        input_errors.append(
            'Recipe needs to have atleast one instruction step!')
    not_valid = True
    for i, ingredient in enumerate(ingredients):
        if ingredient != "" and amounts[i] != "":
            not_valid = False
            break
    if not_valid:
        input_errors.append(
            'Recipe needs to have atleast one ingredient with an amount!')
    return input_errors


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
    for cooking_plan in enumerate(cooking_plans):
        if (cooking_plan[0], cooking_plan[1]) not in cp_dict:
            cp_dict[(cooking_plan[0], cooking_plan[1])] = [
                cooking_plan[2]]
        else:
            cp_dict[(cooking_plan[0], cooking_plan[1])
                    ].append(cooking_plan[2])
    return cp_dict


def get_cp_ingredients(cp_id):
    sql = """
        SELECT i.ingredient, i.amount, i.unit, i.id
        FROM cp_recipes c, ingredients i
        WHERE c.cp_id=:cp_id AND i.recipe_id=c.recipe_id AND i.id not in
        (SELECT ingredient_id FROM cp_hidden WHERE cp_id=:cp_id)
        ORDER BY i.ingredient"""
    result = db.session.execute(sql, {"cp_id": cp_id})
    return result.fetchall()


def get_cp_info(cp_id):
    sql = "SELECT user_id, name FROM cooking_plans WHERE id=:id;"
    result = db.session.execute(sql, {"id": cp_id})
    return result.fetchall()


def get_cp_recipes(cp_id):
    sql = """SELECT r.name, r.id FROM recipes r LEFT JOIN cp_recipes c
    ON r.id=c.recipe_id WHERE c.cp_id=:id;"""
    result = db.session.execute(sql, {"id": cp_id})
    return result.fetchall()


def check_like(user_id, recipe_id):
    sql = "SELECT id FROM likes WHERE user_id=:user_id AND recipe_id=:recipe_id"
    result = db.session.execute(
        sql, {"user_id": user_id, "recipe_id": recipe_id})
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
        db.session.execute(
            sql, {"cp_id": cp_id, "ingredient_id": ingredient_id})
    db.session.commit()


def unhide_cp_ingredients(cp_id):
    sql = "DELETE FROM cp_hidden WHERE cp_id=:cp_id;"
    db.session.execute(sql, {"cp_id": cp_id})
    db.session.commit()
