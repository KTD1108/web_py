from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0.01)])
    image_url = StringField('Image URL', validators=[Length(max=200)])
    submit = SubmitField('Save Product')

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('New Password (leave blank to keep current)', validators=[Length(min=6)])
    role = SelectField('Role', choices=[('USER', 'User'), ('ADMIN', 'Admin')], validators=[DataRequired()])
    submit = SubmitField('Save User')