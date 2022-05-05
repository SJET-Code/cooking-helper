"""Directs user to different parts of the website"""
from flask import redirect, render_template, request, session, abort
from app import app
import recipes
import users


@app.route("/")
def index():
    return render_template("index.html", recipes=recipes.get_recipes(),
                           liked_recipes=recipes.get_recipes("mostlikes"), user=users.is_user(),
                           username=users.get_username(users.user_id()))


@app.route("/new")
def new():
    if users.is_user():
        return render_template("new.html", user=users.is_user(),
                               username=users.get_username(users.user_id()))
    return redirect("/login")


@app.route("/create", methods=["POST"])
def create():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    recipe_name = request.form["Recipe name"]
    instruction = request.form.getlist("instructions")
    ingredients = request.form.getlist("ingredient")
    amounts = request.form.getlist("amount")
    units = request.form.getlist("unit")
    recipe_id = recipes.create_recipe(
        recipe_name, instruction, ingredients, amounts, units, users.user_id())
    return redirect("/recipe/"+str(recipe_id))


@app.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
    recipe_info = recipes.get_recipe_info(recipe_id)
    if len(recipe_info) == 0:
        return render_template("error.html", message=["No such recipe!"], user=users.is_user())
    like = recipes.check_like(users.user_id(), recipe_id)
    return render_template("recipe.html", id=recipe_id, recipe=recipe_info[0][0],
                           instructions=recipe_info[1], ingredients=recipe_info[2],
                           maker=recipe_info[0][1], user=users.is_user(),
                           is_owner=users.user_id() == recipe_info[0][2],
                           like=like, likes=recipes.get_recipe_likes(recipe_id),
                           username=users.get_username(users.user_id()))


@app.route("/recipe/<int:recipe_id>/edit", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    if request.method == "GET":
        recipe_info = recipes.get_recipe_info(recipe_id)
        if users.user_id() != recipe_info[0][2]:
            return render_template("error.html",
                                   message=[
                                       "Only the creator of the recipe can edit it!"],
                                   user=users.is_user(),
                                   username=users.get_username(users.user_id()))
        return render_template("edit_recipe.html", id=recipe_id, recipe=recipe_info[0][0],
                               instructions=recipe_info[1],
                               ingredients=recipe_info[2], maker=recipe_info[0][1],
                               user=users.is_user())
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        instruction = request.form.getlist("instructions")
        ingredients = request.form.getlist("ingredient")
        amounts = request.form.getlist("amount")
        units = request.form.getlist("unit")
        input_errors = recipes.validate_recipe_edit(
            instruction, ingredients, amounts)
        if not input_errors:
            recipes.update_recipe(recipe_id, instruction,
                                  ingredients, amounts, units)
            return redirect("/recipe/"+str(recipe_id))
        recipe_info = recipes.get_recipe_info(recipe_id)
        return render_template("edit_recipe.html", message=input_errors, id=recipe_id,
                               recipe=recipe_info[0][0], instructions=recipe_info[1],
                               ingredients=recipe_info[2], maker=recipe_info[0][1],
                               user=users.is_user(),
                               username=users.get_username(users.user_id()))


@app.route("/recipe/<int:recipe_id>/like")
def like_recipe(recipe_id):
    if users.user_id() == 0:
        return redirect("/login")
    liked = recipes.get_liked(users.user_id())
    like = False
    for recipe_info in liked:
        if recipe_info[0] == recipe_id:
            like = True
            break
    if like:
        recipes.unlike_recipe(users.user_id(), recipe_id)
        return redirect("/recipe/"+str(recipe_id))
    recipes.like_recipe(users.user_id(), recipe_id)
    return redirect("/recipe/"+str(recipe_id))


@app.route("/recipe/<int:recipe_id>/unlike")
def unlike_recipe(recipe_id):
    if users.user_id() == 0:
        return redirect("/login")
    recipes.unlike_recipe(users.user_id(), recipe_id)
    return redirect("/recipe/"+str(recipe_id))


@app.route("/recipe/<int:recipe_id>/delete")
def delete_recipe(recipe_id):
    recipe_info = recipes.get_recipe_info(recipe_id)
    if users.user_id() != recipe_info[0][2]:
        return render_template("error.html",
                               message=["Only the creator of the recipe can delete it!"],
                               user=users.is_user(),
                               username=users.get_username(users.user_id()))
    recipes.delete_recipe(recipe_id)
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        user_name = request.form["username"]
        password = request.form["password"]
        input_errors = users.login(user_name, password)
        if not input_errors:
            return redirect("/")
        return render_template("login.html", message=input_errors, user=users.is_user(),
                               username=users.get_username(users.user_id()))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        if users.is_user():
            return redirect("/")
        return render_template("register.html")
    if request.method == "POST":
        user_name = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("register.html", message=["The passwords differ"],
                                   user=users.is_user(),
                                   username=users.get_username(users.user_id()))
        input_errors = users.register(user_name, password1)
        if not input_errors:
            return redirect("/")
        return render_template("register.html", message=input_errors, user=users.is_user())


@app.route("/logout")
def logout():
    if users.is_user():
        users.logout()
    return redirect("/")


@app.route("/new_cooking_plan", methods=["GET", "POST"])
def new_cooking_plan():
    if users.user_id() == 0:
        return redirect("/login")
    recipe_list = recipes.get_users_liked_recipes(users.user_id())
    if request.method == "GET":
        return render_template("new_cooking_plan.html", recipes=recipe_list,
                               user=users.is_user(), empty=len(recipe_list) == 0,
                               username=users.get_username(users.user_id()))
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        name = request.form["name"]
        recipe_ids = request.form.getlist("id")
        if len(recipe_ids) == 0:
            return render_template("new_cooking_plan.html", recipes=recipe_list,
                                   user=users.is_user(), empty=len(recipe_list) == 0,
                                   message=[
                                       "Can't create an empty Cooking Plan!"],
                                   username=users.get_username(users.user_id()))
        cooking_plan_id = recipes.create_cp(users.user_id(), name, recipe_ids)
        return redirect("/cooking_plan/"+str(cooking_plan_id))


@app.route("/my_page")
def my_cooking_plans():
    if users.user_id() == 0:
        return redirect("/login")
    cooking_plans = recipes.get_cooking_plans(users.user_id())
    user_recipes = recipes.get_recipes(users.user_id())
    return render_template("my_page.html", cooking_plans=cooking_plans,
                           recipes=user_recipes, no_recipes= not user_recipes,
                           user=users.is_user(), no_cps= not cooking_plans,
                           username=users.get_username(users.user_id()))


@app.route("/cooking_plan/<int:cooking_plan_id>")
def cooking_plan(cooking_plan_id):
    cp_info = recipes.get_cp_info(cooking_plan_id)
    if cp_info[0][0] != users.user_id():
        return render_template("error.html",
                               message=["Only the creator of the Cooking Plan can view it!"],
                               user=users.is_user(), username=users.get_username(users.user_id()))
    cp_ingredients = recipes.get_cp_ingredients(cooking_plan_id)
    cp_recipes = recipes.get_cp_recipes(cooking_plan_id)
    return render_template("cooking_plan.html", id=cooking_plan_id, cp_recipes=cp_recipes,
                           cp_ingredients=cp_ingredients, cooking_plan=cp_info[0][1],
                           user=users.is_user(),
                           username=users.get_username(users.user_id()))


@app.route("/cooking_plan/<int:cooking_plan_id>/delete")
def delete_cooking_plan(cooking_plan_id):
    cp_info = recipes.get_cp_info(cooking_plan_id)
    if cp_info[0][0] != users.user_id():
        return render_template("error.html",
                               message=[
                                   "Only the creator of the Cooking Plan can delete it!"],
                               user=users.is_user(), username=users.get_username(users.user_id()))
    recipes.delete_cp(cooking_plan_id)
    return redirect("/")


@app.route("/cooking_plan/<int:cooking_plan_id>/edit", methods=["GET", "POST"])
def edit_cooking_plan(cooking_plan_id):
    cp_info = recipes.get_cp_info(cooking_plan_id)
    if cp_info[0][0] != users.user_id():
        return render_template("error.html",
                               message=[
                                   "Only the creator of the Cooking Plan can edit it!"],
                               user=users.is_user(), username=users.get_username(users.user_id()))
    if request.method == "GET":
        recipe_list = recipes.get_users_liked_recipes(users.user_id())
        return render_template("edit_cooking_plan.html", id=cooking_plan_id,
                               cp_name=cp_info[0][1], recipes=recipe_list,
                               contains=recipes.get_cp_recipes(
                                   cooking_plan_id),
                               user=users.is_user(), username=users.get_username(users.user_id()))
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        name = request.form["name"]
        recipe_ids = request.form.getlist("id")
        if len(recipe_ids) == 0:
            recipe_ids = recipes.get_liked(users.user_id())
            recipe_list = recipes.get_recipes(recipe_ids)
            return render_template("edit_cooking_plan.html",
                                   id=cooking_plan_id, cp_name=cp_info[0][1],
                                   recipes=recipe_list, contains=recipes.get_cp_recipes(
                                       cooking_plan_id),
                                   user=users.is_user(),
                                   message=["Can't create an empty Cooking Plan!"],
                                   username=users.get_username(users.user_id()))
        recipes.edit_cp(cooking_plan_id, name, recipe_ids)
        return redirect("/cooking_plan/"+str(cooking_plan_id))


@app.route("/cooking_plan/<int:cooking_plan_id>/hide", methods=["POST"])
def hide_cooking_plan_ingredients(cooking_plan_id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    ingredient_ids = request.form.getlist("ingredient_id")
    recipes.hide_cp_ingredients(cooking_plan_id, ingredient_ids)
    return redirect("/cooking_plan/"+str(cooking_plan_id))


@app.route("/cooking_plan/<int:cooking_plan_id>/unhide")
def unhide_cooking_plan_ingredients(cooking_plan_id):
    recipes.unhide_cp_ingredients(cooking_plan_id)
    return redirect("/cooking_plan/"+str(cooking_plan_id))
