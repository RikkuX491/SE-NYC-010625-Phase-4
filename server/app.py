#!/usr/bin/env python3
import ipdb

from flask import Flask, make_response, request, session
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS

# Imports the Bcrypt class from the flask_bcrypt package
from flask_bcrypt import Bcrypt

from models import db, Hotel, User, Review

app = Flask(__name__)
app.secret_key = b'`j\xf4\xc4:c\xb1*\xd5\xac\xdfq \xf1q\x82'

# configure a database connection to the local file examples.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotels.db'

# disable modification tracking to use less memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# CORS(app)

# create a Migrate object to manage schema modifications
migrate = Migrate(app, db)

# initialize the Flask application to use the database
db.init_app(app)

# Creates a new instance of the Bcrypt class, passing in the Flask app as an argument into the Bcrypt class constructor. We will use Bcrypt to encrypt our passwords
bcrypt = Bcrypt(app)

api = Api(app)

class AllHotels(Resource):

    def get(self):
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
        except TypeError as te:
            response_body = {
                "error": str(te)
            }
            return make_response(response_body, 422)
        except ValueError as ve:
            response_body = {
                "error": str(ve)
            }
            return make_response(response_body, 422)
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
            response_body = hotel.to_dict(rules=('-reviews.hotel', '-reviews.user'))

            # Add in the association proxy data (The hotel's users) while removing duplicate user data for the hotel's users
            response_body['users'] = [user.to_dict(only=('id', 'first_name', 'last_name', 'username', 'type')) for user in list(set(hotel.users))]
            
            return make_response(response_body, 200)
        
        else:
            response_body = {
                'error': "Hotel Not Found"
            }
            return make_response(response_body, 404)
        
    def patch(self, id):
            hotel = db.session.get(Hotel, id)
            user_id = session.get('user_id')
            user = db.session.get(User, user_id)

            if hotel:
                try:
                    if (user and user.type == "admin"):
                        for attr in request.json:
                            setattr(hotel, attr, request.json[attr])
                        
                        db.session.commit()    
                        response_body = hotel.to_dict(only=('id', 'name', 'image'))
                        return make_response(response_body, 200)
                    
                    else:
                        # raise Exception("Only admins can update hotels!")
                        response_body = {
                            "error": "Only admins can update hotels!"
                        }
                        return make_response(response_body, 401)
                
                except TypeError as te:
                    response_body = {
                        "error": str(te)
                    }
                    return make_response(response_body, 422)
                
                except ValueError as ve:
                    response_body = {
                        "error": str(ve)
                    }
                    return make_response(response_body, 422)
                
                # except Exception as e:
                #     response_body = {
                #         "error": str(e)
                #     }
                #     return make_response(response_body, 401)
                
                except:
                    response_body = {
                        "error": "Hotel must have a name and image, and the hotel name cannot be the same name as any other hotel!"
                    }
                    return make_response(response_body, 422)

            else:
                response_body = {
                    'error': "Hotel Not Found"
                }
                return make_response(response_body, 404)
        
    def delete(self, id):
        # Get the user id data from the session
        user_id = session.get('user_id')

        # Find the user by their user id obtained from the session
        user = db.session.get(User, user_id)

        if not (user and user.type == 'admin'):
            response_body = {
                "error": "Only admins can delete hotels!"
            }
            return make_response(response_body, 401)
        
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

class AllUsers(Resource):

    def get(self):
        users = User.query.all()
        user_list_with_dictionaries = [user.to_dict(only=('id', 'first_name', 'last_name', 'username', 'type')) for user in users]
        return make_response(user_list_with_dictionaries, 200)
    
    # def post(self):
    #     try:
    #         new_user = User(first_name=request.json.get('first_name'), last_name=request.json.get('last_name'), username=request.json.get('username'), password_hash=request.json.get('password'), type='customer')
    #         db.session.add(new_user)
    #         db.session.commit()
    #         response_body = new_user.to_dict(only=('id', 'first_name', 'last_name', 'username', 'type'))
    #         return make_response(response_body, 201)
    #     except:
    #         response_body = {
    #             "error": "Username might already exist. User type can only be either customer or admin. User's first name and last name cannot be the same, and first name and last name must be at least 3 characters long! User must have a username and password!"
    #         }
    #         return make_response(response_body, 400)
    
api.add_resource(AllUsers, '/users')

class UserByID(Resource):

    def get(self, id):
        user = db.session.get(User, id)

        if user:
            response_body = user.to_dict(rules=('-reviews.hotel', '-reviews.user', '-password_hash'))

            # Add in the association proxy data (The user's hotels) while removing duplicate hotel data for the user's hotels
            response_body['hotels'] = [hotel.to_dict(only=('id', 'name', 'image')) for hotel in list(set(user.hotels))]

            return make_response(response_body, 200)
        
        else:
            response_body = {
                'error': "User Not Found"
            }
            return make_response(response_body, 404)
        
    def patch(self, id):
        user = db.session.get(User, id)

        if user:
            try:
                for attr in request.json:
                    setattr(user, attr, request.json[attr])
                
                db.session.commit()
                response_body = user.to_dict(only=('id', 'first_name', 'last_name', 'username', 'type'))
                return make_response(response_body, 200)
            except:
                response_body = {
                    "error": "User's first name and last name cannot be the same, and first name and last name must be at least 3 characters long! User must have a username and password!"
                }
                return make_response(response_body, 400)
        
        else:
            response_body = {
                'error': "User Not Found"
            }
            return make_response(response_body, 404)
         
    def delete(self, id):
        user = db.session.get(User, id)

        if user:
            db.session.delete(user)
            db.session.commit()
            response_body = {}
            return make_response(response_body, 204)
        
        else:
            response_body = {
                'error': "User Not Found"
            }
            return make_response(response_body, 404)

api.add_resource(UserByID, '/users/<int:id>')

class AllReviews(Resource):
    
    def get(self):
        reviews = Review.query.all()
        review_list_with_dictionaries = [review.to_dict(rules=('-hotel.reviews', '-user.reviews', '-user.password_hash')) for review in reviews]
        return make_response(review_list_with_dictionaries, 200)
    
    def post(self):
        try:
            new_review = Review(rating=request.json.get('rating'), text=request.json.get('text'), hotel_id=request.json.get('hotel_id'), user_id=request.json.get('user_id'))
            db.session.add(new_review)
            db.session.commit()
            response_body = new_review.to_dict(rules=('-hotel.reviews', '-user.reviews', '-user.password_hash'))
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
            response_body = review.to_dict(rules=('-hotel.reviews', '-user.reviews', '-user.password_hash'))
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
                response_body = review.to_dict(rules=('-hotel.reviews', '-user.reviews', '-user.password_hash'))
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

class Login(Resource):

    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        
        user = User.query.filter(User.username == username).first()

        if(user and bcrypt.check_password_hash(user.password_hash, password)):
            session['user_id'] = user.id
            response_body = user.to_dict(rules=('-reviews.hotel.reviews', '-reviews.user', '-password_hash'))

            # Add in the association proxy data (The user's hotels) while removing duplicate hotel data for the user's hotels
            response_body['hotels'] = [hotel.to_dict(only=('id', 'name', 'image')) for hotel in list(set(user.hotels))]

            return make_response(response_body, 201)
        else:
            response_body = {
                "error": "Invalid username or password!"
            }
            return make_response(response_body, 401)
    
api.add_resource(Login, '/login')

class CheckSession(Resource):

    def get(self):
        user = db.session.get(User, session.get('user_id'))

        if(user):
            response_body = user.to_dict(rules=('-reviews.hotel.reviews', '-reviews.user', '-password_hash'))

            # Add in the association proxy data (The user's hotels) while removing duplicate hotel data for the user's hotels
            response_body['hotels'] = [hotel.to_dict(only=('id', 'name', 'image')) for hotel in list(set(user.hotels))]

            return make_response(response_body, 200)
        else:
            response_body = {
                "error": "Please Log In!"
            }
            return make_response(response_body, 401)

api.add_resource(CheckSession, '/check_session')

class Logout(Resource):
    
    def delete(self):
        if(session.get('user_id')):
            del(session['user_id'])

        response_body = {}
        return make_response(response_body, 204)
    
api.add_resource(Logout, '/logout')

class Signup(Resource):
    def post(self):
        first_name_data = request.json.get('first_name')
        last_name_data = request.json.get('last_name')
        username_data = request.json.get('username')
        password_data = request.json.get('password')

        pw_hash_value = bcrypt.generate_password_hash(password_data).decode('utf-8')

        try:
            new_user = User(first_name=first_name_data, last_name=last_name_data, username=username_data, password_hash=pw_hash_value, type='customer')
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            response_body = new_user.to_dict(only=('id', 'first_name', 'last_name', 'username', 'type'))
            return make_response(response_body, 201)
        except ValueError as ve:
            response_body = {
                "error": str(ve)
            }
            return make_response(response_body, 422)
        except:
            response_body = {
                "error": "Username might already exist. User's first name and last name cannot be the same! User must have a username and password!"
            }
            return make_response(response_body, 422)

api.add_resource(Signup, '/signup')

if __name__ == "__main__":
    app.run(port=7777, debug=True)