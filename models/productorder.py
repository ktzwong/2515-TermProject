from db import db
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, ForeignKey

class ProductOrder(db.Model):
        __tablename__ = "product_order"

        order_id = mapped_column(Integer, ForeignKey("order.id"), primary_key=True)
        product_id = mapped_column(Integer, ForeignKey("product.id"), primary_key=True)
        qty = mapped_column(Integer, default=0)

        product = relationship("Product", back_populates="product_order")
        order = relationship("Order", back_populates="product_order")