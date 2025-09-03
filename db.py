from pymongo import MongoClient
import os
from dotenv import load_dotenv
from products import products

load_dotenv()

#Connect to Mongo Atlas Cluster
mongo_client = MongoClient(os.getenv("MONGO_URI"))

# Access database
ecommerce_db = mongo_client["ecommerce_db"]

# Pick a connection to operate on
products_collection = ecommerce_db["products"]

if products_collection.count_documents({}) == 0:
    products_collection.insert_many(products)
    print("inserted")
else:
    print("already exist")