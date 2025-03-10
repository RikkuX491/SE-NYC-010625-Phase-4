# Lecture # 2 - Flask-SQLAlchemy

## Lecture Topics

- Flask-SQLAlchemy
- Database Migration
  - `flask db migrate`
- Flask Shell
- Querying a Database in a Flask Application
  - `Hotel.query.all()`
  - `Hotel.query.first()`
  - `Hotel.query.filter(Hotel.id == 1).first()`
  - `Hotel.query.filter_by(id = 1).first()`
  - `db.session.get(Hotel, 1)`
- Seeding a Database
- Serialization
- Returning a JSON response
- Other important Flask db terminal commands
- `flask db init`
- `flask db upgrade`
- `flask db downgrade`
- Adding new rows to the database, and committing to save changes
  - `db.session.add(hotel1)`
  - `db.session.commit()`
- Deleting rows from a table
  - `db.session.delete(hotel1)`
  - `Hotel.query.delete()`

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

Write your code in the `models.py` file in the `server` directory for these first two deliverables:

1. Create a model class named `Hotel` that inherits from two classes: `db.Model` and `SerializerMixin`.

2. In the `Hotel` model class, create the following class variables:
   - A class variable named `__tablename__` that has the value of the string `'hotels'`
   - A class variable named `id` that has the value of a `Column` object that has the `Integer` data type and is a primary key.
   - A class variable named `name` that has the value of a `Column` object that has the `String` data type

Hint: A `Column` object can be created by creating an instance of the `db.Column` class. Use `db.Integer` when referencing the `Integer` data type for a `db.Column()` instance. Use `db.String` when referencing the `String` data type for a `db.Column()` instance.

Write your code in the `app.py` file in the `server` directory for these next two deliverables:

3. Create a `get_hotels()` view. The route for this view should be of the format `/hotels`. The view should retrieve a list of all hotel instances from the `Hotel` model (`hotels` table) and use a list comprehension to create a list of dictionaries from the list of instances from the `Hotel` model such that each dictionary contains keys and value pairs for each `db.Column` in the `Hotel` model. The view should then create and return a `Response` object using the `make_response()` function. Pass in the list that you created from the list comprehension as the first argument to `make_response()`, and pass in a status code of `200` (OK) for the second argument to `make_response()`.

Hint: If the `Hotel` model inherits from the `SerializerMixin` class, you gain access to the `to_dict()` method which can be called on an instance of a model containing `db.Column`s. The `to_dict()` method returns a dictionary containing the information for each of the columns for the instance.

4. Create a `hotel_by_id()` view that takes one parameter, an integer. The route for this view should be of the format `/hotels/<id>`. The view should retrieve the `Hotel` instance that has the id that is equal to the `id` parameter. If the `Hotel` instance is found, convert the instance into a dictionary using the `to_dict()` method provided by `SerializerMixin`. The view should then create and return a `Response` object using the `make_response()` function. Pass in the dictionary that was returned from the `to_dict()` method as the first argument to `make_response()`, and pass in a status code of `200` (OK) for the second argument to `make_response()`. Else, if the `Hotel` instance is not found, the view should instead create and return a `Response` object using the `make_response()` function. For the first argument to `make_response()`, pass in a dictionary that has a key named `"error"` and a value of `"Hotel Not Found!"`. For the second argument to `make_response()`, pass in a status code of `404` (Not Found).