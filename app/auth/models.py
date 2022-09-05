from werkzeug.security import generate_password_hash, check_password_hash
from flask import redirect,url_for
from flask_login import UserMixin,current_user
from datetime import datetime
from app.config import db
from flask_admin.contrib.sqla import ModelView

class User(db.Model,UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),nullable=False,unique=True)
    name = db.Column(db.String(100), nullable=False,index=True) # index=True, to use in search
    email = db.Column(db.String(100), nullable=False,unique=True)
    about_author = db.Column(db.String(500),nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    profile_pic = db.Column(db.String(128),nullable=True)
    password_hash = db.Column(db.String(128))

    # User Can Have Many Posts # One to Many
    posts = db.relationship('Posts',backref='poster')# poster.email to get user email# {{post.poster.email}} in jinja
    # User Can Have Many Comments # One to Many
    comments = db.relationship('Comments',backref='commenter')
    # User Can have 
    likes = db.relationship('Like',backref='user')
    # many two many
    #roles = db.relationship('Role',secondary='user_roles',backref=db.backref('user',lazy='dynamic'))
    role = db.Column(db.String(100),default='user')

    # def __init__(self,name,username,email,role='user'):
    #     self.name = name
    #     self.username = username
    #     self.email = email
    #     self.role = role

    def __repr__(self):
        return "<Username %r>" % self.username

    def is_admin(self):
        return self.role == "admin"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password,'sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# class AdminUser(User):
#     # __tablename__ = 'user' # if do not use this it`ll be created new table
#     role = db.Column(db.String(100),default='admin')

# class UserRoles(db.Model):
#     __tablename__ = 'user_roles'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer,db.ForeignKey('user.id',ONDELETE='CASCADE')) # თუ წაიშალა user, role დარჩება
#     role_id = db.Column(db.Integer,db.ForeignKey('role.id',ONDELETE='CASCADE'))# ondelete=Null # თუ წაიშალა user, user.id-ს ადგილას ჩაწერეს Nullს

# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50),unique=True)

##     is_admin = db.Column(db.Boolean,default=False)
##     user = db.relationship('User', secondary="user_role", backref=db.backref("role"))

class UserView(ModelView):

    def is_accessible(self):
        # return current_user.has_role('admin')
        return current_user.is_admin() # if it returs false, user cant see this view

    # if user tries anyway with link, it`ll  redirected to post.list
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('post.list'))

    can_create = False
    can_delete = False
    can_edit = True
    column_exclude_list = ['password_hash',]
    column_searchable_list = ['username','name','email']
    column_filters = ['role']
    column_editable_list = ['name','role']