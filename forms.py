from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, SelectField, PasswordField
from wtforms.validators import InputRequired, Email, Optional, Length

class SignupForm(FlaskForm):
    """Form for creating a new user"""
    email = StringField('Email', validators=[InputRequired(), Email()])
    username = StringField('Username', validators=[InputRequired(), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired()])
    first_name = StringField('First Name', validators=[InputRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(max=50)])

class LoginForm(FlaskForm):
    """Form for logging a user in / authenticating a user"""
    username = StringField('Username', validators=[InputRequired(), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired()])

class EditUserForm(FlaskForm):
    """Form for editing user info"""
    email = StringField('Email', validators=[Optional(), Email()])
    username = StringField('Username', validators=[Optional(), Length(max=50)])
    password = PasswordField('Password', validators=[Optional()])
    first_name = StringField('First Name', validators=[Optional(), Length(max=50)])
    last_name = StringField('Last Name', validators=[Optional(), Length(max=50)])

class VerifyUserForm(FlaskForm):
    """Verifies the identity of a user whenever they want to change their personal info."""
    email = StringField('Email', validators=[InputRequired(), Email()])
    username = StringField('Username', validators=[InputRequired(), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired()])