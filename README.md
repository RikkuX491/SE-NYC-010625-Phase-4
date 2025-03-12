# Lecture # 4 - Retrieving Data from APIs & Building APIs

## Lecture Topics

- Retrieving Data from APIs & Building APIs

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

Write your code in the `app.py` file in the `server` directory (folder):

1. Modify the `@app.route('/hotels')` decorator so that the route accepts `GET` and `POST` requests.

2. Modify the code in the `all_hotels()` view as follows:
   - `if` a `GET` request is made to `/hotels`, the code to retrieve all hotels, serialize the hotel instances, and return the response will execute.
   - Else if (`elif`) a `POST` request is made to `/hotels`, a new hotel is created from the `json` data received from `request`. The new hotel is added to `db.session`, and the changes are committed to the database. The new hotel instance is then serialized using the `to_dict()` method so that only the `id` and `name` columns are serialized, and a `Response` object is returned using the `make_response()` function that contains the serialized hotel data and a status code of `201` (CREATED).

3. Modify the `@app.route('/hotels/<int:id>')` decorator so that the route accepts `GET`, `PATCH`, and `DELETE` requests.

4. Modify the code in the `hotel_by_id()` view as follows:
   - `if` a `GET` request is made to `/hotels/<int:id>`, the code to serialize the hotel instance, modify the `response_body` dictionary to include the `'customers'` key and value pair, and return the response will execute.
   - Else if (`elif`) a `PATCH` request is made to `/hotels/<int:id>`, the `json` data received from `request` is used to update the hotel instance, and the changes are committed to the database. The hotel instance is then serialized using the `to_dict()` method so that only the `id` and `name` columns are serialized, and a `Response` object is returned using the `make_response()` function that contains the serialized hotel data and a status code of `200` (OK).
   - Else if (`elif`) a `DELETE` request is made to `/hotels/<int:id>`, the hotel is deleted and the changes are committed to the database. A `Response` object is returned using the `make_response()` function that contains a response body with the value of `{}` (empty dictionary) and a status code of `204` (NO CONTENT).

5. Modify the `@app.route('/customers')` decorator so that the route accepts `GET` and `POST` requests.

6. Modify the code in the `all_customers()` view as follows:
   - `if` a `GET` request is made to `/customers`, the code to retrieve all customers, serialize the customer instances, and return the response will execute.
   - Else if (`elif`) a `POST` request is made to `/customers`, a new customer is created from the `json` data received from `request`. The new customer is added to `db.session`, and the changes are committed to the database. The new customer instance is then serialized using the `to_dict()` method so that only the `id`, `first_name`, and `last_name` columns are serialized, and a `Response` object is returned using the `make_response()` function that contains the serialized customer data and a status code of `201` (CREATED).

7. Modify the `@app.route('/customers/<int:id>')` decorator so that the route accepts `GET`, `PATCH`, and `DELETE` requests.

8. Modify the code in the `customer_by_id()` view as follows:
   - `if` a `GET` request is made to `/customers/<int:id>`, the code to serialize the customer instance, modify the `response_body` dictionary to include the `'hotels'` key and value pair, and return the response will execute.
   - Else if (`elif`) a `PATCH` request is made to `/customers/<int:id>`, the `json` data received from `request` is used to update the customer instance, and the changes are committed to the database. The customer instance is then serialized using the `to_dict()` method so that only the `id`, `first_name`, and `last_name` columns are serialized, and a `Response` object is returned using the `make_response()` function that contains the serialized customer data and a status code of `200` (OK).
   - Else if (`elif`) a `DELETE` request is made to `/customers/<int:id>`, the customer is deleted and the changes are committed to the database. A `Response` object is returned using the `make_response()` function that contains a response body with the value of `{}` (empty dictionary) and a status code of `204` (NO CONTENT).

9. Modify the `@app.route('/reviews')` decorator so that the route accepts `GET` and `POST` requests.

10. Modify the code in the `all_reviews()` view as follows:
    - `if` a `GET` request is made to `/reviews`, the code to retrieve all reviews, serialize the review instances, and return the response will execute.
    - Else if (`elif`) a `POST` request is made to `/reviews`, a new review is created from the `json` data received from `request`. The new review is added to `db.session`, and the changes are committed to the database. The new review instance is then serialized using the `to_dict()` method so that the `id`, `rating`, `text`, `hotel_id`, and `customer_id` columns, and the `hotel` and `customer` relationships are serialized, but limit the depth of the serialization of the `hotel` and `customer` relationships so that the hotel's `reviews` relationship and customer's `reviews` relationship are not serialized. A `Response` object is returned using the `make_response()` function that contains the serialized review data and a status code of `201` (CREATED).

11. Modify the `@app.route('/reviews/<int:id>')` decorator so that the route accepts `GET`, `PATCH`, and `DELETE` requests.

12. Modify the code in the `review_by_id()` view as follows:
    - `if` a `GET` request is made to `/reviews/<int:id>`, the code to serialize the review instance and return the response will execute.
    - Else if (`elif`) a `PATCH` request is made to `/reviews/<int:id>`, the `json` data received from `request` is used to update the review instance, and the changes are committed to the database. The review instance is then serialized using the `to_dict()` method so that the `id`, `rating`, `text`, `hotel_id`, and `customer_id` columns, and the `hotel` and `customer` relationships are serialized, but limit the depth of the serialization of the `hotel` and `customer` relationships so that the hotel's `reviews` relationship and customer's `reviews` relationship are not serialized. A `Response` object is returned using the `make_response()` function that contains the serialized review data and a status code of `200` (OK).
    - Else if (`elif`) a `DELETE` request is made to `/reviews/<int:id>`, the review is deleted and the changes are committed to the database. A `Response` object is returned using the `make_response()` function that contains a response body with the value of `{}` (empty dictionary) and a status code of `204` (NO CONTENT).