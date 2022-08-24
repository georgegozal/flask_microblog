from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from microblog import db


class Users(db.Model,UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),nullable=False,unique=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False,unique=True)
    about_author = db.Column(db.String(500),nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    profile_pic = db.Column(db.String(128),nullable=True)
    password_hash = db.Column(db.String(128))
    # User Can Have Many Posts

    def __init__(self,name,username,email,password_hash):
        self.name = name
        self.username = username
        self.email = email
        self.password_hash = password_hash#generate_password_hash(password_hash,method='sha256')

    def __repr__(self):
        return "<Name %r>" % self.name