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
def get_product_by_id(product_id: str):
    try:
        product_obj_id = ObjectId(product_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid product id format")
    
    product = products_collection.find_one({"_id": product_obj_id})
    if product:
        return {"product": replace_product_id(product)}
    
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/users")
def get_users():
    users = users_collection.find().to_list()
    return {"users": list(map(replace_user_id, users))}

@app.post("/register")
def register_user(user: UserModel):
    ecommerce_user_email = users_collection.find_one({"email": user.email})
    ecommerce_user_password = users_collection.find_one({"password": user.password})

    if ecommerce_user_email or ecommerce_user_password:
        raise HTTPException(status_code=409, detail="Email or password already in use")
    else:
        users_collection.insert_one(user.model_dump())
        return {"message": "Registered successfully"}

@app.post("/login")
def login_user(user: UserModel):
    ecommerce_user_email = users_collection.find_one({"email": user.email})

    if ecommerce_user_email and (ecommerce_user_email["password"] != user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    elif not ecommerce_user_email:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        return {"message": "Login successful"}

    
@app.post("/cart")
def cart(item: CartModel):
    get_product_by_id(item)
    users_cart.insert_one(item.model_dump())

    if item.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be at least 1")
    
    return {"message": f"{item.quantity} item(s) added to cart"}


@app.get("/cart/{user_id}")
def get_cart(user_id: str):
    users_cart_items = list(users_cart.find({"user_id": user_id}))
    items = [replace_cart_id(item) for item in users_cart_items]
        
    return {"cart_items": items}

@app.post("/checkout/{user_id}")
def checkout(user_id: str, product: ProductModel):
    cart_items = users_cart.find({"user_id": str(ObjectId(user_id))}).to_list()

    if not cart_items:
        raise HTTPException(status_code=404, detail="No items in cart")
    
    detailed_cart = []
    subtotal = 0
    total = 0
    
    for item in cart_items:

        product = products_collection.find_one({"_id": ObjectId(item["product_id"])})
        if not product: 
            continue

        price = float(item["price"])
        quantity = int(item["quantity"])
        subtotal += price * quantity
        total += subtotal 

        detailed_cart.append({
            "product_id": str(product["_id"]),
            "name": product["name"],
            "price": price,
            "quantity": quantity
        })


    return {
            "cart_items": detailed_cart, 
            "subtotal": subtotal,
            "total": total
            }