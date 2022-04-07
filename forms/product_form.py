from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SelectField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class ProductForm(FlaskForm):
    title = StringField('Продукт', validators=[DataRequired()])
    description = TextAreaField("Описание")
    city = SelectField("Город", choices=["Актау", "Актобе", "Алматы", "	Атырау",
                                         "Жезказган", "Караганды", "Кокшетау", "Костанай",
                                         "Кызылорда", "Нур-Султан", "Павлодар", "Петропавловск",
                                         "Семей", "Талдыкорган", "Тараз", "Туркестан",
                                         "Уральск", "Усть-Каменогорск", "Шымкент"])
    price = FloatField("Цена")
    submit = SubmitField('Применить')