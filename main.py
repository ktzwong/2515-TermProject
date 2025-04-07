import csv
import sys
from model import Product,Base,Customer,Category
from db import Session, engine
from sqlalchemy import select

#Make the table
def create():
    Base.metadata.create_all(engine)
    
#Remove table
def drop():
    Base.metadata.drop_all(engine)

    
def importdata():
    session = Session()
    with open ("products.csv" , "r") as fp:
        reader = csv.DictReader(fp)
       #Filter category             
        for info in reader:
            possible_category = session.execute(select(Category).where(Category.name == info["category"])).scalar()        
            if not possible_category:
                category_obj = Category(name=info['category'])
                session.add(category_obj)
            else:
                category_obj = possible_category
            session.add(Product(qty=info['available'], 
                                price=info['price'], 
                                name=info['name'], 
                                category=category_obj))
        session.commit()
    with open("customers.csv","r") as fp:
        reader = csv.DictReader(fp)
        for info in reader:
            session.add(Customer(name=info['name'], phone=info['phone']))
        session.commit()


def get_products():
    session = Session()
    statement = select(Product)
    results = session.execute(statement)
    #Allowing either name or object
    inquiry = input("Object?(Y/N)")
    if inquiry == "Y":
        for prod in results.scalars():
            print(prod)
    else:
        for prod in results.scalars():
            print(prod.name)

def no_stock():
    session = Session()
    statement = select(Product).where(Product.inventory < 1)
    results = session.execute(statement)
    #Allowing either name or object
    inquiry = input("Object?(Y/N)")
    if inquiry == "Y":
        for prod in results.scalars():
            print(prod)
    else:
        for prod in results.scalars():
            print(prod.name)

def get_customer():
    session = Session()
    inquiry = input("What is the name? ")
    statement = select(Customer).where(Customer.name.ilike(inquiry))
    results = session.execute(statement)
    inquiry = input("Object?(Y/N)")
    if inquiry == "Y":
        for cus in results.scalars():
            print(cus)
    else:
        for cus in results.scalars():
            print(cus.name)



                
#Start session code
if __name__ == "__main__":
    if 'start' in sys.argv:
        drop()
        create()
        importdata()
    elif 'get_products' in sys.argv:
        get_products()
    elif 'no_stock' in sys.argv:
        no_stock()
    elif "customer" in sys.argv:
        get_customer()
    print("Done")