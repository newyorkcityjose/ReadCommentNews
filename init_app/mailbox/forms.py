from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, Length, url
from wtforms.fields.html5 import URLField
from wtforms import ValidationError



class MessageForm(FlaskForm):
    to = StringField("To")
    title = StringField("Title")
    message = StringField("Message")
