#!/usr/bin/env python3
import ipdb

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Hotel, Customer, Review

app = Flask(__name__)

# configure a database connection to the local file examples.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotels.db'

# disable modification tracking to use less memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create a Migrate object to manage schema modifications
migrate = Migrate(app, db)

# initialize the Flask application to use the database
db.init_app(app)

@app.route('/hotels')
def get_hotels():
    response_body = [hotel.to_dict(rules=('-reviews',)) for hotel in Hotel.query.all()]
    return make_response(response_body, 200)

@app.route('/hotels/<int:id>')
def hotel_by_id(id):
    hotel = db.session.get(Hotel, id)

    if hotel:
        response_body = hotel.to_dict(rules=('-reviews.hotel', '-reviews.customer'))
        # response_body = hotel.to_dict(rules=('-reviews.hotel', '-reviews.customer.reviews'))
        response_body['customers'] = [customer.to_dict(rules=('-reviews',)) for customer in set(hotel.customers)]
        return make_response(response_body, 200)
    else:
        response_body = {
            "error": "Hotel Not Found!"
        }
        return make_response(response_body, 404)

@app.route('/reviews')
def get_reviews():
    reviews = Review.query.all()
    response_body = [review.to_dict(rules=('-hotel.reviews', '-customer.reviews')) for review in reviews]
    return make_response(response_body, 200)

if __name__ == "__main__":
    app.run(port=7777, debug=True)