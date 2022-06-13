from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

#  引入form類別
from view_form import UserForm, RegForm

from sqlalchemy.ext.automap import automap_base

app = Flask(__name__)
app.debug=True

app.config['SECRET_KEY']=b'\xef\x01w8\xcd\xe5\xf3!\xc1\xc2\x81k\x12\n\xd7P'

# 連接到mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://team7:nomoredatabse@mc.toto6038.dev:8895/final_prj'
db = SQLAlchemy(app)
# 設定sqlalchemy自動跟蹤資料庫
SQLALCHEMY_TRACK_MODIFICATIONS = True
# 查詢時會顯示原始SQL語句
app.config['SQLALCHEMY_ECHO'] = True
# 禁止自動提交資料處理
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False


Base = automap_base()
Base.prepare(db.engine, reflect = True)

# 建立 table class
User = Base.classes.user
Manufacturer = Base.classes.manufacturer
#Favors = Base.classes.favors
Laptop = Base.classes.laptop
Product = Base.classes.product
Purchase = Base.classes.purchase
Ram= Base.classes.ram
Shop = Base.classes.shop
Storage = Base.classes.storage

@app.route('/test')
def test():
    # new_user = User(ID='121216',name='Howard',password='14765', address="Tainan",regDate='1976-12-01 12:04:12')
    # db.session.add(new_user)
    # db.session.commit()
    # r = db.session.query(User).all()
    # for i in r:
    #     print(i.name)
    return render_template('index.html')

@app.route('/')
def index():
    return render_template('index.html')

# hello後的網址會被接收為變數，可用來傳進template當作內容的一部分
@app.route("/hello/<name>")
def hello_name(name:str):
    return render_template('hello.html', name=name)

@app.route("/about")
def about_us():
    return render_template('about.html')

@app.route("/member")
def member():
    return render_template('member.html', values = db.session.query(User).all())

@app.route('/user', methods=['GET', 'POST'])
def login():
    form = UserForm()
    #  flask_wtf類中提供判斷是否表單提交過來的method，不需要自行利用request.method來做判斷
    name=None
    if form.validate_on_submit():
        name=form.username.data
        form.username.data=''
        return redirect(url_for('hello_name', name=name))
    #  如果不是提交過來的表單，就是GET，這時候就回傳user.html網頁

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if form.validate_on_submit():
        if valid_usrname(form.username.data):
            # 頁面並無 ID 及 address 
            db.session.add(User(ID ='848101', name=form.username.data, password=form.password.data, address='2qqweqw', admin=form.admin.data))
            db.session.commit()
            return redirect(url_for('hello_name', name=form.username.data))
    return render_template('register.html', form=form)
def valid_usrname(name):
    for nm in db.session.query(User).all():
        if nm.name == name:
            return False
    return True

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
    return render_template('404.html', errCode=errCode, errMsg=errMsg), error.code