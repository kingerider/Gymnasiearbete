from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message='fältet får inte vara tomt'),
        Length(min=2, max=15, message='Måste vara mellan 2 och 15 tecken långt')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='fältet får inte vara tomt'),
        Email(message='fältet måste skrivas i email-format')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='fältet får inte vara tomt')
    ])
    confirm_password = PasswordField('Confirm password', validators=[
        DataRequired(message='fältet får inte vara tomt'), 
        EqualTo('password', message='du skrev fel lösenord')
    ])
    submit = SubmitField('Register')
