#!/usr/bin/env python3
import ipdb

# request is an instance from the LocalProxy class. We can access information about the method and json data from request
from flask import Flask, make_response, request

# Migrate is a class from the flask_migrate library that creates a Migrate object that can be used to connect Flask-Migrate to your Flask app and database
from flask_migrate import Migrate

# Api and Resource are classes from the flask_restful library. The Api class can be used to create an Api instance which can be used to connect a class inheriting from the Resource class to a route
from flask_restful import Api, Resource

# db is a variable containing an instance of the SQLAlchemy class (Flask SQLAlchemy extension). Hotel, Customer, and Review are models that are imported from the models.py file
from models import db, Hotel, Customer, Review

# app contains our Flask app, which is an instance of the Flask class
app = Flask(__name__)

# configure a database connection to the local file examples.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotels.db'

# disable modification tracking to use less memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create a Migrate object to manage schema modifications
migrate = Migrate(app, db)

# initialize the Flask application to use the database
db.init_app(app)

# create an instance of the Api class - this Api instance can be used to connect a class inheriting from the Resource class to a route
api = Api(app)

@app.route('/hotels', methods=["GET", "POST"])
def all_hotels():
    if request.method == 'GET':
        hotels = Hotel.query.all()
        response_body = [hotel.to_dict(only=('id', 'name')) for hotel in hotels]
        return make_response(response_body, 200)
    
    elif request.method == 'POST':
        hotel_name = request.json.get('name')
        new_hotel = Hotel(name=hotel_name)
        db.session.add(new_hotel)
        db.session.commit()
        response_body = new_hotel.to_dict(rules=('-reviews',))
        return make_response(response_body, 201)

@app.route('/hotels/<int:id>', methods=["GET", "PATCH", "DELETE"])
def hotel_by_id(id):
    hotel = db.session.get(Hotel, id)

    if hotel:
        if request.method == "GET":
            response_body = hotel.to_dict(rules=('-reviews.hotel', '-reviews.customer'))
            response_body['customers'] = [customer.to_dict(only=('id', 'first_name', 'last_name')) for customer in hotel.customers]
            return make_response(response_body, 200)
        
        elif request.method == 'PATCH':
            for attr in request.json:
                setattr(hotel, attr, request.json.get(attr))
            db.session.commit()
            response_body = hotel.to_dict(rules=('-reviews',))
            return make_response(response_body, 200)
          
        elif request.method == 'DELETE':
            db.session.delete(hotel)
            db.session.commit()
            return make_response({}, 204)

    else:
        response_body = {
            "error": "Hotel Not Found"
        }
        return make_response(response_body, 404)

@app.route('/customers', methods=["GET", "POST"])
def all_customers():
    if request.method == "GET":
        customers = Customer.query.all()
        customer_list_with_dictionaries = [customer.to_dict(only=('id', 'first_name', 'last_name')) for customer in customers]
        return make_response(customer_list_with_dictionaries, 200)
    
    elif request.method == "POST":
        customer_first_name = request.json.get('first_name')
        customer_last_name = request.json.get('last_name')
        new_customer = Customer(first_name=customer_first_name, last_name=customer_last_name)
        db.session.add(new_customer)
        db.session.commit()
        response_body = new_customer.to_dict(rules=('-reviews',))
        return make_response(response_body, 201)

@app.route('/customers/<int:id>', methods=["GET", "PATCH", "DELETE"])
def customer_by_id(id):
    customer = db.session.get(Customer, id)

    if customer:
        if request.method == "GET":
            response_body = customer.to_dict(rules=('-reviews.hotel', '-reviews.customer'))
            response_body['hotels'] = [hotel.to_dict(only=('id', 'name')) for hotel in customer.hotels]
            return make_response(response_body, 200)
        
        elif request.method == "PATCH":
            for attr in request.json:
                setattr(customer, attr, request.json.get(attr))
            db.session.commit()
            response_body = customer.to_dict(rules=('-reviews',))
            return make_response(response_body, 200)
        
        elif request.method == "DELETE":
            db.session.delete(customer)
            db.session.commit()
            return make_response({}, 204)
        
    else:
        response_body = {
            "error": "Customer Not Found"
        }
        return make_response(response_body, 404)

@app.route('/reviews', methods=["GET", "POST"])
def all_reviews():
    if request.method == "GET":
        reviews = Review.query.all()
        review_list_with_dictionaries = [review.to_dict(rules=('-hotel.reviews', '-customer.reviews')) for review in reviews]
        return make_response(review_list_with_dictionaries, 200)
    
    elif request.method == "POST":
        review_rating = request.json.get('rating')
        review_text = request.json.get('text')
        review_hotel_id = request.json.get('hotel_id')
        review_customer_id = request.json.get('customer_id')
        new_review = Review(rating=review_rating, text=review_text, hotel_id=review_hotel_id, customer_id=review_customer_id)
        db.session.add(new_review)
        db.session.commit()
        response_body = new_review.to_dict(rules=('-hotel.reviews', '-customer.reviews'))
        return make_response(response_body, 201)

@app.route('/reviews/<int:id>', methods=["GET", "PATCH", "DELETE"])
def review_by_id(id):
    review = db.session.get(Review, id)

    if review:
        if request.method == "GET":
            response_body = review.to_dict(rules=('-hotel.reviews', '-customer.reviews'))
            return make_response(response_body, 200)
        
        elif request.method == "PATCH":
            for attr in request.json:
                setattr(review, attr, request.json.get(attr))
            db.session.commit()
            response_body = review.to_dict(rules=('-hotel.reviews', '-customer.reviews'))
            return make_response(response_body, 200)
        
        elif request.method == "DELETE":
            db.session.delete(review)
            db.session.commit()
            return make_response({}, 204)
        
    else:
        response_body = {
            "error": "Review Not Found"
        }
        return make_response(response_body, 404)

if __name__ == "__main__":
    app.run(port=7777, debug=True)