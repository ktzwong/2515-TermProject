from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Float, DateTime
from db import db
from datetime import datetime

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