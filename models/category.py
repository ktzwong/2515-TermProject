from db import db
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String

class Category(db.Model):
    __tablename__ = "categories"
    
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String)
    products = relationship("Product", back_populates="category")