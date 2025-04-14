from db import db
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, Float, String, ForeignKey

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
    