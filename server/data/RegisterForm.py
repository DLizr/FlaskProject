from flask_wtf import FlaskForm
from sqlalchemy_serializer import SerializerMixin
from wtforms import PasswordField, StringField, TextAreaField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, ValidationError


class RegisterForm(FlaskForm, SerializerMixin):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    
    name = StringField('Имя пользователя', validators=[DataRequired()])
    
    def validate_name(form, field):
        if (len(field.data) < 3 or len(field.data) > 16):
            raise ValidationError("Длина никнеёма должна быть от 3 до 16 символов (включая).")
    
    about = TextAreaField("Как вы узнали о нашей игре?")
    submit = SubmitField('Войти')
