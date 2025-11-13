from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Tài khoản', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Mật khẩu ', validators=[DataRequired()])
    submit = SubmitField('Đăng nhập')

class RegisterForm(FlaskForm):
    username = StringField('Tài khoản', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Mật khẩu', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Nhập lại mật khẩu',
                              validators=[DataRequired(), EqualTo('password', message='Mật khẩu phải khớp')])
    submit = SubmitField('Đăng kí')