from fastapi import FastAPI
from bson.objectid import ObjectId
from db import products_collection

app = FastAPI()

@app.get("/")
def get_home():
    return {"message": "Welcome to our ecommerce site"}

# List some products
@app.get("/products")
def get_products():
    all_products = products_collection.find()
    return {"products": all_products}

@app.get("/products/{product_id}")
def get_product_by_id(product_id):
    product = products_collection.find_one({"_id": ObjectId(product_id)})
    return {"product": product}


# @app.post("/register")
# def post_user():
#     user_details = {
#         "user_name": "name",
#         "password": "user_password",
#     }