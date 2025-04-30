from flask import jsonify, Blueprint, request
from db import db
from sqlalchemy import select
from models import Customer, Product, Category, Order, ProductOrder

api_bp = Blueprint("api", __name__)


@api_bp.route("/test")
def example_api():
    return jsonify(["a", {"example": True, "other": "yes"}, ("value", "123")])


@api_bp.route("/products")
def products():
    products = db.session.execute(db.select(Product)).scalars()
    return jsonify([p.to_json() for p in products])

@api_bp.route("/products/<int:id>")
def one_product(id):
    product = db.session.execute(db.select(Product).where(Product.id == id)).scalar()
    return jsonify(product.to_json())

@api_bp.route("/products/<string:name>", methods=["PUT"]) #updating products use PUT
def upate_product(name):
    data = request.json
    product = db.session.execute(db.select(Product).where(Product.name == name)).scalar()
    if product is None:
        return {"message": "Cannot find product"}, 404
    if "price" in data:
        if data["price"] < 0:
             return {"message": "not a valid price"}, 400
        product.price = data["price"]

    if "qty" in data:
        if data["qty"] < 0:
            return {"message": "Cannot update quantity "}, 400
        product.qty = data["qty"]
    db.session.commit()
    return jsonify(product.to_json()), 200



'''Orders'''
@api_bp.route("/orders")
def orders():
    orders = db.session.execute(db.select(Order)).scalars()
    return jsonify([c.to_json() for c in orders])

@api_bp.route("/orders/<int:id>")
def one_order(id):
    order = db.session.execute(db.select(Order).where(Order.id == id)).scalar()
    return jsonify(order.to_json())

@api_bp.route("/orders/<int:id>", methods=["PUT"])
def check_order(id):
    data = request.json
    order = db.session.execute(db.select(Order).where(Order.id == id)).scalar()

    if order is None:
        return {"message": "Cannot find order"}, 404
    if "strategy" not in data:
        return {"message": "no strategy provided"}, 400
    if data["strategy"] not in ["ignore", "adjust", "delete"]:
        return {"message": "strategy not valid"}, 400
    
    if order.completed is not None:
        return {"message": "Order completed"}, 400
    
    if data["strategy"] == "ignore":
        pass
    elif data["strategy"] == "adjust":
        for product in order.product_order:
            if product.qty > product.product.qty:
                product.qty = product.product.qty
    elif data["strategy"] == "delete": 
         for product in order.product_order:
            if product.qty > product.product.qty:
                db.session.delete(product)

    order.complete()
    db.session.commit()
    return jsonify(order.to_json()), 200

'''Create new order'''
@api_bp.route("/orders", methods=["POST"])
def create_order():
    data = request.json
    if "phone" not in data:
        return {"message": "Need phone number"}, 400
    customer = db.session.execute(db.select(Customer).where(Customer.phone == data["phone"])).scalar()
    if customer is None:
          return {"message": "Need customer"}, 400
    
    if "product" not in data:
        return {"message": "not a valid food"}, 400
    
    new_order = Order(customer=customer)
    db.session.add(new_order)
    db.session.flush()  ## needed because we created a empty PK 
    
    for item in data["product"]:
        name, qty = item
        product = db.session.execute(db.select(Product).where(Product.name == name)).scalar()
    
        if product is None:
            return {"message": "Product not found"}, 400

        if qty <= 0:
            return {"message": f"Invalid quantity for '{name}'"}, 400
        
        db.session.add(ProductOrder(order_id=new_order.id,
                                    product_id=product.id,
                                    qty=qty))
    db.session.commit()
    return jsonify(new_order.to_json()), 201
    

'''adding product'''
@api_bp.route("/products", methods=["POST"])
def create_product():
    data = request.json

    if "name" not in data or not data["name"].strip():
        return {"message": "Product name is required"}, 400
    if "price" not in data or data["price"] <= 0:
        return {"message": "Valid product price is required"}, 400
    if "category" not in data or not data["category"].strip():
        return {"message": "Category is required"}, 400

    qty = data.get("qty", 0)
    if not  qty < 0:
        return {"message": "Invalid quantity"}, 400

    category = db.session.execute(
        db.select(Category).where(Category.name == data["category"])
    ).scalar()

    # Create category if it doesn't exist
    if category is None:
        category = Category(name=data["category"])
        db.session.add(category)
        db.session.flush()  # Needed so category.id exists

    # Create and add product
    product = Product(
        name=data["name"].strip(),
        price=data["price"],
        qty=qty,
        category=category
    )
    db.session.add(product)
    db.session.commit()

    return jsonify(product.to_json()), 201  


@api_bp.route("/exam/customers/<int:id>", methods=["PUT"])
def update_customer(id):
    data = request.json
    Customer = db.session.execute(db.select(Customer).where(Customer.id == id)).scalar()
    if Customer is None:
        return {"message": "Cannot find customer"}, 404
    if "money" in data:
        if data["money"] < 0:
                return {"message": "not a valid price"}, 400
        Customer.money = data["money"]

    if "status" in data:
        if data["status"] ==True:
            Customer.status = data["status"]
        else:
            Customer.status = data["status"]
    db.session.commit()
    return jsonify(Customer.to_json()), 200

@api_bp.route("/exam/deliver/<int:id>", methods=["PUT"])
def update_delivery(id):
    data = request.json
    order = db.session.execute(db.select(Order).where(Order.id == id)).scalar()
    if Order is None:
        return {"message": "Cannot find Order"}, 404
    if data["delivery"] == True:
            Customer.delivery = data["delivery"]
    elif "delivery" in data["delivery"] == False:
        

    if "status" in data:
        if data["status"] ==True:
            Customer.status = data["status"]
        else:
            Customer.status = data["status"]
    db.session.commit()
    return jsonify(Customer.to_json()), 200