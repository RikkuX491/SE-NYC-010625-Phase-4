#!/usr/bin/env python3

from app import app
from models import db, Hotel, Customer, Review

with app.app_context():
    Hotel.query.delete()
    Customer.query.delete()
    Review.query.delete()

    hotel1 = Hotel(name="Marriott", image="/images/marriott.png")
    hotel2 = Hotel(name="Waikiki Resort", image="/images/waikiki-resort.png")
    hotel3 = Hotel(name="Bahamas Resort", image="/images/bahamas-resort.png")

    customer1 = Customer(first_name="Alice", last_name="Baker", username="alicebaker123")
    customer2 = Customer(first_name="Bob", last_name="Carris", username="bobcarris456")
    customer3 = Customer(first_name="Cynthia", last_name="Dawson", username="cynthiadawson789")

    review1 = Review(rating=5, text="Best hotel ever!", hotel_id=1, customer_id=1)
    review2 = Review(rating=4, text="Amazing!", hotel_id=1, customer_id=2)
    review3 = Review(rating=4, text="Great!", hotel_id=2, customer_id=1)
    review4 = Review(rating=3, text="Not as good as the first time I was there.", hotel_id=1, customer_id=1)
    
    db.session.add_all([hotel1, hotel2, hotel3])
    db.session.add_all([customer1, customer2, customer3])
    db.session.add_all([review1, review2, review3, review4])

    db.session.commit()
    print("🌱 Hotels, Customers, and Reviews successfully seeded! 🌱")