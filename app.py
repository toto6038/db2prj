from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import  LoginManager, UserMixin, login_user, current_user, logout_user

#  引入form類別
from view_form import UserForm, RegForm

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

app = Flask(__name__, static_folder = 'img/')
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


Base = automap_base()
Base.prepare(db.engine, reflect = True)

# 建立 table class
table_User = Base.classes.user
table_Manufacturer = Base.classes.manufacturer
table_Laptop = Base.classes.laptop
table_Product = Base.classes.product
table_Purchase = Base.classes.purchase
table_Ram= Base.classes.ram
table_Shop = Base.classes.shop
table_Storage = Base.classes.storage
table_Favors = Base.classes.favors

db_session = Session(db.engine, future=True)

@app.route('/test')
def test():
    # new_user = User(ID='121216',name='Howard',password='14765', address="Tainan",regDate='1976-12-01 12:04:12')
    # db.session.add(new_user)
    # db.session.commit()
    str = 'name'
    r = db.session.query(table_User).filter(table_User.str == 'Tommy')
    for i in r:
        print(i.name)
    return str(current_user.is_authenticated)

@app.route('/')
def index():
    return render_template(
        'index.html',
        current_user=current_user,
        admin=current_user.is_authenticated 
            and users[current_user.id]['admin'],
        home_active=True
        )

# hello後的網址會被接收為變數，可用來傳進template當作內容的一部分
@app.route("/hello/<name>")
def hello_name(name:str):
    return render_template(
        'hello.html',
        name=name,
        admin=current_user.is_authenticated 
            and users[current_user.id]['admin'],
        hello_active=True
        )

@app.route("/about")
def about_us():
    data=[
        {'name': '林暘瑾', 'stuid': '40947004S', 'img': 'https://avatars.githubusercontent.com/u/74698694', 'github': 'hitsuji0621'},
        {'name': '郭浩雲', 'stuid': '40947006S', 'img': 'https://avatars.githubusercontent.com/u/50100922', 'github': 'toto6038'},
        {'name': '謝皓青', 'stuid': '40947021S', 'img': 'https://avatars.githubusercontent.com/u/72068360', 'github': 'haoching918'}
    ]
    
    return render_template(
        'about.html',
        admin=current_user.is_authenticated 
            and users[current_user.id]['admin'],
        about_active=True,
        data=data
    )

@app.route("/member")
def member():
    if current_user.is_authenticated and users[current_user.id]['admin']:
        return render_template(
            'member.html', 
            values = db.session.query(table_User).all(),
            admin=current_user.is_authenticated 
                and users[current_user.id]['admin'],
            member_active=True
        )
    else:
        return login_manager.unauthorized()

# User login handler
class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    users={}
    for r in db.session.query(table_User).all():
        users[r.name]={'password': r.password, 'admin': not r.admin==0}

    if username not in users:
        return

    user=User()
    user.id=username
    return user

# @login_manager.request_loader
# def request_loader(request):
#     username=request.form.get('user_id')
#     if username not in users:
#         return
    
#     user=User()
#     user.id=username
    
#     user.is_authenticated = request.form['password']==users[username]['password']
#     return user;
    
users={}
for r in db.session.query(table_User).all():
        users[r.name]={'password': r.password, 'admin': not r.admin==0}
    

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
            print(str(users))
            user=User()
            user.id=username
            login_user(user)
            return redirect(url_for('hello_name', name=username))
        else:
            flash('Login failed! Either username or password is incorrect.')

    #  Validate failed or invalid credentials

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if form.validate_on_submit():
        if valid_usrname(form.username.data):
            # 頁面並無 ID 及 address 

            db.session.add(table_User(ID = 0, name=form.username.data, password=form.password.data, address=form.address.data, admin=form.admin.data))
            db.session.commit()

            # login
            user=User()
            user.id=form.username.data
            login_user(user)
            return redirect(url_for('hello_name', name=form.username.data))
        else:
            flash('Register failed! The username has been taken')
    return render_template('register.html', form=form)
def valid_usrname(name):
    for nm in db_session.query(table_User).filter_by(name=name):
        if nm.name == name:
            return False
    return True

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# find product laptop
@app.route('/laptop/positioning/<field>')
def find_laptop_pos(field):
    data = db.session.query(table_Product.name, table_Laptop.positioning, table_Laptop.cpu
    , table_Laptop.weight, table_Laptop.price, table_Laptop.disk_capacity).join(table_Product,table_Laptop.model 
    == table_Product.model).filter(table_Laptop.positioning == field)
    
    flash(f"{data.count()} data were found in Positioning : {field}")
    return render_template('laptop.html', data = data)
@app.route('/laptop/price/<field>')
def find_laptop_price(field):
    data = db.session.query(table_Product.name, table_Laptop.positioning, table_Laptop.cpu
    , table_Laptop.weight, table_Laptop.price, table_Laptop.disk_capacity).join(table_Product,table_Laptop.model 
    == table_Product.model).filter(table_Laptop.price + 10000 > field, table_Laptop.price < field )#　equal to table_Laptop.price > field - 10000
    
    flash(f"{data.count()} data were found for Price : $ {field}")
    return render_template('laptop.html', data = data)
@app.route('/laptop/weight/<field>')
def find_laptop_weight(field):
    data = db.session.query(table_Product.name, table_Laptop.positioning, table_Laptop.cpu
    , table_Laptop.weight, table_Laptop.price, table_Laptop.disk_capacity).join(table_Product,table_Laptop.model 
    == table_Product.model).filter(table_Laptop.weight <= field )

    flash(f"{data.count()} data were found for Weight : {field} Kg")

    return render_template('laptop.html', data = data)

# find product ram
@app.route('/ram/capacity/<field>')
def find_ram_cap(field):
    data = db.session.query(table_Product.name, table_Ram.capacity, table_Ram.price, table_Ram.ddr_type).join(table_Product,table_Ram.model 
    == table_Product.model).filter(table_Ram.capacity == field)

    flash(f"{data.count()} data were found for Capacity : {field} GB")
    return render_template('ram.html', data = data)
@app.route('/ram/price/<field>')
def find_ram_price(field):
    data = db.session.query(table_Product.name, table_Ram.capacity, table_Ram.price, table_Ram.ddr_type).join(table_Product,table_Ram.model 
    == table_Product.model).filter(table_Ram.price + 1000 > field, table_Ram.price < field)

    flash(f"{data.count()} data were found for Price : $ {field} ")
    return render_template('ram.html', data = data)
@app.route('/ram/type/<field>')
def find_ram_type(field):
    data = db.session.query(table_Product.name, table_Ram.capacity, table_Ram.price, table_Ram.ddr_type).join(table_Product,table_Ram.model 
    == table_Product.model).filter(table_Ram.ddr_type == field)

    flash(f"{data.count()} data were found for Type : {field} ")
    return render_template('ram.html', data = data)

# find product storage
@app.route('/storage/<field>')
def find_storage(field):
    return render_template('storage.html')

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
    return render_template(
        '404.html', 
        errCode=errCode, 
        errMsg=errMsg,
        admin=current_user.is_authenticated 
            and users[current_user.id]['admin']
    ), error.code