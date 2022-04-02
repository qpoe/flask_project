from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class ProductForm(FlaskForm):
    title = StringField('Продукт', validators=[DataRequired()])
    description = TextAreaField("Описание")
    price = IntegerField("Цена")
    submit = SubmitField('Применить')