from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange

class ProductForm(FlaskForm):
    name = StringField('Tên sản phẩm', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Mô tả sản phẩm', validators=[Length(max=500)])
    price = DecimalField('Giá tiền', validators=[DataRequired(), NumberRange(min=0.01)])
    image_url = StringField('Image URL', validators=[Length(max=200)])
    submit = SubmitField('Lưu sản phẩm')

class AddToCartForm(FlaskForm):
    quantity = IntegerField('Số lượng', validators=[DataRequired(), NumberRange(min=1)], default=1)
    submit = SubmitField('Thêm vào giỏ hàng')

class AddressForm(FlaskForm):
    full_name = StringField('Họ và tên', validators=[DataRequired(), Length(max=100)])
    phone = StringField('Số điện thoại', validators=[DataRequired(), Length(max=20)])
    street = StringField('Địa chỉ đường', validators=[DataRequired(), Length(max=200)])
    city = StringField('Thành phố', validators=[DataRequired(), Length(max=100)])
    state = StringField('Huyện/Quận', validators=[DataRequired(), Length(max=100)])
    zip_code = StringField('Mã bưu chính', validators=[DataRequired(), Length(max=20)])
    is_default = SelectField('Đặt làm địa chỉ mặc định', choices=[(False, 'Không'), (True, 'Có')], coerce=lambda x: x == 'True')
    submit = SubmitField('Lưu địa chỉ')