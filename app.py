from dataclasses import field
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import  LoginManager, UserMixin, login_user, current_user, logout_user
from sqlalchemy import func, desc
import re
#  引入form類別
from view_form import UserForm, RegForm, ModForm

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

app = Flask(__name__)
app.debug=True

app.config['SECRET_KEY']=b'\xef\x01w8\xcd\xe5\xf3!\xc1\xc2\x81k\x12\n\xd7P'

# 連接到mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://team7:nomoredatabse@mc.toto6038.dev:8895/final_prj'
app.config['SQLALCHEMY_POOL_RECYCLE'] = 600
db = SQLAlchemy(app)
# 設定sqlalchemy自動跟蹤資料庫
SQLALCHEMY_TRACK_MODIFICATIONS = True
# 查詢時會顯示原始SQL語句
# app.config['SQLALCHEMY_ECHO'] = True
# 禁止自動提交資料處理
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
app.jinja_env.globals['is_admin']=False
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'
login_manager.login_message=u'Access denied because you are not logged in or logged in with an unprivileged account.'


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
    )

# hello後的網址會被接收為變數，可用來傳進template當作內容的一部分
@app.route("/hello/<name>")
def hello_name(name:str):
    return render_template(
        'hello.html',
        name=name,
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
        data=data
    )

@app.route("/member")
def member():
    if current_user.is_authenticated and users[current_user.id]['admin']:
        return render_template(
            'member.html', 
            values = db.session.query(table_User).all(),
        )
    else:
        return login_manager.unauthorized()

@app.route("/admin")
def admin():
    if current_user.is_authenticated and users[current_user.id]['admin']:
        return render_template(
            'admin.html', 
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
def update_user():
    for r in db.session.query(table_User).all():
        users[r.name]={'password': r.password, 'admin': not r.admin==0}
update_user()


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
            app.jinja_env.globals['is_admin']=users[username]['admin']
            return redirect(url_for('hello_name', name=username))
        else:
            flash('Login failed! Either username or password is incorrect.')

    #  Validate failed or invalid credentials

    return render_template('login.html', form=form)

@app.route('/account', methods=['GET', 'POST'])
def account():
    form = ModForm()
    if form.validate_on_submit():
        if valid_usrname(form.username.data):
            db.session.query(table_User).filter(table_User.name == current_user.id).update(dict(name=form.username.data))
            db.session.query(table_User).filter(table_User.name == form.username.data).update(dict(password=form.password.data))
            db.session.commit()
            
            update_user()
            
            user=User()
            user.id=form.username.data
            login_user(user)
            app.jinja_env.globals['is_admin']=users[user.id]['admin']
            flash("user data has been modify")
            return render_template('index.html')
        else:
            flash('Modify failed! The username has been taken')
    return render_template('account.html', form = form)

@app.route('/delete')
def delete():
    name = current_user.id
    logout_user()
    app.jinja_env.globals['is_admin']=False
    db.session.query(table_User).filter(table_User.name == name).delete()
    db.session.commit()
    flash(f"{name} has been delete")
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if form.validate_on_submit():
        if valid_usrname(form.username.data):
            db.session.add(table_User(ID = 0, name=form.username.data, password=form.password.data, admin=form.admin.data))
            db.session.commit()
            
            update_user()
            user=User()
            user.id=form.username.data
            login_user(user)
            app.jinja_env.globals['is_admin']=users[user.id]['admin']
            return redirect(url_for('hello_name', name=user.id))
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
    app.jinja_env.globals['is_admin']=False
    return redirect(url_for('index'))

# find product laptop
@app.route('/laptop/positioning/<field>', methods=['GET'])
def find_laptop_pos(field):
    attribute=request.args.get('sortBy')
    if not attribute or attribute not in table_Laptop.__table__.columns.keys():
        attribute='price'

    descendingOrder=request.args.get('orderBy')=='desc'

    if descendingOrder:
        data = db.session.query(table_Laptop, table_Product).filter(table_Laptop.model==table_Product.model).filter(table_Laptop.positioning == field).order_by(desc(getattr(table_Laptop, attribute)))
    else:
        data = db.session.query(table_Laptop, table_Product).filter(table_Laptop.model==table_Product.model).filter(table_Laptop.positioning == field).order_by(getattr(table_Laptop, attribute))
    

    flash(f"{data.count()} entries in: {field.title()}") if data.count()>1 else flash(f"{data.count()} entry in: {field.title()}")

    return render_template('laptop.html', data = data)


@app.route('/laptop/price/<field>', methods=['GET'])
def find_laptop_price(field='all'):
    attribute=request.args.get('sortBy')
    if not attribute or attribute not in table_Laptop.__table__.columns.keys():
        attribute='price'

    descendingOrder=request.args.get('orderBy')=='desc'

    if field=='lapor':
        data = db.session.query(table_Laptop, table_Product, func.max(table_Laptop.price)).filter(table_Laptop.model==table_Product.model).filter(db.session.query(func.max(table_Laptop.price)).scalar()==table_Laptop.price).group_by(table_Laptop.model).order_by(getattr(table_Laptop, attribute))
        flash('Since you are as rich as Lapor, the most expensive item is returned.')
    elif field=='all':
        if descendingOrder:
            data = db.session.query(table_Laptop, table_Product).filter(table_Laptop.model==table_Product.model).filter(table_Laptop.price > 0, table_Laptop.price <= 2147483647 ).order_by(desc(getattr(table_Laptop, attribute)))
        else:
            data = db.session.query(table_Laptop, table_Product).filter(table_Laptop.model==table_Product.model).filter(table_Laptop.price > 0, table_Laptop.price <= 2147483647 ).order_by(getattr(table_Laptop, attribute))
        
        flash(f'{data.count()} entries returned')

    elif not bool(re.match("^(\d{1,10})(\-)(\d{1,10})$", field)):
        return redirect(location='/404')
    else:
        field1=int(field.split('-')[0])
        field2=int(field.split('-')[1])

        if descendingOrder:
            data = db.session.query(table_Laptop, table_Product).filter(table_Laptop.model==table_Product.model).filter(table_Laptop.price > field1, table_Laptop.price <= field2 ).order_by(desc(getattr(table_Laptop, attribute)))
        else:
            data = db.session.query(table_Laptop, table_Product).filter(table_Laptop.model==table_Product.model).filter(table_Laptop.price > field1, table_Laptop.price <= field2 ).order_by(getattr(table_Laptop, attribute))
        
        if int(field1) != 0 and int(field2) == 2147483647:
            flash(f"{data.count()} data were found for Price : $ > {field1}")
        elif int(field1) != 0 and int(field2) != 0:
            flash(f"{data.count()} data were found for Price : $ {field1} - {field2}")
        else:
            flash(f"{data.count()} data were found for Price : $ < {field2}")

    return render_template('laptop.html', data = data)


@app.route('/laptop/weight/<field>', methods=['GET'])
def find_laptop_weight(field):
    attribute=request.args.get('sortBy')
    if not attribute or attribute not in table_Laptop.__table__.columns.keys():
        attribute='price'

    descendingOrder=request.args.get('orderBy')=='desc'


    if descendingOrder:
        data = db.session.query(table_Laptop, table_Product).filter(table_Laptop.model==table_Product.model).filter(table_Laptop.weight <= field).order_by(desc(getattr(table_Laptop, attribute)))
    else:
        data = db.session.query(table_Laptop, table_Product).filter(table_Laptop.model==table_Product.model).filter(table_Laptop.weight <= field).order_by(getattr(table_Laptop, attribute))
    
    flash(f"{data.count()} data were found for Weight : {field} Kg")

    return render_template('laptop.html', data = data)

# find product ram
@app.route('/ram/capacity/<field>', methods=['GET'])
def find_ram_cap(field):
    attribute=request.args.get('sortBy')
    if not attribute or attribute not in table_Laptop.__table__.columns.keys():
        attribute='price'

    descendingOrder=request.args.get('orderBy')=='desc'

    if descendingOrder:
        data = db.session.query(table_Ram, table_Product).filter(table_Ram.model==table_Product.model).filter(table_Ram.capacity == field).order_by(desc(getattr(table_Ram, attribute)))
    else:
        data = db.session.query(table_Ram, table_Product).filter(table_Ram.model==table_Product.model).filter(table_Ram.capacity == field).order_by(getattr(table_Ram, attribute))

    flash(f"{data.count()} data were found for Capacity : {field} GB")
    return render_template('ram.html', data = data)

@app.route('/ram/price/<field>')
def find_ram_price(field='all'):
    attribute=request.args.get('sortBy')
    if not attribute or attribute not in table_Laptop.__table__.columns.keys():
        attribute='price'

    descendingOrder=request.args.get('orderBy')=='desc'

    if field=='lapor':
        if descendingOrder:
            data = db.session.query(table_Ram, table_Product, func.max(table_Ram.price)).filter(table_Ram.model==table_Product.model).filter(db.session.query(func.max(table_Ram.price)).scalar()==table_Ram.price).group_by(table_Ram.model).order_by(desc(getattr(table_Ram, attribute)))
        else:
            data = db.session.query(table_Ram, table_Product, func.max(table_Ram.price)).filter(table_Ram.model==table_Product.model).filter(db.session.query(func.max(table_Ram.price)).scalar()==table_Ram.price).group_by(table_Ram.model).order_by(getattr(table_Ram, attribute))

        flash('Since you are as rich as Lapor, the most expensive item is returned.')

    elif field=='all':
        if descendingOrder:
            data = db.session.query(table_Ram, table_Product).filter(table_Ram.model==table_Product.model).filter(table_Ram.price > 0, table_Ram.price <= 2147483647).order_by(desc(getattr(table_Ram, attribute)))
        else:
            data = db.session.query(table_Ram, table_Product).filter(table_Ram.model==table_Product.model).filter(table_Ram.price > 0, table_Ram.price <= 2147483647).order_by(getattr(table_Ram, attribute))

        flash(f'{data.count()} entries returned')

    elif not bool(re.match("^(\d{1,10})(\-)(\d{1,10})$", field)):
        return redirect(location='/404')
    else:
        field1 = int(field.split('-')[0])
        field2 = int(field.split('-')[1])

        if descendingOrder:
            data = db.session.query(table_Ram, table_Product).filter(table_Ram.model==table_Product.model).filter(table_Ram.price > field1, table_Ram.price <= field2).order_by(desc(getattr(table_Ram, attribute)))
        else:
            data = db.session.query(table_Ram, table_Product).filter(table_Ram.model==table_Product.model).filter(table_Ram.price > field1, table_Ram.price <= field2).order_by(getattr(table_Ram, attribute))
            
        if int(field1) != 0 and int(field2) == 2147483647:
            flash(f"{data.count()} data were found for Price : $ > {field1}")
        elif int(field1) != 0 and int(field2) != 0:
            flash(f"{data.count()} data were found for Price : $ {field1} - {field2}")
        else:
            flash(f"{data.count()} data were found for Price : $ < {field2}")

    return render_template('ram.html', data = data)

@app.route('/ram/type/<field>', methods=['GET'])
def find_ram_type(field):
    attribute=request.args.get('sortBy')
    if not attribute or attribute not in table_Laptop.__table__.columns.keys():
        attribute='price'

    descendingOrder=request.args.get('orderBy')=='desc'

    if descendingOrder:
        data = db.session.query(table_Ram, table_Product).filter(table_Ram.model==table_Product.model).filter(table_Ram.ddr_type==field).order_by(desc(getattr(table_Ram, attribute)))
    else:
        data = db.session.query(table_Ram, table_Product).filter(table_Ram.model==table_Product.model).filter(table_Ram.ddr_type==field).order_by(getattr(table_Ram, attribute))



    flash(f"{data.count()} data were found for Type : {field} ")
    return render_template('ram.html', data = data)

# find product storage
@app.route('/storage/type/<field>', methods=['GET'])
def find_storage_type(field):
    attribute=request.args.get('sortBy')
    if not attribute or attribute not in table_Laptop.__table__.columns.keys():
        attribute='price'

    descendingOrder=request.args.get('orderBy')=='desc'

    if descendingOrder:
        data = db.session.query(table_Storage, table_Product).filter(table_Storage.model == table_Product.model).filter(table_Storage.media_type == field).order_by(desc(getattr(table_Storage, attribute)))
    else:
        data = db.session.query(table_Storage, table_Product).filter(table_Storage.model == table_Product.model).filter(table_Storage.media_type == field).order_by(getattr(table_Storage, attribute))

    flash(f"{data.count()} data were found for Type : {field.upper()} ")

    return render_template('storage.html', data = data)

@app.route('/storage/price/<field>', methods=['GET'])
def find_storage_price(field='all'):
    attribute=request.args.get('sortBy')
    if not attribute or attribute not in table_Laptop.__table__.columns.keys():
        attribute='price'

    descendingOrder=request.args.get('orderBy')=='desc'


    if field=='lapor':
        if descendingOrder:
            data = db.session.query(table_Storage, table_Product, func.max(table_Storage.price)).filter(table_Storage.model==table_Product.model).filter(db.session.query(func.max(table_Storage.price)).scalar()==table_Storage.price).group_by(table_Storage.model).order_by(desc(getattr(table_Storage, attribute)))
        else:
            data = db.session.query(table_Storage, table_Product, func.max(table_Storage.price)).filter(table_Storage.model==table_Product.model).filter(db.session.query(func.max(table_Storage.price)).scalar()==table_Storage.price).group_by(table_Storage.model).order_by(getattr(table_Storage, attribute))
            
        flash('Since you are as rich as Lapor, the most expensive item is returned.')

    elif field=='all':
        if descendingOrder:
            data = db.session.query(table_Storage, table_Product).filter(table_Storage.model==table_Product.model).filter(table_Storage.price > 0, table_Storage.price <= 2147483647).order_by(desc(getattr(table_Storage, attribute)))
        else:
            data = db.session.query(table_Storage, table_Product).filter(table_Storage.model==table_Product.model).filter(table_Storage.price > 0, table_Storage.price <= 2147483647).order_by(getattr(table_Storage, attribute))

        flash(f'{data.count()} entries returned')
    elif not bool(re.match("^(\d{1,10})(\-)(\d{1,10})$", field)):
        return redirect(location='/404')
    else:
        field1 = int(field.split('-')[0])
        field2 = int(field.split('-')[1])

        if descendingOrder:
            data = db.session.query(table_Storage, table_Product).filter(table_Storage.model == table_Product.model).filter(table_Storage.price > field1, table_Storage.price <= field2).order_by(desc(getattr(table_Storage, attribute)))
        else:
            data = db.session.query(table_Storage, table_Product).filter(table_Storage.model == table_Product.model).filter(table_Storage.price > field1, table_Storage.price <= field2).order_by(getattr(table_Storage, attribute))


        if int(field1) != 0 and int(field2) == 2147483647:
            flash(f"{data.count()} data were found for Price : $ > {field1}")
        elif int(field1) != 0 and int(field2) != 0:
            flash(f"{data.count()} data were found for Price : $ {field1} - {field2}")
        else:
            flash(f"{data.count()} data were found for Price : $ < {field2}")

    return render_template('storage.html', data = data)
@app.route('/storage/capacity/<field>', methods=['GET'])
def find_storage_cap(field):
    field=int(field)
    attribute=request.args.get('sortBy')
    if not attribute or attribute not in table_Laptop.__table__.columns.keys():
        attribute='price'

    descendingOrder=request.args.get('orderBy')=='desc'

    if field<0:
        return redirect(location='/404')
    elif field==0:
        if descendingOrder:
            data = db.session.query(table_Storage, table_Product).filter(table_Storage.model == table_Product.model).filter(table_Storage.price>4000).order_by(desc(getattr(table_Storage, attribute)))
        else:
            data = db.session.query(table_Storage, table_Product).filter(table_Storage.model == table_Product.model).filter(table_Storage.price>4000).order_by(getattr(table_Storage, attribute))

        flash(f"{data.count()} data were found for Capacity > 4 TB")
    else:
        if descendingOrder:
            data = db.session.query(table_Storage, table_Product).filter(table_Storage.model == table_Product.model).filter(table_Storage.capacity <= field).order_by(desc(getattr(table_Storage, attribute)))
        else:
            data = db.session.query(table_Storage, table_Product).filter(table_Storage.model == table_Product.model).filter(table_Storage.capacity <= field).order_by(getattr(table_Storage, attribute))
    
        if field < 1000:
            flash(f"{data.count()} data were found for Capacity: {field} GB")
        else:
            flash(f"{data.count()} data were found for Capacity: {field//1000} TB")
            
    return render_template('storage.html', data = data)

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

app.add_url_rule('/storage', view_func=find_storage_price)
app.add_url_rule('/ram', view_func=find_ram_price)
app.add_url_rule('/laptop', view_func=find_laptop_price)