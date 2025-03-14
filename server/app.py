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

class AllHotels(Resource):
    def get(self):
        hotels = Hotel.query.all()
        response_body = [hotel.to_dict(only=('id', 'name')) for hotel in hotels]
        return make_response(response_body, 200)
    
    def post(self):
        hotel_name = request.json.get('name')
        new_hotel = Hotel(name=hotel_name)
        db.session.add(new_hotel)
        db.session.commit()
        response_body = new_hotel.to_dict(rules=('-reviews',))
        return make_response(response_body, 201)
    
api.add_resource(AllHotels, '/hotels')

class HotelByID(Resource):
    def get(self, id):
        hotel = db.session.get(Hotel, id)

        if hotel:
            response_body = hotel.to_dict(rules=('-reviews.hotel', '-reviews.customer'))

            # Add in the association proxy data (The hotel's customers)
            response_body['customers'] = [customer.to_dict(only=('id', 'first_name', 'last_name')) for customer in hotel.customers]

            return make_response(response_body, 200)
        
        else:
            response_body = {
                "error": "Hotel Not Found"
            }
            return make_response(response_body, 404)
        
    def patch(self, id):
        hotel = db.session.get(Hotel, id)

        if hotel:
            for attr in request.json:
                setattr(hotel, attr, request.json.get(attr))
            db.session.commit()
            response_body = hotel.to_dict(rules=('-reviews',))
            return make_response(response_body, 200)

        else:
            response_body = {
                "error": "Hotel Not Found"
            }
            return make_response(response_body, 404)
        
    def delete(self, id):
        hotel = db.session.get(Hotel, id)

        if hotel:
            db.session.delete(hotel)
            db.session.commit()
            return make_response({}, 204)
        
        else:
            response_body = {
                "error": "Hotel Not Found"
            }
            return make_response(response_body, 404)
        
api.add_resource(HotelByID, '/hotels/<int:id>')

class AllCustomers(Resource):
    def get(self):
        customers = Customer.query.all()
        customer_list_with_dictionaries = [customer.to_dict(only=('id', 'first_name', 'last_name')) for customer in customers]
        return make_response(customer_list_with_dictionaries, 200)

    def post(self):
        customer_first_name = request.json.get('first_name')
        customer_last_name = request.json.get('last_name')
        new_customer = Customer(first_name=customer_first_name, last_name=customer_last_name)
        db.session.add(new_customer)
        db.session.commit()
        response_body = new_customer.to_dict(rules=('-reviews',))
        return make_response(response_body, 201)
    
api.add_resource(AllCustomers, '/customers')

class CustomerByID(Resource):
    def get(self, id):
        customer = db.session.get(Customer, id)

        if customer:
            response_body = customer.to_dict(rules=('-reviews.hotel', '-reviews.customer'))

            # Add in the association proxy data (The customer's hotels)
            response_body['hotels'] = [hotel.to_dict(only=('id', 'name')) for hotel in customer.hotels]
            
            return make_response(response_body, 200)
        
        else:
            response_body = {
                "error": "Customer Not Found"
            }
            return make_response(response_body, 404)
        
    def patch(self, id):
        customer = db.session.get(Customer, id)

        if customer:
            for attr in request.json:
                setattr(customer, attr, request.json.get(attr))
            db.session.commit()
            response_body = customer.to_dict(rules=('-reviews',))
            return make_response(response_body, 200)
        
        else:
            response_body = {
                "error": "Customer Not Found"
            }
            return make_response(response_body, 404)
        
    def delete(self, id):
        customer = db.session.get(Customer, id)

        if customer:
            db.session.delete(customer)
            db.session.commit()
            return make_response({}, 204)

        else:
            response_body = {
                "error": "Customer Not Found"
            }
            return make_response(response_body, 404)
        
api.add_resource(CustomerByID, '/customers/<int:id>')

class AllReviews(Resource):
    def get(self):
        reviews = Review.query.all()
        review_list_with_dictionaries = [review.to_dict(rules=('-hotel.reviews', '-customer.reviews')) for review in reviews]
        return make_response(review_list_with_dictionaries, 200)

    def post(self):
        review_rating = request.json.get('rating')
        review_text = request.json.get('text')
        review_hotel_id = request.json.get('hotel_id')
        review_customer_id = request.json.get('customer_id')
        new_review = Review(rating=review_rating, text=review_text, hotel_id=review_hotel_id, customer_id=review_customer_id)
        db.session.add(new_review)
        db.session.commit()
        response_body = new_review.to_dict(rules=('-hotel.reviews', '-customer.reviews'))
        return make_response(response_body, 201)

api.add_resource(AllReviews, '/reviews')

class ReviewByID(Resource):
    def get(self, id):
        review = db.session.get(Review, id)

        if review:
            response_body = review.to_dict(rules=('-hotel.reviews', '-customer.reviews'))
            return make_response(response_body, 200)

        else:
            response_body = {
                "error": "Review Not Found"
            }
            return make_response(response_body, 404)

    def patch(self, id):
        review = db.session.get(Review, id)

        if review:
            for attr in request.json:
                setattr(review, attr, request.json.get(attr))
            db.session.commit()
            response_body = review.to_dict(rules=('-hotel.reviews', '-customer.reviews'))
            return make_response(response_body, 200)

        else:
            response_body = {
                "error": "Review Not Found"
            }
            return make_response(response_body, 404)

    def delete(self, id):
        review = db.session.get(Review, id)

        if review:
            db.session.delete(review)
            db.session.commit()
            return make_response({}, 204)

        else:
            response_body = {
                "error": "Review Not Found"
            }
            return make_response(response_body, 404)

api.add_resource(ReviewByID, '/reviews/<int:id>')

if __name__ == "__main__":
    app.run(port=7777, debug=True)