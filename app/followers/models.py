# from werkzeug.security import generate_password_hash, check_password_hash
# from flask import redirect,url_for
# from flask_login import UserMixin,current_user
# from datetime import datetime
# from app.extensions import db
# from flask_admin.contrib.sqla import ModelView
# from flask_admin.contrib.fileadmin import FileAdmin
# from app.auth.models import User
# from app.posts.models import Posts

# class UserFollowers(User):
#     # __tablename__ = 'users'
#     # def __init__(self):
#     #     super(UserFollowers,self)
#     # create followers for user
#     followers = db.Table('followers',
#         db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
#         db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
#     )

#     followed = db.relationship(
#         'User', secondary=followers,
#         primaryjoin=(followers.c.follower_id == id),
#         secondaryjoin=(followers.c.followed_id == id),
#         backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

#     #get posts from followed users, and own posts
#     def followed_posts(self):
#         followed = Posts.query.join(
#             self.followers, (self.followers.c.followed_id == Posts.user_id)).filter(
#                 self.followers.c.follower_id == self.id)
#         own = Posts.query.filter_by(user_id=self.id)
#         return followed.union(own).order_by(Posts.timestamp.desc())

#     def follow(self, user):
#         if not self.is_following(user):
#             self.followed.append(user)

#     def unfollow(self, user):
#         if self.is_following(user):
#             self.followed.remove(user)

#     def is_following(self, user):
#         return self.followed.filter(
#             self.followers.c.followed_id == user.id).count() > 0

# # 'app.auth.models.User 'followers'