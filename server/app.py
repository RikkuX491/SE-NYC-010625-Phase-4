#!/usr/bin/env python3
from flask import Flask
from flatburger.data import burgers
from flatburger.html import flatburger_html_code

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Welcome to my website!</h1>'

@app.route('/another_page')
def different_page():
    return '<h1>This is another page!</h1>'

@app.route('/intro/<name>')
def intro(name):
    return f"<h1>Hi! My name is {name}.</h1>"

@app.route('/intro/<name>/<int:age>')
def intro_2(name, age):
    return f"<h1>Hi! My name is {name}. I'm {age} years old!</h1>"

@app.route('/<float:number>')
def float_example(number):
    return f"<h1>The number is {number}</h1>"

# Deliverable # 1 solution code
@app.route('/greeting/<first_name>/<last_name>')
def greeting(first_name, last_name):
    return f"<h1>Greetings, {first_name} {last_name}!</h1>"

# Deliverable # 2 solution code
@app.route('/count_and_square/<int:number>')
def count_and_square(number):
    squared_nums_string = ""

    for num in range(1, number + 1):
        squared_nums_string += f'{num ** 2}\n'
    
    return squared_nums_string

# Deliverable # 3 solution code
@app.route('/burgers')
def get_burgers():
    return burgers

# Deliverable # 4 solution code
@app.route('/flatburger_page')
def flatburger():
    return flatburger_html_code

if __name__ == "__main__":
    app.run(port=7777, debug=True)