from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import NumberRange, DataRequired


class ParameterForm(FlaskForm):
    width = IntegerField(
        'Ширина: ',
        default=20,
        name='width',
        validators=[NumberRange(min=20), DataRequired()]
    )
    height = IntegerField(
        'Высота: ',
        default=20,
        name='height',
        validators=[NumberRange(min=20), DataRequired()]
    )
    submit = SubmitField('Задать размер мира')
