from fastapi import FastAPI, HTTPException
from bson.objectid import ObjectId
from db import products_collection, users_collection, users_cart
from pydantic import BaseModel, EmailStr
from utils import replace_product_id, replace_user_id, replace_cart_id


class UserModel(BaseModel):
    email: EmailStr
    password: str

class ProductModel(BaseModel):
    name: str
    description: str
    price: float
    image: str

class CartModel(BaseModel):
    user_id: str
    product_id: str
    quantity: int


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
    return {"message": "Product added successfully"}

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
    ecommerce_user_email = users_collection.find_one({"email": user.email})

    if ecommerce_user_email and (ecommerce_user_email["password"] != user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        return {"message": "Login successful"}

    
@app.post("/cart")
def cart(item: CartModel):
    users_cart.insert_one(item.model_dump())
    # cart_item = users_cart.find_one({"product_id": item.product_id})

    # if item.quantity <= 0:
    #     raise HTTPException(status_code=400, detail="Quantity must be at least 1")
    # else:
    return {"message": f"{item.quantity} item(s) added to cart"}

    # return {}

@app.get("/cart/{user_id}")
def get_cart(user_id: str):
    users_cart_items = list(users_cart.find_one({"user_id": ObjectId(user_id)}))

    for item in users_cart_items:
        item["_id"]
    return {"item": list(map(replace_cart_id, users_cart_items))}

# @app.post("checkout/{user_id}")
# def checkout(user_id: UserModel, cart: CartModel):
#     subtotal = cart.price * cart.quantity
#     total = subtotal * 1
#     return {"cart_items": cart, "total": total}