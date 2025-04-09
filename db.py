from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from flask_sqlalchemy import SQLAlchemy



class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

engine = create_engine("sqlite:///store.db", echo=True)
session = sessionmaker(bind=engine)

