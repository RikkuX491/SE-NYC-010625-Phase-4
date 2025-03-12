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

    # serialize_only = ('id', 'name')
    # serialize_rules = ('-reviews',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # The 1-to-many relationship data - 1 Hotel has many Reviews
    reviews = db.relationship('Review', back_populates='hotel', cascade='all')

    # The many-to-many relationship data - The 1 Hotel has many Customers side of the relationship
    customers = association_proxy('reviews', 'customer', creator=lambda c: Review(customer=c))

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)

    # The 1-to-many relationship data - 1 Customer has many Reviews
    reviews = db.relationship('Review', back_populates='customer', cascade='all')

    # The many-to-many relationship data - The 1 Customer has many Hotels side of the relationship    
    hotels = association_proxy('reviews', 'hotel', creator=lambda h: Review(hotel=h))

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    text = db.Column(db.String)

    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))

    hotel = db.relationship('Hotel', back_populates='reviews')
    customer = db.relationship('Customer', back_populates='reviews')