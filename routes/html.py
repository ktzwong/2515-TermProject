from flask import Blueprint, render_template, request, redirect, url_for
from db import db
from models import Product, Category, Customer, Order




html_routes = Blueprint("html_routes", __name__)

@html_routes.route("/")
def home():
    return render_template("home.html")

# Products
@html_routes.route("/products")
def show_products():
    products = db.session.execute(db.select(Product)).scalars()
    return render_template("products.html", data=products)

# Categories
@html_routes.route("/categories")
def show_categories():
    categories = db.session.execute(db.select(Category)).scalars()
    return render_template("categories.html", data=categories)

@html_routes.route("/categories/<string:category_name>")
def category_products(category_name):
    products = db.session.execute(
        db.select(Product).where(Product.category.has(Category.name == category_name))
    ).scalars()
    return render_template("products.html", category=category_name, data=products)

# Customers
@html_routes.route("/customers")
def show_customers():
    customers = db.session.execute(db.select(Customer)).scalars()
    return render_template("customers.html", data=customers)

@html_routes.route("/customers/<int:id>")
def customer_detail(id):
    customer = db.session.execute(db.select(Customer).where(Customer.id == id)).scalar()
    return render_template("customer.html", data=customer)

# Orders
@html_routes.route("/orders")
def show_orders():
    orders = db.session.execute(db.select(Order)).scalars()
    return render_template("orders.html", data=orders)

@html_routes.route("/order/<int:id>")
def order_detail(id):
    order = db.session.execute(db.select(Order).where(Order.id == id)).scalar()
    return render_template("order.html", data=order)

@html_routes.route("/order/<int:id>/complete", methods=['GET', 'POST'])
def complete_order_view(id):
    order = db.session.get(Order, id)

    if not order:
        return render_template("error.html", message="Order not found"), 404

    result, message = order.complete()
    if not result:
        return render_template("error.html", message=message), 400

    db.session.commit()
    return redirect(url_for('html_routes.order_detail', id=id))

# Error
@html_routes.route("/error")
def error_page():
    data = request.args.get('message', 'An unknown error occurred')
    return render_template("error.html", data=data)