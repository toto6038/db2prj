#  引入flask_wtf
from wsgiref.validate import validator
from flask_wtf import FlaskForm
#  各別引入需求欄位類別
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.fields import EmailField
#  引入驗證
from wtforms.validators import DataRequired, Email

#  從繼承FlaskForm開始
#  自定義 label
class UserForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired(message='Not Null')])
  password = PasswordField('Password', validators = [DataRequired(message='Not Null')])
  submit = SubmitField('Submit')

class RegForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired(message='Not Null')])
  password = PasswordField('Password', validators = [DataRequired(message='Not Null')])
  address = StringField('Address', validators=[DataRequired(message='Not Null')])
  admin = BooleanField('Administrator?', validators = [])
  submit = SubmitField('Submit')