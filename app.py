from flask import Flask
from pathlib import Path
from db import db
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship
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


@app.route("/")
def home():
    return "<h1>Welcome to the Food Store!</h1>"



'''
will run the flask web application, in debug mode, that listens on port 8888
listens on local interfaces, access via localhost or 127.0.0.1 
'''
if __name__ == "__main__":
    app.run(debug=True, port=8888)
