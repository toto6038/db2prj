from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.debug=True

@app.route('/')
def index():
    return render_template('index.html')

# hello後的網址會被接收為變數，可用來傳進template當作內容的一部分
@app.route("/hello/<name>")
def hello_name(name):
    return render_template('hello.html', name=name)

@app.route("/about")
def about_us():
    return render_template('about.html')

@app.route("/member")
def member():
    return render_template('member.html')

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html'), 404