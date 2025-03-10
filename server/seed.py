#!/usr/bin/env python3

from app import app
from models import db

with app.app_context():
    # Write code to seed hotels into the hotels table in the database
    print("🌱 Hotels successfully seeded! 🌱")