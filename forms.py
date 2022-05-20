from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length


class NewUser(FlaskForm):
    """Form to register a new user"""
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])

class EditUserForm(FlaskForm):
    """Form to edit user info"""
    username = StringField("Username", validators=[InputRequired()])

class LoginForm(FlaskForm):
    """Form for logging in a user"""
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=7)])

class ReviewForm(FlaskForm):
    """Form for creating a game review"""
    title = StringField("Title", validators=[InputRequired()])
    text = TextAreaField("Text", validators=[InputRequired()])