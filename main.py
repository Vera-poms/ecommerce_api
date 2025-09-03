from fastapi import FastAPI
from bson.objectid import ObjectId
from db import products_collection, users_collection
from pydantic import BaseModel
from utils import replace_product_id, replace_user_id


class UserModel(BaseModel):
    email: str
    password: str

class ProductModel(BaseModel):
    product_id: str
    name: str
    description: str
    price: float
    image: str


app = FastAPI()

ecommerce_user_db = []

@app.get("/")
def get_home():
    return {"message": "Welcome to our ecommerce site"}

# List some products
@app.get("/products")
def get_products():
    all_products = products_collection.find().to_list()
    return {"products": list(map(replace_product_id, all_products))}

@app.post("/products")
def post_products(product: ProductModel):
    products_collection.insert_one(product.model_dump())
    return {"message": "Products added successfully"}

@app.get("/products/{product_id}")
def get_product_by_id(product_id):
    product = products_collection.find_one({"_id": ObjectId(product_id)})
    return {"product": replace_product_id(product)}

@app.get("/users")
def get_users():
    users = users_collection.find().to_list()
    return {"users": list(map(replace_user_id, users))}

@app.post("/register")
def register_user(user: UserModel):
    users_collection.insert_one(user.model_dump())
    return {"message": "Registered successfully"}

@app.post("/login")
def login_user(user: UserModel):
    users_collection.find_one(user.model_dump())







#     if (users_collection.email == users_collection.email) and (users_collection.password == users_collection.password):
#         return {"message": "Login successfull"}
#     elif(users_collection.email != users_collection.email):
#         return {"message": "Invalid email"}
    
# @app.post("/cart")
# def cart():
#     return {}

# @app.get("/cart/{user_id}")
# def get_cart():
#     return {}