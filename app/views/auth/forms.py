from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, EmailField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from .models import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class UserForm(FlaskForm):
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email):
        email_address = User.query.filter_by(email=email.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField('Username', [Length(min=2, max=30), DataRequired()])
    name = StringField('Name', [DataRequired()])
    email = EmailField('Email', [Email(), DataRequired()])
    password_hash = PasswordField('Password', [Length(min=6), DataRequired()])
    password_hash2 = PasswordField('Confirm Password', [EqualTo('password_hash', message='Passwords Must Match!'), DataRequired()])
    profile_pic = FileField('Profile Pic', [FileAllowed(['png', 'jpg', 'jpeg'])])

    # about_author = TextAreaField('About Author')
    submit = SubmitField('Create Account')


class RequestResetForm(FlaskForm):
    def validate_email_address(self, email):
        email_address = User.query.filter_by(email=email.data).first()
        if email_address is None:
            raise ValidationError('There is no account with that email!')

    email = EmailField('Email', [Email(), DataRequired()])
    submit = SubmitField("Request Password Reset")


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', [Length(min=6), DataRequired()])
    password_confirm = PasswordField('Confirm Password', [EqualTo('password', message='Passwords Must Match!'), DataRequired()])
    submit = SubmitField("Reset Password")
