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

# Deliverable # 1 solution code
@app.route('/hotels', methods=['GET', "POST"])
def all_hotels():
    # Deliverable # 2 solution code
    if request.method == 'GET':
        hotels = Hotel.query.all()
        response_body = [hotel.to_dict(only=('id', 'name')) for hotel in hotels]
        return make_response(response_body, 200)
    elif request.method == 'POST':
        new_hotel = Hotel(name=request.json.get('name'))
        db.session.add(new_hotel)
        db.session.commit()
        response_body = new_hotel.to_dict(rules=('-reviews',))
        return make_response(response_body, 201)

# Deliverable # 3 solution code
@app.route('/hotels/<int:id>', methods=["GET", "PATCH", "DELETE"])
def hotel_by_id(id):
    hotel = db.session.get(Hotel, id)

    if hotel:
        # Deliverable # 4 solution code
        if request.method == 'GET':
            response_body = hotel.to_dict(rules=('-reviews.hotel', '-reviews.customer'))
            response_body['customers'] = [customer.to_dict(only=('id', 'first_name', 'last_name')) for customer in hotel.customers]
            return make_response(response_body, 200)
        elif request.method == 'PATCH':
            json_data = request.json
            for key in json_data:
                setattr(hotel, key, json_data[key])
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

# Deliverable # 5 solution code
@app.route('/customers', methods=['GET', 'POST'])
def all_customers():
    # Deliverable # 6 solution code
    if request.method == 'GET':
        customers = Customer.query.all()
        customer_list_with_dictionaries = [customer.to_dict(only=('id', 'first_name', 'last_name')) for customer in customers]
        return make_response(customer_list_with_dictionaries, 200)
    elif request.method == 'POST':
        json_data = request.json
        new_customer = Customer(first_name=json_data.get('first_name'), last_name=json_data.get('last_name'))
        db.session.add(new_customer)
        db.session.commit()
        response_body = new_customer.to_dict(rules=('-reviews',))
        return make_response(response_body, 201)

# Deliverable # 7 solution code
@app.route('/customers/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def customer_by_id(id):
    customer = db.session.get(Customer, id)

    if customer:
        # Deliverable # 8 solution code
        if request.method == 'GET':
            response_body = customer.to_dict(rules=('-reviews.hotel', '-reviews.customer'))
            response_body['hotels'] = [hotel.to_dict(only=('id', 'name')) for hotel in customer.hotels]
            return make_response(response_body, 200)
        elif request.method == 'PATCH':
            json_data = request.json
            for key in json_data:
                setattr(customer, key, json_data[key])
            db.session.commit()
            response_body = customer.to_dict(rules=('-reviews',))
            return make_response(response_body, 200)
        elif request.method == 'DELETE':
            db.session.delete(customer)
            db.session.commit()
            return make_response({}, 204)
    else:
        response_body = {
            "error": "Customer Not Found"
        }
        return make_response(response_body, 404)

# Deliverable # 9 solution code
@app.route('/reviews', methods=['GET', 'POST'])
def all_reviews():
    # Deliverable # 10 solution code
    if request.method == 'GET':
        reviews = Review.query.all()
        review_list_with_dictionaries = [review.to_dict(rules=('-hotel.reviews', '-customer.reviews')) for review in reviews]
        return make_response(review_list_with_dictionaries, 200)
    elif request.method == 'POST':
        json_data = request.json
        new_review = Review(rating=json_data.get('rating'), text=json_data.get('text'), hotel_id=json_data.get('hotel_id'), customer_id=json_data.get('customer_id'))
        db.session.add(new_review)
        db.session.commit()
        response_body = new_review.to_dict(rules=('-hotel.reviews', '-customer.reviews'))
        return make_response(response_body, 201)

# Deliverable # 11 solution code
@app.route('/reviews/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def review_by_id(id):
    review = db.session.get(Review, id)

    if review:
        # Deliverable # 12 solution code
        if request.method == 'GET':
            response_body = review.to_dict(rules=('-hotel.reviews', '-customer.reviews'))
            return make_response(response_body, 200)
        elif request.method == 'PATCH':
            json_data = request.json
            for key in json_data:
                setattr(review, key, json_data[key])
            db.session.commit()
            response_body = review.to_dict(rules=('-hotel.reviews', '-customer.reviews'))
            return make_response(response_body, 200)
        elif request.method == 'DELETE':
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