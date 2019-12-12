from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class LoginForm(FlaskForm):

    id = StringField('ID', validators=[DataRequired(), Length(min=3, max=15)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=3, max=16)])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')

class AdminLoginForm(FlaskForm):

    username = StringField('User Name', validators=[DataRequired(), Length(min=3, max=10)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=3, max=16)])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')