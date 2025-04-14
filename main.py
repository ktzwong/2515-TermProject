import csv
import sys
from app import app, db, Product, Customer, Category
from sqlalchemy import select



def create_tables():
    db.drop_all()
    db.create_all()
    print("✅ Tables dropped and created.")


def import_data():
    with open("products.csv", "r") as fp:
        reader = csv.DictReader(fp)
        for info in reader:
            # Check if category exists
            category = db.session.execute(
                select(Category).where(Category.name == info["category"])
            ).scalar()
            if not category:
                category = Category(name=info["category"])
                db.session.add(category)

            # Add product
            product = Product(
                name=info["name"],
                qty=int(info["available"]),
                price=float(info["price"]),
                category=category
            )
            db.session.add(product)

        db.session.commit()
        print(" Products imported.")

    with open("customers.csv", "r") as fp:
        reader = csv.DictReader(fp)
        for info in reader:
            customer = Customer(name=info["name"], phone=info["phone"])
            db.session.add(customer)

        db.session.commit()
        print(" Customers imported.")


def list_products():
    products = db.session.execute(select(Product)).scalars()
    for p in products:
        print(f"{p.name} - {p.qty} in stock")


def out_of_stock():
    products = db.session.execute(
        select(Product).where(Product.qty < 1)
    ).scalars()
    for p in products:
        print(f"{p.name} is out of stock")


def find_customer():
    name = input("Enter customer name: ")
    customers = db.session.execute(
        select(Customer).where(Customer.name.ilike(name))
    ).scalars()
    for c in customers:
        print(f"{c.name} - {c.phone}")


# CLI Entry point
if __name__ == "__main__":
    with app.app_context():
        if 'start' in sys.argv:
            create_tables()
            import_data()
        elif 'get_products' in sys.argv:
            list_products()
        elif 'no_stock' in sys.argv:
            out_of_stock()
        elif "customer" in sys.argv:
            find_customer()
        elif "random" in sys.argv:
            create_rand_order()
        else:
            print("No valid command provided.")