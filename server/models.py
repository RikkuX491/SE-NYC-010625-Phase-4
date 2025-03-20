from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates

# contains definitions of tables and associated schema constructs
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
})

# create the Flask SQLAlchemy extension
db = SQLAlchemy(metadata=metadata)

# define a model class by inheriting from db.Model.
class Hotel(db.Model, SerializerMixin):
    __tablename__ = 'hotels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    image = db.Column(db.String, nullable=False)

    # 1 hotel has many reviews: 1-to-many relationship between hotels and reviews tables
    reviews = db.relationship('Review', back_populates='hotel', cascade='all')

    # hotels and users Many-to-Many relationship: The hotel's users
    users = association_proxy('reviews', 'user', creator = lambda u: Review(user = u))

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    username = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)

    # 1 user has many reviews: 1-to-many relationship between users and reviews tables
    reviews = db.relationship('Review', back_populates='user', cascade='all')

    # hotels and users Many-to-Many relationship: The user's hotels
    hotels = association_proxy('reviews', 'hotel', creator = lambda h: Review(hotel = h))

    __table_args__ = (db.CheckConstraint('first_name != last_name'),)

    @validates('first_name', 'last_name')
    def validate_first_and_last_name(self, attr, value):
        if (not isinstance(value, str)) or len(value) < 3:
            raise ValueError(f"{attr} must be a string that is at least 3 characters long!")
        return value
    
    @validates('type')
    def validate_type(self, column, value):
        if value in ['customer', 'admin']:
            return value
        else:
            raise ValueError(f"{column} must be either customer or admin!")

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    text = db.Column(db.String)

    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # A review belongs to a hotel: 1-to-many relationship between hotels and reviews tables
    hotel = db.relationship('Hotel', back_populates='reviews')

    # A review belongs to a user: 1-to-many relationship between users and reviews tables
    user = db.relationship('User', back_populates='reviews')

    @validates('rating')
    def validate_rating(self, attr, value):
        if not (isinstance(value, int) and 1 <= value <= 5):
            raise ValueError(f"{attr} must be an integer that is between 1 and 5!")
        else:
            return value
        
    @validates('hotel_id', 'user_id')
    def validate_hotel_id_and_customer_id(self, attr, value):
        if not (isinstance(value, int)):
            raise ValueError(f"Review must have a {attr} and {attr} must be an integer!")
        else:
            return value