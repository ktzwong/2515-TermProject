from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Float, DateTime
from db import db
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Product(db.Model):
    __tablename__ = "products"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    qty = mapped_column(Integer, default=0)
    price = mapped_column(Float)
    category_id = mapped_column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")
    product_orders = relationship("ProductOrder", back_populates="product")


class Customer(db.Model):
    __tablename__ = "customers"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    phone = mapped_column(String)
    orders = relationship("Order", back_populates="customer")


class Category(db.Model):
    __tablename__ = "categories"
    
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    products = relationship("Product", back_populates="category")

class ProductOrder(db.Model):
        __tablename__ = "product_order"

        order_id = mapped_column(Integer, ForeignKey("orders.id"), primary_key=True)
        product_id = mapped_column(Integer, ForeignKey("Products.id"), primary_key=True)
        qty = mapped_column(Integer, default=0)
        product = relationship("Product", back_populates="product_order")
        order = relationship("Order", back_populates="product_orders")
        

class Order(db.Model):
        __tablename__ = "product_order"

        id = mapped_column(Integer, primary_key=True)
        customer_id = mapped_column(Integer, ForeignKey("customers.id"), primary_key=True)

        created = mapped_column(DateTime, default=datetime.now)
        completed = mapped_column(DateTime, nullable=True)
        amount = mapped_column(Float, nullable=True)

        product_orders = relationship("ProductOrder", back_populates="order")
        customer = relationship("Customer", back_populates="orders")


