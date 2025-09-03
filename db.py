from pymongo import MongoClient
import os
from dotenv import load_dotenv
from products import products
from users import user_details

load_dotenv()

#Connect to Mongo Atlas Cluster
mongo_client = MongoClient(os.getenv("MONGO_URI"))


# Access database
ecommerce_db = mongo_client["ecommerce_db"]
users_db = mongo_client["ecommerce_db"]
cart_db = mongo_client["ecommerce_db"]

# Pick a connection to operate on
products_collection = ecommerce_db["products"]
users_collection = ecommerce_db["users"]
users_cart = ecommerce_db["cart"]

if products_collection.count_documents({}) == 0:
    products_collection.insert_many(products)


if users_collection.count_documents({}) == 0:
    users_collection.insert_many(user_details)

