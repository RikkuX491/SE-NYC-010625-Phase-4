# Lecture # 6 - Constraints and Validations

## Lecture Topics

- SQLAlchemy Constraints
  - `name = db.Column(db.String, nullable=False, unique=True)`
- CheckConstraint
  - `__table_args__ = (db.CheckConstraint('first_name != last_name'),)`
- Flask-SQLAlchemy Validations
  - `@validates('rating')`
  - ` @validates('first_name', 'last_name')`

## Setup

1. Make sure that you are in the correct directory (folder) that contains a `Pipfile`, then enter the command `pipenv install` in your terminal to install the required packages.

2. Now that your `pipenv` virtual environment is ready to use, enter the command `pipenv shell` in your terminal to enter the virtual environment.

3. Enter the command `cd server` in your terminal to move into the server directory.

4. Run these two terminal commands while in the `server` directory:

```sh
export FLASK_APP=app.py

export FLASK_RUN_PORT=7777
```

5. Run `flask run --debug` or `python app.py` in the terminal to run your flask app with Debug mode set to on.

## Deliverables

Write your code in the `models.py` file in the `server` directory for these first seven deliverables:

1. Add the following constraints to columns in the `Hotel` model:
   - A `unique` constraint to the `name` column. The value of the `unique` constraint should be `True`, so that hotel names are unique.
   - A `nullable` constraint to the `name` column. The value of the `nullable` constraint should be `False`, so that hotel names cannot have a `NULL` value.

2. Add the following validation in the `Hotel` model:
   - Must have a `name` that is a `string` between `5` and `50` characters long. Raises an `Exception` if the `name` is not valid.

3. Add the following constraints to columns in the `Customer` model:
   - A `nullable` constraint to the `first_name` column. The value of the `nullable` constraint should be `False`, so that customer first names cannot have a `NULL` value.
   - A `nullable` constraint to the `last_name` column. The value of the `nullable` constraint should be `False`, so that customer last names cannot have a `NULL` value.

4. Add the following `__table_args__` to the `Customer` model:
   - A `db.CheckConstraint` that does not allow for the value of the `first_name` column to be equal to the value of the `last_name` column.

5. Add the following validations in the `Customer` model:
   - Must have a `first_name` that is a `string` between `3` and `15` characters long. Raises an `Exception` if the `first_name` is not valid.
   - Must have a `last_name` that is a `string` between `3` and `15` characters long. Raises an `Exception` if the `last_name` is not valid.

6. Add the following constraints to columns in the `Review` model:
   - A `nullable` constraint to the `rating` column. The value of the `nullable` constraint should be `False`, so that review ratings cannot have a `NULL` value.
   - A `nullable` constraint to the `text` column. The value of the `nullable` constraint should be `False`, so that review texts cannot have a `NULL` value.
   - A `nullable` constraint to the `hotel_id` column. The value of the `nullable` constraint should be `False`, so that review hotel_ids cannot have a `NULL` value.
   - A `nullable` constraint to the `customer_id` column. The value of the `nullable` constraint should be `False`, so that review customer_ids cannot have a `NULL` value.

7. Add the following validations in the `Review` model:
   - Must have a `rating` that is an `integer` between `1` and `5`. Raises an `Exception` if the `rating` is not valid.
   - Must have a `text` that is a `string` between `3` and `100` characters long. Raises an `Exception` if the `text` is not valid.
   - Must have a `hotel_id` that is an `integer`. Raises an `TypeError` if the `hotel_id` is not valid.
   - Must have a `customer_id` that is an `integer`. Raises an `TypeError` if the `customer_id` is not valid.

Open a new terminal and run the following commands in the terminal to enter the virtual environment, change into the server folder, create the `migrations` folder, create a new revision file in the `versions` folder in `migrations`, execute the code within the `upgrade()` function in the revision file, and seed the database:

```sh
pipenv shell
cd server
flask db init
flask db migrate -m 'Create tables and columns with constraints'
flask db upgrade
python seed.py
```

Write your code in the `app.py` file in the `server` directory for these next six deliverables:

8. Modify the code in the `post` method in the `AllHotels` Resource class (`/hotels` route) so that the exceptions are caught when new hotels are not valid using `try` and `except` blocks. The response body should be a `dictionary` with the key of `"error"` and value of `"Hotel names cannot be null, must be unique, and must be strings that are between 5 and 50 characters long!"`

9. Modify the code in the `patch` method in the `HotelByID` Resource class (`/hotels/<int:id>` route) so that the exceptions are caught when the updated data is not valid using `try` and `except` blocks. The response body should be a `dictionary` with the key of `"error"` and value of `"Hotel names cannot be null, must be unique, and must be strings that are between 5 and 50 characters long!"`

10. Modify the code in the `post` method in the `AllCustomers` Resource class (`/customers` route) so that the exceptions are caught when new customers are not valid using `try` and `except` blocks. The response body should be a `dictionary` with the key of `"error"` and value of `"Customer first names and last names cannot be null, must be between 3 and 15 characters long, and the first name cannot be the same as the last name!"`

11. Modify the code in the `patch` method in the `CustomerByID` Resource class (`/customers/<int:id>` route) so that the exceptions are caught when the updated data is not valid using `try` and `except` blocks. The response body should be a `dictionary` with the key of `"error"` and value of `"Customer first names and last names cannot be null, must be between 3 and 15 characters long, and the first name cannot be the same as the last name!"`

12. Modify the code in the `post` method in the `AllReviews` Resource class (`/reviews` route) so that the exceptions are caught when new reviews are not valid using `try` and `except` blocks. The response body should be a `dictionary` with the key of `"error"` and value of `"Invalid Review data provided!"`

13. Modify the code in the `patch` method in the `ReviewByID` Resource class (`/reviews/<int:id>` route) so that the exceptions are caught when the updated data is not valid using `try` and `except` blocks. The response body should be a `dictionary` with the key of `"error"` and value of `"Invalid Review data provided!"`
