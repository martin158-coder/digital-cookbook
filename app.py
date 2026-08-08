import os
import pymongo
from routes.recipes import recipes_bp
from flask import Flask, render_template, redirect, request, url_for, jsonify, flash
from extensions import mongo
from dotenv import load_dotenv, find_dotenv
from utils import (
    get_pages,
    generate_pagination_links,
    search_name,
    get_sorted_recipes,
    get_recipe_form_data,
    redirect_to_recipes,
)
from flask_wtf import FlaskForm, Form
from wtforms import validators
from forms import Username, ReusableForm, Search
from config import Config

load_dotenv(find_dotenv())

app = Flask(__name__)

app.config.from_object(Config)
app.secret_key = app.config["SECRET_KEY"]

mongo.init_app(app)

#Ejecutar una sola vez para crear el índice de búsqueda de texto.
# mongo.db.recipes.create_index([
#   ("name", TEXT),
#   ("description", TEXT),
#  ("ingredients", TEXT)
# ])


@app.route("/<username>/search", methods=["GET", "POST"])
def search(username):
    
    wtform = Search(request.form)
    if wtform.validate():
        return redirect(
            url_for(
                "results",
                username=username,
                search=request.form["search"],
                limit=10,
                offset=0,
            )
        )
    return render_template(
        "search.html", username=username, form=wtform, errors=wtform.errors
    )


@app.route("/<username>/search/<search>", methods=["GET", "POST"])
def results(username, search):

    recipes = mongo.db.recipes

    limit = int(request.args.get("limit"))
    offset = 0

    query = {"$text": {"$search": search}}

    count = recipes.count_documents(query)

    if count == 0 or not search:
        return render_template("noresults.html", username=username)

    pages = get_pages(count, limit)
    url_list = generate_pagination_links(
        offset, limit, pages, "search", search, username
    )

    dynamic_position = request.args.get("offset")
    starting_id = recipes.find({"$text": {"$search": str(search)}}).sort("_id")
    last_id = starting_id[int(dynamic_position)]["_id"]

    sorted_recipes = get_sorted_recipes(
        {"$text": {"$search": str(search)}}, last_id, limit
    )

    return render_template(
        "results.html",
        author=sorted_recipes["author"],
        default=sorted_recipes["default"],
        name=sorted_recipes["name"],
        upvotes=sorted_recipes["upvotes"],
        downvotes=sorted_recipes["downvotes"],
        country=sorted_recipes["country"],
        url_list=url_list,
        pages=pages,
        search=search,
        count=count,
        username=username,
    )


@app.route("/<username>/add_recipe", methods=["GET", "POST"])
def add_recipe(username):

    wtform = ReusableForm(request.form)

    the_recipe_name = mongo.db.recipes.find({}, {"name": 1, "_id": 0})
    name_list = list(the_recipe_name)

    # Obtener la receta con el recipeID más alto
    last_recipe = mongo.db.recipes.find_one(sort=[("recipeID", pymongo.DESCENDING)])

    if last_recipe:
        next_recipe_id = last_recipe["recipeID"] + 1
    else:
        next_recipe_id = 1

    if wtform.validate():

        recipes = mongo.db.recipes

        recipe_data = get_recipe_form_data()

        if search_name(recipe_data["name"], name_list):
            flash("That recipe already exists. Please enter another.")
        else:
            
            recipes.insert_one(
                {
                    "name": recipe_data["name"],
                    "description": recipe_data["description"],
                    "instructions": recipe_data["instructions"],
                    "ingredients": recipe_data["ingredients"],
                    "allergens": recipe_data["allergens"],
                    "country": recipe_data["country"],
                    "author": recipe_data["author"],
                    "upvotes": 0,
                    "downvotes": 0,
                    "recipeID": next_recipe_id,
                }
            )
            return redirect_to_recipes(username)

    return render_template(
        "add_recipe.html", form=wtform, errors=wtform.errors, username=username
    )


@app.route("/<username>/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(username, recipe_id):

    wtform = ReusableForm(request.form)

    the_recipe = mongo.db.recipes.find_one({"recipeID": int(recipe_id)})
    if not the_recipe:
        flash("Recipe not found.")
        return redirect_to_recipes(username)

    if wtform.validate():
        
        recipes = mongo.db.recipes

        recipe_data = get_recipe_form_data()

        recipes.update_one(
            {"recipeID": int(recipe_id)},
            {
                "$set": {
                    "name": recipe_data["name"],
                    "description": recipe_data["description"],
                    "instructions": recipe_data["instructions"],
                    "ingredients": recipe_data["ingredients"],
                    "allergens": recipe_data["allergens"],
                    "country": recipe_data["country"],
                    "author": recipe_data["author"],
                    "upvotes": the_recipe["upvotes"],
                    "downvotes": the_recipe["downvotes"],
                }
            },
        )

        return redirect_to_recipes(username)

    return render_template(
        "edit_recipe.html", recipe=the_recipe, form=wtform, username=username
    )


@app.route("/<username>/delete_recipe/<recipe_id>")
def delete_recipe(username, recipe_id):

    recipes = mongo.db.recipes

    recipe = recipes.find_one({"recipeID": int(recipe_id)})

    if not recipe:
        flash("Recipe not found.")
        return redirect_to_recipes(username)

    mongo.db.votes.delete_many({"recipeID": int(recipe_id)})
    recipes.delete_one({"recipeID": int(recipe_id)})

    return redirect_to_recipes(username)


@app.route("/<username>/view_recipe/<recipe_id>", methods=["GET", "POST"])
def view_recipe(username, recipe_id):

    recipes = mongo.db.recipes

    the_recipe = mongo.db.recipes.find_one({"recipeID": int(recipe_id)})
    if not the_recipe:
        flash("Recipe not found.")
        return redirect_to_recipes(username)

    if request.method == "POST":

        # Verificar si el usuario ya votó esta receta
        existing_vote = mongo.db.votes.find_one(
            {"username": username, "recipeID": int(recipe_id)}
        )

        if existing_vote:
            flash("Ya has votado esta receta.")
            return redirect(
                url_for("view_recipe", username=username, recipe_id=recipe_id)
            )

        # If Upvote
        if request.form["vote"] == "upvote":

            # Increment upvote
            recipes.update_one({"recipeID": int(recipe_id)}, {"$inc": {"upvotes": 1}})

            mongo.db.votes.insert_one(
                {"username": username, "recipeID": int(recipe_id), "vote": "upvote"}
            )

            return redirect(
                url_for("view_recipe", username=username, recipe_id=recipe_id)
            )

        # If Downvote
        elif request.form["vote"] == "downvote":

            # Incrementar downvote
            recipes.update_one({"recipeID": int(recipe_id)}, {"$inc": {"downvotes": 1}})

            mongo.db.votes.insert_one(
                {"username": username, "recipeID": int(recipe_id), "vote": "downvote"}
            )

            return redirect(
                url_for("view_recipe", username=username, recipe_id=recipe_id)
            )

    return render_template("view_recipe.html", recipe=the_recipe, username=username)

@app.route("/api/health", methods=["GET"])
def health():
    try:
        mongo.db.command("ping")

        return jsonify({
            "status": "healthy",
            "database": "connected"
        }), 200

    except Exception:
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected"
        }), 503
    


app.register_blueprint(recipes_bp)

if __name__ == "__main__":
    app.run(
        host=os.getenv("HOST", "127.0.0.1"),
        port=5000
    )