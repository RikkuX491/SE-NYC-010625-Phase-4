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

# define a model class by inheriting from db.Model. SerializerMixin allows for calling the to_dict() method on an instance which will return a dictionary with keys are value pairs for each db.Column. db.relationships are also serialized
class Hotel(db.Model, SerializerMixin):
    __tablename__ = 'hotels'

    id = db.Column(db.Integer, primary_key=True)

    # Deliverable # 1 solution code
    name = db.Column(db.String, unique=True, nullable=False)

    # 1 hotel has many reviews: 1-to-many relationship between hotels and reviews tables
    reviews = db.relationship('Review', back_populates='hotel', cascade='all')

    # hotels and customers Many-to-Many relationship: The hotel's customers
    customers = association_proxy('reviews', 'customer', creator = lambda c: Review(customer = c))

    # Deliverable # 2 solution code
    @validates('name')
    def validate_name(self, column_name, value):
        if (type(value) == str) and (5 <= len(value) <= 50):
            return value
        else:
            raise Exception

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)

    # Deliverable # 3 solution code
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)

    # Deliverable # 4 solution code
    __table_args__ = (
        db.CheckConstraint('first_name != last_name'),
    )

    # 1 customer has many reviews: 1-to-many relationship between customers and reviews tables
    reviews = db.relationship('Review', back_populates='customer', cascade='all')

    # hotels and customers Many-to-Many relationship: The customer's hotels
    hotels = association_proxy('reviews', 'hotel', creator = lambda h: Review(hotel = h))

    # Deliverable # 5 solution code
    @validates('first_name', 'last_name')
    def validate_first_and_last_name(self, column_name, value):
        if (type(value) == str) and (3 <= len(value) <= 15):
            return value
        else:
            raise Exception

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)

    # Deliverable # 6 solution code
    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String, nullable=False)

    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)

    # A review belongs to a hotel: 1-to-many relationship between hotels and reviews tables
    hotel = db.relationship('Hotel', back_populates='reviews')

    # A review belongs to a customer: 1-to-many relationship between customers and reviews tables
    customer = db.relationship('Customer', back_populates='reviews')

    # Deliverable # 7 solution code
    @validates('rating')
    def validate_rating(self, column_name, value):
        if (type(value) == int) and (1 <= value <= 5):
            return value
        else:
            raise Exception
        
    @validates('text')
    def validate_text(self, column_name, value):
        if (type(value) == str) and (3 <= len(value) <= 100):
            return value
        else:
            raise Exception
        
    @validates('hotel_id', 'customer_id')
    def validate_hotel_id_and_customer_id(self, column_name, value):
        if (type(value) == int):
            return value
        else:
            raise Exception