# Lecture # 5 - REST APIs with Flask

## Lecture Topics

- Building REST APIs with `flask-restful`
- Retrieve with `flask-restful` (handling `GET` requests)
- Create with `flask-restful` (handling `POST` requests)
- Update with `flask-restful` (handling `PATCH` requests)
- Delete with `flask-restful` (handling `DELETE` requests)

## Setup

1. Make sure that you are in the correct directory (folder) that contains a `Pipfile`, then enter the command `pipenv install` in your terminal to install the required packages.

2. Now that your `pipenv` virtual environment is ready to use, enter the command `pipenv shell` in your terminal to enter the virtual environment.

3. Enter the command `cd server` in your terminal to move into the server directory.

4. Run these two terminal commands while in the `server` directory:

```
export FLASK_APP=app.py

export FLASK_RUN_PORT=7777
```

5. Run `flask run --debug` or `python app.py` to run your flask app with Debug mode set to on.

## Deliverables

In line 28 of `app.py` (in the `server` directory / folder), the following line of code has created an instance of the `Api` class and stored it into a variable, `api`:

```python
api = Api(app)
```

You can use this `Api` instance to connect a Resource to a route as follows, if there is a Resource named `AllHotels` and a `/hotels` route:

```python
api.add_resource(AllHotels, '/hotels')
```

1. Refactor your code for the `/hotels` route's `all_hotels()` view, instead using `flask_restful` to create an `AllHotels` class that inherits from the `Resource` class. The `AllHotels` Resource class should contain a `get()` method and a `post()` method. The `get()` method should be able to retrieve all hotels and return the appropriate response and status code, same as before. The `post()` method should be able to add a new hotel to the database and return the appropriate response and status code, same as before. Use the `api.add_resource()` method to connect your `AllHotels` Resource class to the `/hotels` route.

2. Refactor your code for the `/hotels/<int:id>` route's `hotel_by_id()` view, instead using `flask_restful` to create a `HotelByID` class that inherits from the `Resource` class. The `HotelByID` Resource class should contain a `get()` method, a `patch()` method, and a `delete()` method. The `get()` method should be able to find a hotel by its `id` and return the appropriate response and status code, same as before. The `patch()` method should be able to find a hotel by its `id`, update it, and return the appropriate response and status code, same as before. The `delete()` method, should be able to find a hotel by its `id`, delete it, and return the appropriate response and status code, same as before. For the `get()`, `patch()`, and `delete()` methods, if the hotel is not found, return the appropriate response and status code, same as before. Use the `api.add_resource()` method to connect your `HotelByID` Resource class to the `/hotels/<int:id>` route.

3. Refactor your code for the `/customers` route's `all_customers()` view, instead using `flask_restful` to create an `AllCustomers` class that inherits from the `Resource` class. The `AllCustomers` Resource class should contain a `get()` method and a `post()` method. The `get()` method should be able to retrieve all customers and return the appropriate response and status code, same as before. The `post()` method should be able to add a new customer to the database and return the appropriate response and status code, same as before. Use the `api.add_resource()` method to connect your `AllCustomers` Resource class to the `/customers` route.

4. Refactor your code for the `/customers/<int:id>` route's `customer_by_id()` view, instead using `flask_restful` to create a `CustomerByID` class that inherits from the `Resource` class. The `CustomerByID` Resource class should contain a `get()` method, a `patch()` method, and a `delete()` method. The `get()` method should be able to find a customer by its `id` and return the appropriate response and status code, same as before. The `patch()` method should be able to find a customer by its `id`, update it, and return the appropriate response and status code, same as before. The `delete()` method, should be able to find a customer by its `id`, delete it, and return the appropriate response and status code, same as before. For the `get()`, `patch()`, and `delete()` methods, if the customer is not found, return the appropriate response and status code, same as before. Use the `api.add_resource()` method to connect your `CustomerByID` Resource class to the `/customers/<int:id>` route.

5. Refactor your code for the `/reviews` route's `all_reviews()` view, instead using `flask_restful` to create an `AllReviews` class that inherits from the `Resource` class. The `AllReviews` Resource class should should contain a `get()` method and a `post()` method. The `get()` method should be able to retrieve all reviews and return the appropriate response and status code, same as before. The `post()` method should be able to add a new review to the database and return the appropriate response and status code, same as before. Use the `api.add_resource()` method to connect your `AllReviews` Resource class to the `/reviews` route.

6. Refactor your code for the `/reviews/<int:id>` route's `review_by_id()` view, instead using `flask_restful` to create a `ReviewByID` class that inherits from the `Resource` class. The `ReviewByID` Resource class should contain a `get()` method, a `patch()` method, and a `delete()` method. The `get()` method should be able to find a review by its `id` and return the appropriate response and status code, same as before. The `patch()` method should be able to find a review by its `id`, update it, and return the appropriate response and status code, same as before. The `delete()` method, should be able to find a review by its `id`, delete it, and return the appropriate response and status code, same as before. For the `get()`, `patch()`, and `delete()` methods, if the review is not found, return the appropriate response and status code, same as before. Use the `api.add_resource()` method to connect your `ReviewByID` Resource class to the `/reviews/<int:id>` route.