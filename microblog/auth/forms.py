from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,EmailField,PasswordField#,ValidationError
from wtforms.validators import DataRequired,Email,EqualTo, Length,ValidationError
from .models import Users


class LoginForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField('Submit')

class UserForm(FlaskForm):
    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email):
        email_address = Users.query.filter_by(email=email.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField('Username',[Length(min=2, max=30),DataRequired()])
    name = StringField('Name',[DataRequired()])
    email = EmailField('Email',[Email(),DataRequired()])
    password_hash = PasswordField('Password',validators=[Length(min=6),DataRequired()])
    password_hash2 = PasswordField('Confirm Password',validators=[EqualTo('password_hash',message='Passwords Must Match!'),DataRequired()])
    # profile_pic = FileField('Profile Pic',validators=[FileAllowed(['png','jpg'])])
    # about_author = TextAreaField('About Author')
    submit = SubmitField('Create Account')


class PasswordForm(FlaskForm):
    email = EmailField('Email',validators=[DataRequired()])
    password_hash = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Sign in")