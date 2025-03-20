# Lecture # 9 - Authorization

## Lecture Topics

- Authorizing Requests
- Password Protection with Bcrypt

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

## Important notes

1. The following code is used to import `Bcrypt` in `app.py`:

```python
from flask_bcrypt import Bcrypt
```

2. The following code is used to initialize an instance of the `Bcrypt` class and use it within your Flask app. This instance can be stored into a variable to reference the `Bcrypt` instance throughout your code:

```python
bcrypt = Bcrypt(app)
```

3. The following code can be used to encrypt your password, using `Bcrypt`. `password` is a variable containing a password. `bcrypt` is a variable containing the `Bcrypt` instance:

```python
password = request.json.get('password')

bcrypt.generate_password_hash(password).decode('utf-8')
```

4. We use the following code to check if a password, when "hashed" (the process that the password would go through when being encrypted), matches a hashed password that is stored in the database. `password` is a variable containing a password. `user.password_hash` is a reference to the value from the `password_hash` column for a particular user:

```python
username = request.json.get('username')
password = request.json.get('password')
user = User.query.filter(User.username == username).first()

bcrypt.check_password_hash(user.password_hash, password)
```