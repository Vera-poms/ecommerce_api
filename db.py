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
users_db = mongo_client["db_db"]

# Pick a connection to operate on
products_collection = ecommerce_db["products"]
users_collection = users_db["users"]

if products_collection.count_documents({}) == 0:
    products_collection.insert_many(products)
    print("inserted")
else:
    print("already exist")

if users_collection.count_documents({}) == 0:
    users_collection.insert_many(user_details)
    print("Users details inserted successfully")
else:
    print("Details already exist")