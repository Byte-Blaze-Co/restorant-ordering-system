from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, PasswordField, EmailField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, length, NumberRange
from flask_wtf.file import FileField, FileRequired


class SignUpForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), length(min=2)])
    password1 = PasswordField('Enter Your Password', validators=[DataRequired(), length(min=6)])
    password2 = PasswordField('Confirm Your Password', validators=[DataRequired(), length(min=6)])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Enter Your Password', validators=[DataRequired()])
    submit = SubmitField('Giriş Yap')


class PasswordChangeForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired(), length(min=6)])
    new_password = PasswordField('New Password', validators=[DataRequired(), length(min=6)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), length(min=6)])
    change_password = SubmitField('Şifreyi Değiştir')


class ShopItemsForm(FlaskForm):
    product_name = StringField('Ürünün İsmi', validators=[DataRequired()])
    current_price = FloatField('Şuanki Fiyat', validators=[DataRequired()])
    previous_price = FloatField('Eski Fiyatı', validators=[DataRequired()])
    in_stock = IntegerField('Stok Durumu', validators=[DataRequired(), NumberRange(min=0)])
    product_picture = FileField('Ürün Fotoğrafı', validators=[DataRequired()])
    flash_sale = BooleanField('Hızlı Satış')

    add_product = SubmitField('Ürün Ekle')
    update_product = SubmitField('Güncelle')


class OrderForm(FlaskForm):
    order_status = SelectField('Order Status', choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'),
                                                        ('Out for delivery', 'Out for delivery'),
                                                        ('Delivered', 'Delivered'), ('Canceled', 'Canceled')])

    update = SubmitField('Update Status')





