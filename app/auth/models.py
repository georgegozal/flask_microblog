from werkzeug.security import generate_password_hash, check_password_hash
from flask import redirect, url_for
from flask_login import UserMixin, current_user
from datetime import datetime
from app.extensions import db
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from app.posts.models import Posts
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.config import Config


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    about_author = db.Column(db.String(500), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    profile_pic = db.Column(db.String(128), nullable=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(100), default='user')

    # User Can Have Many Posts # One to Many
    posts = db.relationship('Posts', backref='poster')
    # User Can Have Many Comments # One to Many
    comments = db.relationship('Comments', backref='commenter')
    # User Can have
    likes = db.relationship('Like', backref='user')

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(Config.SECRET_KEY, expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(Config.SECRET_KEY)
        try:
            user_id = s.loads(token)['user_id']
        except Exception as e:
            print(e)
            return None
        return User.query.get(user_id)

    followers = db.Table('followers',
        db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
        db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
    )

    followed = db.relationship(
        'User', 
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    followed_posts = db.relationship(
        'Posts', 
        secondary=followers,#'join(Posts,User).join(followers)',
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(Posts.poster_id == followers.c.followed_id),
        lazy='dynamic', 
        viewonly=True)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        try:
            is_following = self.followed.filter_by(username=user.username).count() > 0
        except AttributeError:
            is_following = False
        return is_following

    def __repr__(self):
        return "<Username %r>" % self.username

    def is_admin(self):
        return self.role == "admin"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, 'sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class UserView(ModelView):

    def is_accessible(self):
        try:
            is_admin = current_user.is_admin()
        except AttributeError as a:
            print(a)
            is_admin = False
        return is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('post.list'))

    can_create = False
    can_delete = False
    can_edit = True
    column_exclude_list = ['password_hash']
    column_searchable_list = ['username', 'name', 'email']
    column_filters = ['role']
    column_editable_list = ['name', 'role']
    column_list = ('id', 'username', 'name', 'email', 'about_author', 'date_added', 'role')


class FileView(FileAdmin):
    def is_accessible(self):
        try:
            is_admin = current_user.is_admin()
        except AttributeError as a:
            print(a)
            is_admin = False
        return is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('post.list'))
