from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import  LoginManager, UserMixin, login_user

#  引入form類別
from view_form import UserForm

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

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'
login_manager.login_message='Please log in first'


Base = automap_base()
Base.prepare(db.engine, reflect = True)

# 建立 table class
User = Base.classes.user
Manufacturer = Base.classes.manufacturer
#Favor = Base.classes.favor
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

# User login handler
class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return

    user=User()
    user.id=username
    return user

@login_manager.request_loader
def request_loader(request):
    username=request.form.get('user_id')
    if username not in users:
        return
    
    user=User()
    user.id=username
    
    user.is_authenticated = request.form['password']==users[username]['password']
    return user;
    
users = {'tommy': {'password': '918'}}

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserForm()
    #  flask_wtf類別中提供判斷是否表單提交過來的method，不需要自行利用request.method來做判斷
    if form.validate_on_submit():
        username=form.username.data
        # Clear username field after submitting
        form.username.data=''
        password=form.password.data
        
        if (username in users) and (users[username]['password']==password):
            user=User()
            user.id=username
            login_user(user)
            return redirect(url_for('hello_name', name=username))
        else:
            flash('Login failed! Either username or password is incorrect.')

    #  Validate failed or invalid credentials

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
    return render_template('404.html', errCode=errCode, errMsg=errMsg), error.code