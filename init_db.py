from pymongo import MongoClient

client = MongoClient("mongodb+srv://martinbv3125_db_user:5dg87iKRBQ5Jbplf@cluster0.3zjbwai.mongodb.net/digital_cookbook?appName=Cluster0")
db = client.digital_cookbook

db.recipes.create_index([
    ("name", "text"),
    ("description", "text"),
    ("ingredients", "text")
])

print("Índice creado correctamente.")