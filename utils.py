import json
import pymongo

from flask import request, redirect, url_for

from extensions import mongo

def get_pages(count, limit):
    #Get Number of Pages to Paginate
    pages = count // limit
    if count % limit > 0:
        if count % limit <= limit:
            pages += 1
            return pages
        else:
            pages += 2
    else:
        return pages

def generate_pagination_links(offset, limit, pages, webpage, search, username):
    #Generates Pagination Links
    if webpage == 'search':
        url_list = ['/' + username + '/' + webpage + '/' + search  + '?limit=' + str(limit) + '&offset=0']
        for i in range(pages):
            url_list.append('/' + username + '/'  + webpage + '/' + search  + '?limit=' + str(limit) + '&offset=' + str(offset + limit))
            offset += limit
    else:
        url_list = ['/'+ username + '/'  + webpage + '?limit=' + str(limit) + '&offset=0']
        for x in range(pages):
            url_list.append('/'+ username + '/'  + webpage  + '?limit=' + str(limit) + '&offset=' + str(offset + limit))
            offset += limit
    return url_list
 
def get_countries():
    #Return a list of countries
    with open('data/countries.json') as j:
        loaded =json.load(j)
        country_list = []
        for i in loaded:
            country_list.append((i['name'], i['name']))
        return country_list

def increment_field(voteType, current):
    # Increment Field
    for x in current:
        if voteType in x:
            return x[voteType] + 1

def search_name(formName, names):
    for name in names:
        if name['name'].title() == formName.title():
            return True

def get_sorted_recipes(base_query, last_id, limit):
    recipes = mongo.db.recipes

    query = {"$and": [{"_id": {"$gte": last_id}}, base_query]}

    return {
        "default": recipes.find(query).sort("_id", 1).limit(limit),
        "country": recipes.find(query).sort([("country", 1), ("name", 1)]).limit(limit),
        "name": recipes.find(query).sort("name", 1).limit(limit),
        "upvotes": recipes.find(query)
        .sort([("upvotes", pymongo.DESCENDING), ("name", 1)])
        .limit(limit),
        "downvotes": recipes.find(query)
        .sort([("downvotes", pymongo.DESCENDING), ("name", 1)])
        .limit(limit),
        "author": recipes.find(query).sort([("author", 1), ("name", 1)]).limit(limit),
    }


def get_recipe_form_data():
    
    instructions = request.form.getlist("instruction2")
    instructions.insert(0, request.form["instruction1"])

    ingredients = request.form.getlist("ingredient2")
    ingredients.insert(0, request.form["ingredient1"])

    allergens = request.form.getlist("allergen2")
    first_allergen = request.form.get("allergen1")

    if first_allergen:
        allergens.insert(0, first_allergen)
        #allergens = [a for a in allergens if a.strip()]

    return {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": instructions,
        "ingredients": ingredients,
        "allergens": allergens,
        "country": request.form["country"],
        "author": request.form["author"],
    }


def redirect_to_recipes(username):
    return redirect(url_for("recipes", username=username, limit=10, offset=0))