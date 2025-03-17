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
    name = db.Column(db.String, nullable=False, unique=True)

    # 1 hotel has many reviews: 1-to-many relationship between hotels and reviews tables
    reviews = db.relationship('Review', back_populates='hotel', cascade='all')

    # hotels and customers Many-to-Many relationship: The hotel's customers
    customers = association_proxy('reviews', 'customer', creator = lambda c: Review(customer = c))

    @validates('name')
    def validate_name(self, column_name, value):
        # Here's one way to write out our validation code
        # if(type(value) == str) and (len(value) > 4):
        #     return value
        # else:
        #     raise Exception(f"Hotel {column_name} must be a string that is at least 5 characters long!")

        # Here's another way using multiple exception types
        if (type(value) != str):
            raise TypeError(f"Hotel {column_name} must be a string!")
        elif (len(value) < 5):
            raise ValueError(f"Hotel {column_name} must be at least 5 characters long!")
        else:
            return value


class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)

    __table_args__ = (
        db.CheckConstraint('first_name != last_name'),
    )

    # 1 customer has many reviews: 1-to-many relationship between customers and reviews tables
    reviews = db.relationship('Review', back_populates='customer', cascade='all')

    # hotels and customers Many-to-Many relationship: The customer's hotels
    hotels = association_proxy('reviews', 'hotel', creator = lambda h: Review(hotel = h))

    @validates('first_name', 'last_name')
    def validate_first_and_last_name(self, column_name, value):
        if (type(value) != str):
            raise TypeError(f"Customer's {column_name} must be a string!")
        elif (len(value) < 3):
            raise ValueError(f"Customer's {column_name} must be at least 3 characters long!")
        else:
            return value

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    text = db.Column(db.String)

    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))

    # A review belongs to a hotel: 1-to-many relationship between hotels and reviews tables
    hotel = db.relationship('Hotel', back_populates='reviews')

    # A review belongs to a customer: 1-to-many relationship between customers and reviews tables
    customer = db.relationship('Customer', back_populates='reviews')