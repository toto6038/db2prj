from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.debug=True

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/hello/<name>")
def hello_name(name):
    return render_template('hello.html', name=name)