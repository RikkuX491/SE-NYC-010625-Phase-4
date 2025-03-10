#!/usr/bin/env python3

import ipdb

# make_response() is a function from the flask library that returns a Response object. We can include data (a list, dictionary, or string) and a status code and pass these in as arguments to the make_response() function. We can return a Response object from a Flask view.
from flask import Flask, make_response

# Migrate is a class from the flask_migrate library that creates a Migrate object that can be used to connect Flask-Migrate to your Flask app and database.
from flask_migrate import Migrate

# db is a variable containing an instance of the SQLAlchemy class (Flask SQLAlchemy extension)
from models import db

app = Flask(__name__)

# configure a database connection to the local file hotels.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotels.db'

# disable modification tracking to use less memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create a Migrate object to manage schema modifications
migrate = Migrate(app, db)

# initialize the Flask application to use the database
db.init_app(app)

if __name__ == "__main__":
    app.run(port=7777, debug=True)