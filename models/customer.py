from db import db
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String

class Customer(db.Model):
    __tablename__ = "customers"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String)
    phone = mapped_column(String,unique=True)
    order = relationship("Order", back_populates="customer")
    money = mapped_column(Integer,default=0)
    status = mapped_column(String,default="regular")

    
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

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "status":self.status,
            "money":self.money,
            "pending_orders": [o.to_json() for o in self.pending_orders()],
            "completed_orders": [o.to_json() for o in self.completed_orders()]
        }
    