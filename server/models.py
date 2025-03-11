from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

# contains definitions of tables and associated schema constructs
metadata = MetaData()

# create the Flask SQLAlchemy extension
db = SQLAlchemy(metadata=metadata)

# define a model class by inheriting from db.Model.
# class Example(db.Model):
#     __tablename__ = 'examples'

#     id = db.Column(db.Integer, primary_key=True)
#     columnname = db.Column(db.String)
#     price = db.Column(db.Float)

class Hotel(db.Model, SerializerMixin):
    __tablename__ = 'hotels'

    # serialize_only = ('id',)
    # serialize_rules = ('-id',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return f"<Hotel # {self.id} - Name: {self.name}>"