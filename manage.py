import csv
import sys
from db import db
from sqlalchemy import select, update
from app import app
from random import randint
from datetime import datetime as dt
from datetime import timedelta
from sqlalchemy.exc import SQLAlchemyError
from models import Customer, Product, Category, Order, ProductOrder


def drop_tables():
    db.drop_all()
    print("Dropped tables")

def create_tables():
    db.create_all()
    print("Tables created.")
    

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

def create_rand_order():
    # Get random customer
    random_customer = db.session.execute(db.select(Customer).order_by(db.func.random())).scalar()
    
    random_time = dt.now() - timedelta(days=randint(1,3), hours=randint(0,15), minutes=randint(0,30))
    
    # Create new order
    new_order = Order(customer_id=random_customer.id, created=random_time)
    db.session.add(new_order)
    db.session.flush()  
    
    # Get random products
    num_prods = randint(4, 6)
    random_prods = db.session.execute(db.select(Product).order_by(db.func.random()).limit(num_prods)).scalars().all()
    
    # Create product orders
    for product in random_prods:
        quantity = randint(1, 5) 
        product_order = ProductOrder(
            product_id= product.id,
            order_id= new_order.id,
            qty = quantity
        )
        db.session.add(product_order)
    db.session.commit()
    
    print(f"Created order {new_order} for customer {random_customer.name} with {num_prods} products")
    return new_order

def complete_order(id):
    try:
        # Find the order to calculate the estimate
        order = db.session.get(Order, id)
        
        if not order:
            return False, "Order not found"
        elif order:
            for item in order.product_order:  
                product = item.product
                if item.qty > product.qty:
                    return False, f'{product.name} does not have enough quantity ({product.qty})'
                   
                else:
                    db.session.execute(update(Product).where(Product.id == product.id).values(
                        qty = product.qty - item.qty
                    ))

        estimated_amount = order.estimate()
        stmt = update(Order).where(Order.id == id).values(
            completed=dt.now(),
            amount=estimated_amount
        )
        db.session.execute(stmt)
        db.session.commit() 
        
        return True, "Order completed successfully"
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return False, f"Database error: {str(e)}"
    

                
#Start session code
if __name__ == "__main__":
    with app.app_context():
        if 'start' in sys.argv:
            create_tables()
            import_data()
        elif 'drop' in sys.argv:
            drop_tables()
        elif 'get_products' in sys.argv:
            get_products()
        elif 'no_stock' in sys.argv:
            no_stock()
        elif "customer" in sys.argv:
            get_customer()
        elif "random" in sys.argv:
            create_rand_order()
