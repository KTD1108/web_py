from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0.01)])
    image_url = StringField('Image URL', validators=[Length(max=200)])
    submit = SubmitField('Save Product')

class AddToCartForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)], default=1)
    submit = SubmitField('Add to Cart')

class AddressForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(max=20)])
    street = StringField('Street Address', validators=[DataRequired(), Length(max=200)])
    city = StringField('City', validators=[DataRequired(), Length(max=100)])
    state = StringField('State/Province', validators=[DataRequired(), Length(max=100)])
    zip_code = StringField('ZIP/Postal Code', validators=[DataRequired(), Length(max=20)])
    is_default = SelectField('Set as Default Address', choices=[(False, 'No'), (True, 'Yes')], coerce=lambda x: x == 'True')
    submit = SubmitField('Save Address')