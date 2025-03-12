#!/usr/bin/env python3
import ipdb

from flask import Flask, make_response, request
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
def all_hotels():
    # This code should only be executed if the request method is "GET"
    hotels = Hotel.query.all()
    response_body = [hotel.to_dict(only=('id', 'name')) for hotel in hotels]
    return make_response(response_body, 200)

@app.route('/hotels/<int:id>')
def hotel_by_id(id):
    hotel = db.session.get(Hotel, id)

    if hotel:
        # This code should only be executed if the request method is "GET"
        response_body = hotel.to_dict(rules=('-reviews.hotel', '-reviews.customer'))
        response_body['customers'] = [customer.to_dict(only=('id', 'first_name', 'last_name')) for customer in hotel.customers]
        return make_response(response_body, 200)
    else:
        response_body = {
            "error": "Hotel Not Found"
        }
        return make_response(response_body, 404)

@app.route('/customers')
def all_customers():
    # This code should only be executed if the request method is "GET"
    customers = Customer.query.all()
    customer_list_with_dictionaries = [customer.to_dict(only=('id', 'first_name', 'last_name')) for customer in customers]
    return make_response(customer_list_with_dictionaries, 200)

@app.route('/customers/<int:id>')
def customer_by_id(id):
    customer = db.session.get(Customer, id)

    if customer:
        # This code should only be executed if the request method is "GET"
        response_body = customer.to_dict(rules=('-reviews.hotel', '-reviews.customer'))
        response_body['hotels'] = [hotel.to_dict(only=('id', 'name')) for hotel in customer.hotels]
        return make_response(response_body, 200)
    else:
        response_body = {
            "error": "Customer Not Found"
        }
        return make_response(response_body, 200)

@app.route('/reviews')
def all_reviews():
    # This code should only be executed if the request method is "GET"
    reviews = Review.query.all()
    review_list_with_dictionaries = [review.to_dict(rules=('-hotel.reviews', '-customer.reviews')) for review in reviews]
    return make_response(review_list_with_dictionaries, 200)

@app.route('/reviews/<int:id>')
def review_by_id(id):
    review = db.session.get(Review, id)

    if review:
        # This code should only be executed if the request method is "GET"
        response_body = review.to_dict(rules=('-hotel.reviews', '-customer.reviews'))
        return make_response(response_body, 200)
    else:
        response_body = {
            "error": "Review Not Found"
        }
        return make_response(response_body, 404)

if __name__ == "__main__":
    app.run(port=7777, debug=True)