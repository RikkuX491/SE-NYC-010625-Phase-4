#!/usr/bin/env python3
import ipdb

from flask import Flask, make_response, request, session
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS

from models import db, Hotel, Customer, Review

import os

app = Flask(__name__)

# Here's the secret key value that will be used for the session object
# app.secret_key = b'Xu\xcd\xd4\xda\xdf\xc9>\xf1:\x91\xfaz\x80\xeb\x91'

# Here's a potential more best practice approach for storing the secret key value
app.secret_key = os.urandom(16)

# configure a database connection to the local file examples.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotels.db'

# disable modification tracking to use less memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# CORS(app)

# create a Migrate object to manage schema modifications
migrate = Migrate(app, db)

# initialize the Flask application to use the database
db.init_app(app)

api = Api(app)

class AllHotels(Resource):

    def get(self):
        # ipdb.set_trace()
        hotels = Hotel.query.all()
        response_body = [hotel.to_dict(only=('id', 'name', 'image')) for hotel in hotels]
        return make_response(response_body, 200)
    
    def post(self):
        try:
            new_hotel = Hotel(name=request.json.get('name'), image=request.json.get('image'))
            db.session.add(new_hotel)
            db.session.commit()
            response_body = new_hotel.to_dict(only=('id', 'name', 'image'))
            return make_response(response_body, 201)
        except:
            response_body = {
                "error": "Hotel must have a name and image, and the hotel name cannot be the same name as any other hotel!"
            }
            return make_response(response_body, 400)
    
api.add_resource(AllHotels, '/hotels')

class HotelByID(Resource):

    def get(self, id):
        hotel = db.session.get(Hotel, id)

        if hotel:
            response_body = hotel.to_dict(rules=('-reviews.hotel', '-reviews.customer'))

            # Add in the association proxy data (The hotel's customers)
            response_body['customers'] = [customer.to_dict(only=('id', 'first_name', 'last_name', 'username')) for customer in hotel.customers]
            
            return make_response(response_body, 200)
        
        else:
            response_body = {
                'error': "Hotel Not Found"
            }
            return make_response(response_body, 404)
        
    def patch(self, id):
            hotel = db.session.get(Hotel, id)

            if hotel:
                try:
                    for attr in request.json:
                        setattr(hotel, attr, request.json[attr])
                    
                    db.session.commit()    
                    response_body = hotel.to_dict(only=('id', 'name', 'image'))
                    return make_response(response_body, 200)
                
                except:
                    response_body = {
                        "error": "Hotel must have a name and image, and the hotel name cannot be the same name as any other hotel!"
                    }
                    return make_response(response_body, 400)

            else:
                response_body = {
                    'error': "Hotel Not Found"
                }
                return make_response(response_body, 404)
        
    def delete(self, id):
        hotel = db.session.get(Hotel, id)

        if hotel:
            db.session.delete(hotel)
            db.session.commit()
            response_body = {}
            return make_response(response_body, 204)
        
        else:
            response_body = {
                'error': "Hotel Not Found"
            }
            return make_response(response_body, 404)
    
api.add_resource(HotelByID, '/hotels/<int:id>')

class AllCustomers(Resource):

    def get(self):
        customers = Customer.query.all()
        customer_list_with_dictionaries = [customer.to_dict(only=('id', 'first_name', 'last_name', 'username')) for customer in customers]
        return make_response(customer_list_with_dictionaries, 200)
    
    def post(self):
        try:
            new_customer = Customer(first_name=request.json.get('first_name'), last_name=request.json.get('last_name'), username=request.json.get('username'))
            db.session.add(new_customer)
            db.session.commit()
            response_body = new_customer.to_dict(only=('id', 'first_name', 'last_name', 'username'))
            return make_response(response_body, 201)
        except:
            response_body = {
                "error": "Customer's first name and last name cannot be the same, and first name and last name must be at least 3 characters long! Customer must have a username!"
            }
            return make_response(response_body, 400)
    
api.add_resource(AllCustomers, '/customers')

class CustomerByID(Resource):

    def get(self, id):
        customer = db.session.get(Customer, id)

        if customer:
            response_body = customer.to_dict(rules=('-reviews.hotel', '-reviews.customer'))

            # Add in the association proxy data (The customer's hotels)
            response_body['hotels'] = [hotel.to_dict(only=('id', 'name', 'image')) for hotel in customer.hotels]

            return make_response(response_body, 200)
        
        else:
            response_body = {
                'error': "Customer Not Found"
            }
            return make_response(response_body, 404)
        
    def patch(self, id):
        customer = db.session.get(Customer, id)

        if customer:
            try:
                for attr in request.json:
                    setattr(customer, attr, request.json[attr])
                
                db.session.commit()
                response_body = customer.to_dict(only=('id', 'first_name', 'last_name', 'username'))
                return make_response(response_body, 200)
            except:
                response_body = {
                    "error": "Customer's first name and last name cannot be the same, and first name and last name must be at least 3 characters long! Customer must have a username!"
                }
                return make_response(response_body, 400)
        
        else:
            response_body = {
                'error': "Customer Not Found"
            }
            return make_response(response_body, 404)
         
    def delete(self, id):
        customer = db.session.get(Customer, id)

        if customer:
            db.session.delete(customer)
            db.session.commit()
            response_body = {}
            return make_response(response_body, 204)
        
        else:
            response_body = {
                'error': "Customer Not Found"
            }
            return make_response(response_body, 404)

api.add_resource(CustomerByID, '/customers/<int:id>')

class AllReviews(Resource):
    
    def get(self):
        reviews = Review.query.all()
        review_list_with_dictionaries = [review.to_dict(rules=('-hotel.reviews', '-customer.reviews')) for review in reviews]
        return make_response(review_list_with_dictionaries, 200)
    
    def post(self):
        try:
            new_review = Review(rating=request.json.get('rating'), text=request.json.get('text'), hotel_id=request.json.get('hotel_id'), customer_id=request.json.get('customer_id'))
            db.session.add(new_review)
            db.session.commit()
            response_body = new_review.to_dict(rules=('-hotel.reviews', '-customer.reviews'))
            return make_response(response_body, 201)
        except ValueError as value_error:
            value_error_string = str(value_error)
            response_body = {
                "error": value_error_string
            }
            return make_response(response_body, 400)
    
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
            try:
                for attr in request.json:
                    setattr(review, attr, request.json.get(attr))
                
                db.session.commit()
                response_body = review.to_dict(rules=('-hotel.reviews', '-customer.reviews'))
                return make_response(response_body, 200)
            
            except ValueError as value_error:
                value_error_string = str(value_error)
                response_body = {
                    "error": value_error_string
                }
                return make_response(response_body, 400)
        
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
            response_body = {}
            return make_response(response_body, 204)
        
        else:
            response_body = {
                "error": "Review Not Found"
            }
            return make_response(response_body, 404)

api.add_resource(ReviewByID, '/reviews/<int:id>')

# Here's the backend portion of our Login feature
class Login(Resource):
    def post(self):
        username_data = request.json.get('username')
        customer = Customer.query.filter(Customer.username == username_data).first()

        if customer:
            session['customer_id'] = customer.id
            response_body = customer.to_dict(rules=('-reviews',))
            return make_response(response_body, 201)

        else:
            response_body = {
                "error": "Unable to login due to invalid username!"
            }
            return make_response(response_body, 401)

api.add_resource(Login, '/login')

class CheckSession(Resource):
    def get(self):
        id = session.get('customer_id')
        customer = db.session.get(Customer, id)

        if customer:
            response_body = customer.to_dict(rules=('-reviews',))
            return make_response(response_body, 200)

        else:
            response_body = {
                "error": "Please log in!"
            }
            return make_response(response_body, 401)

api.add_resource(CheckSession, '/check_session')

class Logout(Resource):
    def delete(self):
        if session.get('customer_id') != None:
            del session['customer_id']
        
        return make_response({}, 204)

api.add_resource(Logout, '/logout')

if __name__ == "__main__":
    app.run(port=7777, debug=True)