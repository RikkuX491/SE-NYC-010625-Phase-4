from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

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
    name = db.Column(db.String)

    # Deliverable # 3 solution code
    reviews = db.relationship('Review', back_populates='hotel', cascade='all')
    customers = association_proxy('reviews', 'customer', creator=lambda c: Review(customer=c))

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)

    # Deliverable # 4 solution code
    reviews = db.relationship('Review', back_populates='customer', cascade='all')
    hotels = association_proxy('reviews', 'hotel', creator=lambda h: Review(hotel=h))

# Deliverable # 1 solution code
class Review(db.Model, SerializerMixin):
    
    # Deliverable # 2 solution code
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    text = db.Column(db.String)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    hotel = db.relationship('Hotel', back_populates='reviews')
    customer = db.relationship('Customer', back_populates='reviews')