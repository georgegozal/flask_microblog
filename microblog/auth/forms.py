from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,EmailField,PasswordField,BooleanField,ValidationError,TextAreaField
from wtforms.validators import DataRequired,Email,EqualTo, Length
from wtforms.widgets import TextArea
from flask_wtf.file import FileField,FileAllowed,FileRequired
from flask_ckeditor import CKEditorField

class LoginForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField('Submit')

class UserForm(FlaskForm):
    username = StringField('Username',[DataRequired()])
    name = StringField('Name',[DataRequired()])
    email = EmailField('Email',[DataRequired()])
    password_hash = PasswordField('Password',validators=[DataRequired(),EqualTo('password_hash2',message='Passwords Must MAtch!')])
    password_hash2 = PasswordField('Confirm Password',validators=[DataRequired()])
    profile_pic = FileField('Profile Pic',validators=[FileRequired(),FileAllowed(['png','jpg'])])
    submit = SubmitField("Submit")

class PasswordForm(FlaskForm):
    email = EmailField('Email',validators=[DataRequired()])
    password_hash = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('submit')