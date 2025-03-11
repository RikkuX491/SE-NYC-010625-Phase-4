#!/usr/bin/env python3

import ipdb

# make_response() is a function from the flask library that returns a Response object. We can include data (a list, dictionary, or string) and a status code and pass these in as arguments to the make_response() function. We can return a Response object from a Flask view.
from flask import Flask, make_response

# Migrate is a class from the flask_migrate library that creates a Migrate object that can be used to connect Flask-Migrate to your Flask app and database.
from flask_migrate import Migrate

# db is a variable containing an instance of the SQLAlchemy class (Flask SQLAlchemy extension)
from models import db, Hotel

app = Flask(__name__)

# configure a database connection to the local file hotels.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotels.db'

# disable modification tracking to use less memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create a Migrate object to manage schema modifications
migrate = Migrate(app, db)

# initialize the Flask application to use the database
db.init_app(app)

# Deliverable # 3 solution code
@app.route('/hotels')
def get_hotels():
    hotels = Hotel.query.all()
    response_body = [hotel.to_dict() for hotel in hotels]
    return make_response(response_body, 200)

# Deliverable # 4 solution code
@app.route('/hotels/<int:id>')
def hotel_by_id(id):
    hotel = db.session.get(Hotel, id)

    if hotel:
        response_body = hotel.to_dict()
        return make_response(response_body, 200)
    else:
        response_body = {
            "error": "Hotel Not Found!"
        }
        return make_response(response_body, 404)

if __name__ == "__main__":
    app.run(port=7777, debug=True)