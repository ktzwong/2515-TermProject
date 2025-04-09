from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Float


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    qty = mapped_column(Integer, default=0)
    price = mapped_column(Float)  
    category_id = mapped_column(Integer, ForeignKey("Categories.id"))  
    category = relationship("Category", back_populates="products")     


class Customer(Base):
    __tablename__ = "Customers"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    phone = mapped_column(String)



class Category(Base):
    __tablename__ = "Categories"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    products = relationship("Product", back_populates="category")




'''  data = results-scalars()'''

