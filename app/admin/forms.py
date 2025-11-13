from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange

class ProductForm(FlaskForm):
    name = StringField('Tên sản phẩm', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Mô tả chi tiết', validators=[Length(max=500)])
    price = DecimalField('Giá', validators=[DataRequired(), NumberRange(min=0.01)])
    image_url = StringField('URL ảnh', validators=[Length(max=200)])
    submit = SubmitField('Lưu sản phẩm')

class UserForm(FlaskForm):
    username = StringField('Tên tài khoản', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Mật khẩu mới (Để trống nếu muốn giữ mật khẩu hiện tại)', validators=[Length(min=6)])
    role = SelectField('Role', choices=[('USER', 'User'), ('ADMIN', 'Admin')], validators=[DataRequired()])
    submit = SubmitField('Lưu người dùng')