from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
#  引入form類別
from view_form import UserForm

app = Flask(__name__)
app.config['SECRET_KEY']='your key'
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

@app.route('/user', methods=['GET', 'POST'])
def login():
    form = UserForm()
    #  flask_wtf類中提供判斷是否表單提交過來的method，不需要自行利用request.method來做判斷
    if form.validate_on_submit():
        return 'Success Submit'
    #  如果不是提交過來的表單，就是GET，這時候就回傳user.html網頁
    return render_template('login.html', form=form)

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