from flask import jsonify, Blueprint, request
from db import db
from model import Product, Order, Category, Customer, ProductOrder
from sqlalchemy import select

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
