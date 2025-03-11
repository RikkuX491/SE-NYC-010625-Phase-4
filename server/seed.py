#!/usr/bin/env python3

from app import app
from models import db, Hotel, Customer

with app.app_context():
    Hotel.query.delete()
    Customer.query.delete()

    hotel1 = Hotel(name="Marriott")
    hotel2 = Hotel(name="Hampton Inn")
    hotel3 = Hotel(name="The Chanler at Cliff Walk")

    customer1 = Customer(first_name="Alice", last_name="Baker")
    customer2 = Customer(first_name="Bob", last_name="Willis")
    customer3 = Customer(first_name="Cindy", last_name="Davidson")
    
    db.session.add_all([hotel1, hotel2, hotel3])
    db.session.add_all([customer1, customer2, customer3])

    db.session.commit()
    print("🌱 Hotels and Customers successfully seeded! 🌱")