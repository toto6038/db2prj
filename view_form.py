#  引入flask_wtf
from wsgiref.validate import validator
from flask_wtf import FlaskForm
#  各別引入需求欄位類別
from wtforms.fields import *
#  引入驗證
from wtforms.validators import DataRequired, Email
from wtforms import validators

#  從繼承FlaskForm開始
#  自定義 label
class UserForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired(message='Not Null')])
  password = PasswordField('Password', validators = [DataRequired(message='Not Null')])
  submit = SubmitField('Submit')

class RegForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired(message='Not Null')])
  password = PasswordField('Password', validators = [DataRequired(message='Not Null')])
  admin = BooleanField('Administrator?', validators = [])
  submit = SubmitField('Submit')

class ModForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired(message='Not Null')])
  password = PasswordField('Password', validators = [DataRequired(message='Not Null')])
  submit = SubmitField('Submit changes')

class insertLaptopForm(FlaskForm):
  productName = StringField('Product name', validators=[DataRequired(message='Not Null')])
  maker = SelectField('Manufacturer')
  model = StringField('Model', validators=[DataRequired(message='Not Null')])
  position = SelectField('Positioning', choices=[('entry level', 'Entry level'), ('light gaming', 'Light gaming'), ('pro gaming', 'Pro gaming'), ('professional', 'Professional'), ('creator', 'Creator'), ('business', 'Business')])
  price = IntegerField('Price', [validators.NumberRange(0, 2147483647)])
  os = StringField('Operating system', validators=[DataRequired(message='Not Null')])
  cpu = StringField('CPU', validators=[DataRequired(message='Not Null')])
  gpu = StringField('GPU', validators=[DataRequired(message='Not Null')])
  vram = IntegerField('VRAM', [validators.NumberRange(0, 2147483647)])
  disk_capacity = IntegerField('Disk capacity', [validators.NumberRange(1, 2147483647)])
  ram = IntegerField('Ram capacity', [validators.NumberRange(1, 2147483647)])
  screen = FloatField('Screen size', [validators.DataRequired(message='Not Null'), validators.NumberRange(0, 2147483647)])
  dimension = StringField('Dimension')
  resolution = StringField('Resolution')
  refreshRate = IntegerField('Refresh rate', [validators.NumberRange(0, 2147483647)])
  weight = FloatField('Weight', [validators.DataRequired(message='Not Null'), validators.NumberRange(0, 2147483647)])
  color = StringField('Color', [validators.DataRequired(message='Not Null')])
  rgb = BooleanField('RGB')
  submit = SubmitField('Submit')