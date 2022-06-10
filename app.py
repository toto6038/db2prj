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
@app.errorhandler(500)
def pageNotFound(error):
    errCode=error.code
    if(errCode==404):
        errMsg='The page you are looking for is not found.'
    elif(errCode==500):
        errMsg='Internal server error'
    else:
        errMsg=''
    return render_template('404.html', errCode=errCode, errMsg=errMsg), 404