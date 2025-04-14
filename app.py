from flask import Flask, render_template, redirect, url_for, request
from pathlib import Path
from db import db
from sqlalchemy.orm import mapped_column, relationship
from model import Product, Category, ProductOrder, Order, Customer
from routes.api import api_bp



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///store.db"
app.instance_path = Path(" ").resolve()
db.init_app(app)


app.register_blueprint(api_bp, url_prefix="/api")




'''routes'''
@app.route("/")
def home():
    return render_template("home.html")

'''Products'''
@app.route("/products")
def show_products():
    products = db.session.execute(db.select(Product)).scalars()
    return render_template("products.html", data = products)

'''Categories'''
@app.route("/categories")
def show_categories():
    categories = db.session.execute(db.select(Category)).scalars()
    return render_template("categories.html", data = categories)

@app.route("/categories/<string:category_name>")
def category_products(category_name):
    products = db.session.execute(db.select(Product).where(Product.category.has(Category.name == category_name))).scalars()
    return render_template("products.html", category=category_name, data=products)


'''Customers'''
@app.route("/customers")
def show_customers():
    customers = db.session.execute(db.select(Customer)).scalars()
    return render_template("customers.html", data = customers )

@app.route("/customers/<int:id>")
def customer_detail(id):
    customer = db.session.execute(db.select(Customer).where(Customer.id == id)).scalar()
    return render_template("customer.html", data=customer)

'''Orders'''
@app.route("/orders")
def show_orders():
    orders = db.session.execute(db.select(Order)).scalars()
    return render_template("orders.html", data = orders)

@app.route("/order/<int:id>")
def order_detail(id):
    order = db.session.execute(db.select(Order).where(Order.id == id)).scalar()
    return render_template("order.html", data = order)

@app.route("/order/<int:id>/complete", methods=['GET', 'POST'])
def complete_order_view(id):
    order = db.session.get(Order, id)
    
    if not order:
        return render_template("error.html", message="Order not found"), 404

    result, message = order.complete()
    if not result:
        return render_template("error.html", message=message), 400

    db.session.commit()
    return redirect(url_for('order_detail', id=id))





'''
@app.route("/order/<int:id>/complete", methods=['GET', 'POST'])
def complete_order_view(id):
    order = db.session.execute(db.select(Order).where(Order.id == id)).scalar()
    if not order:
        return render_template("error.html", message="Order not found"), 404

    result, message = order.complete()
    if not result:
        return render_template("error.html", message=message), 400

    db.session.commit()
    return redirect(url_for('order_detail', id=id))
'''

'''    else:
        order = db.session.execute(db.select(Order).where(Order.id == id)).scalar()
        result, message = order.complete()
        if result == False:
            return redirect(url_for('error_page', message=message))
        db.session.commit()
        return redirect(url_for('order_detail', id=id)) 
'''    

'''else:    
        from manage import complete_order
        result, message =  complete_order(id)
        if result == False:
            return redirect(url_for('error_page', message=message))
       
        return redirect(url_for('order_detail', id=id)) 
'''

@app.route("/error")
def error_page():
    data = request.args.get('message', 'An unknown error occurred')
    return render_template("error.html", data=data)
    
'''
will run the flask web application, in debug mode, that listens on port 8888
listens on local interfaces, access via localhost or 127.0.0.1 
'''

if __name__ == "__main__":
    app.run(debug=True, port=8888)
