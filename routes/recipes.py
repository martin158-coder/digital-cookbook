from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash,
    url_for,
)

from extensions import mongo
import pymongo

from forms import ReusableForm, Search, Username
from utils import (
    get_pages,
    generate_pagination_links,
    search_name,
    get_sorted_recipes,
    get_recipe_form_data,
    redirect_to_recipes,
)

recipes_bp = Blueprint("recipes", __name__)


@recipes_bp.route("/", methods=["GET", "POST"])
def index():
    wtform = Username(request.form)

    if wtform.validate():
        username = request.form["username"]

        return redirect(
            url_for(
                "recipes.recipes",
                username=username,
                limit=10,
                offset=0,
            )
        )

    return render_template(
        "index.html",
        form=wtform,
        errors=wtform.errors,
    )


@recipes_bp.route("/<username>/recipes")
def recipes(username):

    recipes = mongo.db.recipes
    all_recipes = recipes.find().sort("_id", 1)
    recipe_list = list(all_recipes)

    offset = 0
    limit = int(request.args.get("limit"))

    count = len(recipe_list)

    if count == 0:
        return render_template(
            "recipes.html",
            author=[],
            default=[],
            name=[],
            upvotes=[],
            downvotes=[],
            country=[],
            url_list=[],
            pages=0,
            username=username,
        )

    pages = get_pages(count, limit)
    url_list = generate_pagination_links(
        offset, limit, pages, "recipes", "null", username
    )

    starting_position = int(request.args.get("offset", 0))

    if starting_position >= len(recipe_list):
        starting_position = 0

    last_id = recipe_list[starting_position]["_id"]

    sorted_recipes = get_sorted_recipes({}, last_id, limit)

    return render_template(
        "recipes.html",
        author=sorted_recipes["author"],
        default=sorted_recipes["default"],
        name=sorted_recipes["name"],
        upvotes=sorted_recipes["upvotes"],
        downvotes=sorted_recipes["downvotes"],
        country=sorted_recipes["country"],
        url_list=url_list,
        pages=pages,
        username=username,
    )


@recipes_bp.route("/<username>/my_recipes")
def my_recipes(username):

    recipes = mongo.db.recipes

    all_recipes = list(
        recipes.find({"author": username}).sort("_id", 1)
    )

    limit = int(request.args.get("limit", 10))
    offset = int(request.args.get("offset", 0))

    count = len(all_recipes)

    if count == 0:
        return render_template(
            "recipes.html",
            author=[],
            default=[],
            name=[],
            upvotes=[],
            downvotes=[],
            country=[],
            url_list=[],
            pages=0,
            username=username,
        )

    pages = get_pages(count, limit)

    url_list = generate_pagination_links(
        0,
        limit,
        pages,
        "my_recipes",
        "null",
        username,
    )

    last_id = all_recipes[offset]["_id"]

    sorted_recipes = get_sorted_recipes(
        {"author": username},
        last_id,
        limit,
    )

    return render_template(
        "recipes.html",
        author=sorted_recipes["author"],
        default=sorted_recipes["default"],
        name=sorted_recipes["name"],
        upvotes=sorted_recipes["upvotes"],
        downvotes=sorted_recipes["downvotes"],
        country=sorted_recipes["country"],
        url_list=url_list,
        pages=pages,
        username=username,
    )