from app import app
from unittest.mock import patch

def test_index_get():
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.get("/")

        assert response.status_code == 200


def test_index_contains_title():
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.get("/")

        assert b"Digital Cookbook" in response.data


def test_invalid_route():
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.get("/ruta_que_no_existe")

        assert response.status_code == 404

@patch("routes.recipes.get_sorted_recipes")
@patch("routes.recipes.generate_pagination_links")
@patch("routes.recipes.get_pages")
@patch("routes.recipes.mongo")
def test_recipes_route(
    mock_mongo,
    mock_pages,
    mock_links,
    mock_sorted,
):
    app.config["TESTING"] = True

    # Simular recetas en la base de datos
    mock_mongo.db.recipes.find.return_value.sort.return_value = [
        {"_id": 1},
        {"_id": 2},
    ]

    mock_pages.return_value = 1
    mock_links.return_value = ["/Martin/recipes?limit=10&offset=0"]

    mock_sorted.return_value = {
        "author": [],
        "default": [
            {
                "name": "Pizza",
                "upvotes": 5,
                "downvotes": 1,
                "country": "Mexico",
                "author": "Martin",
                "recipeID": 1,
            }
        ],
        "name": [],
        "upvotes": [],
        "downvotes": [],
        "country": [],
    }

    with app.test_client() as client:
        response = client.get("/Martin/recipes?limit=10&offset=0")

        assert response.status_code == 200


@patch("routes.recipes.get_sorted_recipes")
@patch("routes.recipes.generate_pagination_links")
@patch("routes.recipes.get_pages")
@patch("routes.recipes.mongo")
def test_my_recipes_route(
    mock_mongo,
    mock_pages,
    mock_links,
    mock_sorted,
):
    app.config["TESTING"] = True

    mock_mongo.db.recipes.find.return_value.sort.return_value = [
        {"_id": 1},
    ]

    mock_pages.return_value = 1
    mock_links.return_value = ["/Martin/my_recipes?limit=10&offset=0"]

    mock_sorted.return_value = {
        "author": [],
        "default": [
            {
                "name": "Pizza",
                "upvotes": 5,
                "downvotes": 1,
                "country": "Mexico",
                "author": "Martin",
                "recipeID": 1,
            }
        ],
        "name": [],
        "upvotes": [],
        "downvotes": [],
        "country": [],
    }

    with app.test_client() as client:
        response = client.get("/Martin/my_recipes?limit=10&offset=0")

        assert response.status_code == 200


@patch("app.mongo")
def test_view_recipe_route(mock_mongo):
    app.config["TESTING"] = True

    # Simular una receta encontrada
    mock_mongo.db.recipes.find_one.return_value = {
        "recipeID": 1,
        "name": "Pizza",
        "upvotes": 5,
        "downvotes": 1,
        "country": "Mexico",
        "author": "Martin",
        "ingredients": ["Queso"],
        "instructions": ["Hornear"],
    }

    with app.test_client() as client:
        response = client.get("/Martin/view_recipe/1")

        assert response.status_code == 200
        assert b"Pizza" in response.data

def test_search_route():
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.get("/Martin/search")

        assert response.status_code == 200
        assert b"Search" in response.data


@patch("app.redirect_to_recipes")
@patch("app.search_name")
@patch("app.get_recipe_form_data")
@patch("app.mongo")
def test_add_recipe_post(
    mock_mongo,
    mock_get_recipe_form_data,
    mock_search_name,
    mock_redirect,
):
    app.config["TESTING"] = True

    # Simular recetas existentes
    mock_mongo.db.recipes.find.return_value = []
    mock_mongo.db.recipes.find_one.return_value = {"recipeID": 5}

    # La receta NO existe
    mock_search_name.return_value = False

    # Datos simulados del formulario
    mock_get_recipe_form_data.return_value = {
        "name": "Pizza",
        "description": "Muy rica",
        "instructions": "Hornear",
        "ingredients": "Queso",
        "allergens": "Lactosa",
        "country": "Italia",
        "author": "Martin",
    }

    # Simular la redirección
    mock_redirect.return_value = "OK"

    with app.test_client() as client:
        response = client.post(
            "/Martin/add_recipe",
            data={
                "name": "Pizza",
                "description": "Muy rica",
                "author": "Martin",
                "instruction1": "Hornear",
                "ingredient1": "Queso",
                "country": "Mexico",
            },
        )

    assert response.status_code == 200
    mock_mongo.db.recipes.insert_one.assert_called_once()

@patch("app.mongo")
def test_health_route(mock_mongo):
    app.config["TESTING"] = True

    # Simular que MongoDB responde correctamente al ping
    mock_mongo.db.command.return_value = {"ok": 1}

    with app.test_client() as client:
        response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"
    assert response.json["database"] == "connected"


@patch("app.mongo")
def test_search_no_results(mock_mongo):
    app.config["TESTING"] = True

    # Simular que la búsqueda no encuentra recetas
    mock_mongo.db.recipes.count_documents.return_value = 0

    with app.test_client() as client:
        response = client.get(
            "/Martin/search/Pizza?limit=10&offset=0"
        )

    assert response.status_code == 200