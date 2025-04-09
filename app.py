from flask import Flask, render_template
from pathlib import Path
from db import db
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Float



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///store.db"
app.instance_path = Path(" ").resolve()
db.init_app(app)


'''
Classes
'''
class Product(db.Model):
    __tablename__ = "products"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    qty = mapped_column(Integer, default=0)
    price = mapped_column(Float)
    category_id = mapped_column(Integer, ForeignKey("Categories.id"))
    category = relationship("Category", back_populates="products")



class Customer(db.Model):
    __tablename__ = "Customers"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    phone = mapped_column(String)



class Category(db.Model):
    __tablename__ = "Categories"
    
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    products = relationship("Product", back_populates="category")




'''routes'''
@app.route("/")
def home():
    return render_template("home.html")

'''Products'''
@app.route("/Products")
def show_products():
    products = db.session.execute(db.select(Product)).scalars()
    return render_template("products.html", data = products)

'''Categories'''
@app.route("/Categories")
def show_categories():
    categories = db.session.execute(db.select(Category)).scalars()
    return render_template("categories.html", data = categories)

@app.route("/categories/<string:category_name>")
def category_products(category_name):
    products = db.session.execute(db.select(Product).where(Product.category.has(Category.name == category_name))).scalars()
    return render_template("products.html", category=category_name, data=products)


'''Customers'''
@app.route("/Customers")
def show_customers():
    customers = db.session.execute(db.select(Customer)).scalars()
    return render_template("Customers.html", data = customers )

@app.route("/Customers/<int:id>")
def customer_detail(id):
    customer = db.session.execute(db.select(Customer).where(Customer.id ==id)).scalar()
    return render_template("Customer.html", data=customer)



'''
will run the flask web application, in debug mode, that listens on port 8888
listens on local interfaces, access via localhost or 127.0.0.1 
'''

if __name__ == "__main__":
    app.run(debug=True, port=8888)
