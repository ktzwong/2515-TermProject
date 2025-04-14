from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Float, DateTime
from db import db
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Product(db.Model):
    __tablename__ = "product"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String)
    qty = mapped_column(Integer, default=0)
    price = mapped_column(Float)
    category_id = mapped_column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")
    product_order = relationship("ProductOrder", back_populates="product")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "inventory": self.qty,
            "category_id": self.category_id
        }
    

class Customer(db.Model):
    __tablename__ = "customers"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String)
    phone = mapped_column(String)
    order = relationship("Order", back_populates="customer")

#checking for pending orders
    def pending_orders(self):
        pending_orders = []
        for order in self.order:
            if order.completed is None:
                pending_orders.append(order)
        return pending_orders
#getting completed orders
    def completed_orders(self):
        completed_orders = []
        for order in self.order:
            if order.completed is not None:
                completed_orders.append(order)
        return completed_orders

    
class Category(db.Model):
    __tablename__ = "categories"
    
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String)
    products = relationship("Product", back_populates="category")

class ProductOrder(db.Model):
        __tablename__ = "product_order"

        order_id = mapped_column(Integer, ForeignKey("order.id"), primary_key=True)
        product_id = mapped_column(Integer, ForeignKey("product.id"), primary_key=True)
        qty = mapped_column(Integer, default=0)

        product = relationship("Product", back_populates="product_order")
        order = relationship("Order", back_populates="product_order")
        
class Order(db.Model):
        __tablename__ = "order"

        id = mapped_column(Integer, primary_key=True, autoincrement=True)
        customer_id = mapped_column(Integer, ForeignKey("customers.id"))

        created = mapped_column(DateTime, default=datetime.now)
        completed = mapped_column(DateTime, nullable=True)
        amount = mapped_column(Float, nullable=True)

        product_order = relationship("ProductOrder", back_populates="order")
        customer = relationship("Customer", back_populates="order")

        def estimate(self):
            total = 0
            for po in self.product_order:
                one = po.product.price * po.qty
                total = total + one
            return total

        def complete(self):
            for po in self.product_order:
                print(f"{po.product.name} - Ordered: {po.qty}, In Stock: {po.product.qty}")
                if po.qty > po.product.qty:
                    return False, f"{po.product.name} Out of stock"
            for po in self.product_order:
                    po.product.qty -= po.qty

                    self.completed = datetime.now()
                    self.amount = self.estimate()
            return True, f"Sucessfully added."
            
        def to_json(self):
            json = {
                "id": self.id,
                "customer_id": self.customer_id,
                "amount": self.amount,
                "created": self.created,
                "completed_date": self.completed,
            }
            if self.completed is not None:
                json["items"] = [{"item":item.product.name,"price":item.product.price,"quantity":item.qty} for item in self.product_order]
            else:
                json["items"] = [{"item":item.product.name,"quantity":item.qty} for item in self.product_order]
            return json