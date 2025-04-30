from app import app
from db import db
from models import Customer
import sys


def create_customer():
    Kevin = Customer(name="Kevin Wong",phone="123-456-7890")
    tim = Customer(name="Time",phone="123-456-7899")
    

    db.session.add(Kevin,tim)
    db.session.commit()
    print('Added customers')

if __name__ == "__main__":
    with app.app_context():
         if 'Customer' in sys.argv:
             create_customer()
              