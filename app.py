from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/")
def index():
    sql = "SELECT id, name FROM recipes ORDER BY id DESC"
    result = db.session.execute(sql)
    recipes = result.fetchall()
    return render_template("index.html", recipes=recipes)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/create", methods=["POST"])
def create():
    recipe = request.form["Recipe name"]
    sql = "INSERT INTO recipes (name) VALUES (:recipe) RETURNING id"
    result = db.session.execute(sql, {"recipe":recipe})
    recipe_id = result.fetchone()[0]
    instruction = request.form["Instructions"]
    sql = "INSERT INTO instructions (recipe_id, instruction) VALUES (:recipe_id, :instruction)"
    db.session.execute(sql, {"recipe_id":recipe_id, "instruction":instruction})
    ingredients = request.form.getlist("add ingredient")
    amounts = request.form.getlist("amount")
    for i in range(len(ingredients)):
        if ingredients[i] != "":
            sql = "INSERT INTO ingredients (recipe_id, ingredient, amount) VALUES (:recipe_id, :ingredient, :amount)"
            db.session.execute(sql, {"recipe_id":recipe_id, "ingredient":ingredients[i], "amount":amounts[i]})
    db.session.commit()
    return redirect("/")

@app.route("/recipe/<int:id>")
def recipe(id):
    sql = "SELECT name FROM recipes WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    recipe = result.fetchone()[0]
    sql = "SELECT instruction FROM instructions WHERE recipe_id=:id"
    result = db.session.execute(sql, {"id":id})
    instruction = result.fetchone()[0]  
    sql = "SELECT id, ingredient, amount FROM ingredients WHERE recipe_id=:id"
    result = db.session.execute(sql, {"id":id})
    ingredients = result.fetchall()
    return render_template("recipe.html", id=id, recipe=recipe, instruction=instruction, ingredients=ingredients)
