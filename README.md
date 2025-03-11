# Lecture # 3 - Modeling Relationships in Flask-SQLAlchemy

## Lecture Topics

- One-To-Many Relationships with Flask-SQLAlchemy
  - `reviews = db.relationship('Review', back_populates='hotel')`
  - `hotel = db.relationship('Hotel', back_populates='reviews')`
- Cascades
  - `reviews = db.relationship('Review', back_populates='hotel', cascade='all')`
- Setting up Foreign Key columns in a table
  - `hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'))`
- Many-To-Many Relationships with Flask-SQLAlchemy
- Association Proxy
  - `customers = association_proxy('reviews', 'customer', creator = lambda c: Review(customer = c))`
- Serialization with Relationships
  - `rules=('-reviews.hotel', '-reviews.customer')`
  - `only=('id', 'name')`
  - `serialize_rules`
  - `serialize_only`

## Setup

1. Make sure that you are in the correct directory (folder) that contains a `Pipfile`, then enter the command `pipenv install` in your terminal to install the required packages.

2. Now that your `pipenv` virtual environment is ready to use, enter the command `pipenv shell` in your terminal to enter the virtual environment.

3. Enter the command `cd server` in your terminal to move into the server directory.

4. Run these two terminal commands while in the `server` directory:

```
export FLASK_APP=app.py

export FLASK_RUN_PORT=7777
```

## Deliverables

Write your code in the `models.py` file in the `server` directory for these first four deliverables:

1. Create a model class named `Review` that inherits from two classes: `db.Model` and `SerializerMixin`.

2. In the `Review` model class, create the following class variables:
   - A class variable named `__tablename__` that has the value of the string `'reviews'`.
   - A class variable named `id` that has the value of a `Column` object that has the `Integer` data type and is a primary key.
   - A class variable named `rating` that has the value of a `Column` object that has the `Integer` data type.
   - A class variable named `text` that has the value of a `Column` object that has the `String` data type.
   - A class variable named `hotel_id` that has the `Integer` data type and a `ForeignKey` constraint that uses the `db.ForeignKey` class and passes in `'hotels.id'` as an argument to `db.ForeignKey()`.
   - A class variable named `customer_id` that has the `Integer` data type and a `ForeignKey` constraint that uses the `db.ForeignKey` class and passes in `'customers.id'` as an argument to `db.ForeignKey()`.
   - A class variable named `hotel` that has the value returned from the `db.relationship()` method. The first argument of `db.relationship()` should be `'Hotel'`. The `back_populates` argument should have the value `'reviews'` which will be the variable that will be created in the `Hotel` model later to reference the other side of the 1-to-Many relationship.
   - A class variable named `customer` that has the value returned from the `db.relationship()` method. The first argument of `db.relationship()` should be `'Customer'`. The `back_populates` argument should have the value `'reviews'` which will be the variable that will be created in the `Customer` model later to reference the other side of the 1-to-Many relationship.

Hint: A `Column` object can be created by creating an instance of the `db.Column` class. Use `db.Integer` when referencing the `Integer` data type for a `db.Column()` instance. Use `db.String` when referencing the `String` data type for a `db.Column()` instance.

3. Add the following class variables to the `Hotel` model class:
   - A class variable named `reviews` that has the value returned from the `db.relationship()` method. The first argument of `db.relationship()` should be `'Review'`. The `back_populates` argument should have the value `'hotel'` which will be the variable that was created in the `Review` model which references the other side of the 1-to-Many relationship. Include a `cascade` argument that has the value of `'all'` in `db.relationship()` so that deleting a `Hotel` instance will result in deleting its associated `Review` instances.
   - A class variable named `customers` that has the value of an AssociationProxy object returned from the `association_proxy()` function that allows you to get a hotel's associated `Customer` instances.

4. Add the following class variables to the `Customer` model class:
   - A class variable named `reviews` that has the value returned from the `db.relationship()` method. The first argument of `db.relationship()` should be `'Review'`. The `back_populates` argument should have the value `'customer'` which will be the variable that was created in the `Review` model which references the other side of the 1-to-Many relationship. Include a `cascade` argument that has the value of `'all'` in `db.relationship()` so that deleting a `Customer` instance will result in deleting its associated `Review` instances.
   - A class variable named `hotels` that has the value of an AssociationProxy object returned from the `association_proxy()` function that allows you to get a customer's associated `Hotel` instances.

Write your code in the `app.py` file in the `server` directory for these next three deliverables:

5. Modify the code in the `get_hotels()` view (`/hotels` route) so that `hotel.to_dict()` serializes only the `id` and `name` columns.

6. Modify the code in the `hotel_by_id()` view (`/hotels/<int:id>` route) so that `hotel.to_dict()` serializes the `id` and `name` columns, and the `reviews` relationship, but limits the depth of the `reviews` relationship so that the reviews' `hotel` relationship and reviews' `customer` relationship are not serialized. Modify the `response_body` dictionary so that it includes a key named `customers` that has the value of the hotel's serialized customers data. Make sure to remove duplicate customers so that the serialized data only contains data for unique customers.

Hint: A hotel's customers can be accessed from the `customers` association proxy that was previously created in the `Hotel` model in Deliverable # 3. The `customers` association proxy will give you a `list` of `Customer` instances. To remove duplicate customers, convert that `list` to a `set`, and then convert it back to a `list`. Once you have the unique `list` of `customers`, you can use a list comprehension to create a `list` of serialized customers. Use the `to_dict()` method on a `Customer` instance to serialize the `Customer` instance.

7. Create a `get_reviews()` view. The route for this view should be of the format `/reviews`. The view should retrieve a list of all review instances from the `Review` model (`reviews` table) and use a list comprehension to create a list of dictionaries from the list of instances from the `Review` model such that each dictionary is created using the `to_dict()` method which serializes the `id`, `rating`, `text`, `hotel_id`, and `customer_id` columns, and the `hotel` and `customer` relationships, but limits the depth of the `hotel` and `customer` relationships so that the hotel's `reviews` relationship and customer's `reviews` relationship are not serialized. The view should then create and return a `Response` object using the `make_response()` function. Pass in the list that you created from the list comprehension as the first argument to `make_response()`, and pass in a status code of `200` (OK) for the second argument to `make_response()`.