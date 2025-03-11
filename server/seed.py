#!/usr/bin/env python3

from app import app
from models import db, Hotel

with app.app_context():
    # Write code to seed hotels into the hotels table in the database

    # Delete all hotels from the hotels table before seeding the hotels table
    Hotel.query.delete()

    hotel1 = Hotel(name="The Lodge At Woodloch")
    hotel2 = Hotel(name="Crystal Springs Resort")
    hotel3 = Hotel(name="Hammock Cove Resort")
    hotel4 = Hotel(name="Agalia Luxury Hotel")

    db.session.add_all([hotel1, hotel2, hotel3, hotel4])
    db.session.commit()

    print("🌱 Hotels successfully seeded! 🌱")