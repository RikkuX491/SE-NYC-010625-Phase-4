# Lecture # 7 - Client & Server Communication

## Lecture Topics

- Adding React to Flask
- CORS (Cross-Origin Resource Sharing)
- How to proxy the requests to our API

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

6. In another terminal, run `npm install --prefix client` in your terminal to install the dependencies from the `package.json` file.

7. Run `npm start --prefix client` in your terminal to run this React app in the browser. If your browser does not automatically open the page for you, open [http://localhost:4000](http://localhost:4000) to view it in your browser.

## Deliverables

Write your code in the `package.json` file in the `client` directory for this first deliverable:

1. Inside of the object in the `package.json` file, add a new key named `'proxy'` that has the value `'http://localhost:7777'`

Write your code in the `App` component in the `App.js` file in the `client/src/components` directory for these next four deliverables:

2. In the `getHotels()` function, write the code to make a `GET` request to `'/hotels'` to retrieve all hotels and update the `hotels` state with the hotel data.

3. In the `addHotel()` function, write the code to make a `POST` request to `'/hotels'` to create a new hotel and update the `'hotels'` state to add the new hotel to the state.

Hint: Use the spread operator to add the new hotel to the state (i.e.: `[...hotels, newHotel]`)

Note: In the `addHotel()` function, there is a parameter named `newHotel` which contains an object with the new hotel data that should be used for the `POST` request.

4. In the `updateHotel()` function, write the code to make a `PATCH` request to `/hotels/${id}` (use string interpolation since the value of the `id` parameter should be incorporated into the `string`). You should update a hotel by id and update the `hotels` state with the updated hotel data.

Hint: Use the `map()` array iterator method to update the state after getting the updated hotel data from the server.

Note: In the `updateHotel()` function, there are two parameters named `id` and `hotelDataForUpdate`. The `id` parameter contains a `number` that refers to the id for the hotel that should be updated. The `hotelDataForUpdate` parameter contains an `object` with the hotel data for the `PATCH` request.

5. In the `deleteHotel()` function, write the code to make a `DELETE` request to `/hotels/${id}` (use string interpolation since the value of the `id` parameter should be incorporated into the `string`). You should delete a hotel by id and update the `hotels` state to remove the hotel from the state.

Hint: Use the `filter()` array iterator method to update the state to remove a hotel from the state.

Note: In the `deleteHotel()` function, there is a parameter named `id` that contains a `number` that refers to the id for the hotel that should be deleted.

Write your code in the `HotelProfile` component in the `HotelProfile.js` file in the `client/src/components` directory for this final deliverable:

6. In the `getHotel` function, write the code to make a `GET` request to `/hotels/${id}` (use string interpolation since the value of the id variable should be incorporated into the `string`). You should retrieve a hotel by id and update the `hotel` state with the hotel data.

Note: In the `HotelProfile` component, there is a variable named `id` that is declared which is destructured from `useParams()`. This `id` value should be used when retrieving the hotel by id.
