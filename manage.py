import csv
import sys
from model import Product,Base,Customer,Category
from db import db
from sqlalchemy import select
from app import app


#Make the table
def create_tables():
    Base.metadata.create_all(db.engine)
    
#Remove table
def drop_tables():
    Base.metadata.drop_all(db.engine)

    

def import_data():
    with open ("products.csv" , "r") as fp:
        reader = csv.DictReader(fp)
       #Filter category             
        for info in reader:
            possible_category = db.session.execute(select(Category).where(Category.name == info["category"])).scalar()        
            if not possible_category:
                category_obj = Category(name=info['category'])
                db.session.add(category_obj)
            else:
                category_obj = possible_category
            db.session.add(Product(qty=info['available'], 
                                price=info['price'], 
                                name=info['name'], 
                                category=category_obj))
        db.session.commit()
    with open("customers.csv","r") as fp:
        reader = csv.DictReader(fp)
        for info in reader:
            db.session.add(Customer(name=info['name'], phone=info['phone']))
        db.session.commit()


def get_products():
    statement = select(Product)
    results = db.session.execute(statement)
    #Allowing either name or object
    inquiry = input("Object?(Y/N)")
    if inquiry == "Y":
        for prod in results.scalars():
            print(prod)
    else:
        for prod in results.scalars():
            print(prod.name)

def no_stock():
    statement = select(Product).where(Product.qty < 1)
    results = db.session.execute(statement)
    #Allowing either name or object
    inquiry = input("Object?(Y/N)")
    if inquiry == "Y":
        for prod in results.scalars():
            print(prod)
    else:
        for prod in results.scalars():
            print(prod.name)

def get_customer():
    inquiry = input("What is the name? ")
    statement = select(Customer).where(Customer.name.ilike(inquiry))
    results = db.session.execute(statement)
    inquiry = input("Object?(Y/N)")
    if inquiry == "Y":
        for cus in results.scalars():
            print(cus)
    else:
        for cus in results.scalars():
            print(cus.name)



                
#Start session code
if __name__ == "__main__":
    with app.app_context():
        if 'start' in sys.argv:
            drop_tables()
            create_tables()
            import_data()
        elif 'get_products' in sys.argv:
            get_products()
        elif 'no_stock' in sys.argv:
            no_stock()
        elif "customer" in sys.argv:
            get_customer()
'''     elif "products_by_cat" in sys.argv:
            get_category()
        elif "gen_cus" in sys.argv:
            rand_customer()
'''


'''
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
'''