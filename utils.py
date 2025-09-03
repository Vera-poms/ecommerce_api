def replace_product_id(prod):
    prod["id"] = str(prod["_id"])
    del prod["_id"]
    return prod
def replace_user_id(user):
    user["id"] = str(user["_id"])
    del user["_id"]
    return user