from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, Length, url
from wtforms.fields.html5 import URLField
from wtforms import ValidationError

class AddUserForm(FlaskForm):
    """Form for adding users"""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=4)])
    picture = FileField("Update Profile Picture", validators=[FileAllowed(["jpg", "png"])])
    bio = StringField('Bio')

class LoginForm(FlaskForm):
    """Login Form"""
    
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=4)])

class UpdateProfileForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password')
    picture = FileField("Update Profile Picture", validators=[FileAllowed(["jpg", "png"])])
    bio = StringField('Bio')

    def validate_password(self, password):
        print("I am here.")
        if password.data and len(password.data) < 4:
            raise ValidationError("Minimum 4 charactes should be provided")