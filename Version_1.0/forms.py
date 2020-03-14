from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import InputRequired, length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), length(min=3, max=20)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])


class LoginForm(FlaskForm):
    email=StringField('Email',validators=[InputRequired(),Email()])
    password=PasswordField('Password',validators=[InputRequired()])



