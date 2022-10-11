from flask import redirect, url_for
from flask_login import current_user
from datetime import datetime
from app.extensions import db
from flask_admin.contrib.sqla import ModelView


class Posts(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Key To Link Users # many 2 one
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # Foreign Key To Link Comments #one to one
    # comment_id = db.Column(db.Integer,db.ForeignKey('comments.id'))
    comments = db.relationship('Comments', backref='post')
    likes = db.relationship('Like', backref='post')

    def __repr__(self):
        return "Title:  %r" % self.title


class Comments(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    # Foreign Key To Link Users
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete="CASCADE"))
    likes = db.relationship('Like', backref='comments')


class Like(db.Model):
    __tablename__ = 'like'
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    author = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=False)
    # users = db.relationship('User',backref='like')
    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id', ondelete="CASCADE")  # nullable=False
        )

    comment_id = db.Column(db.Integer, db.ForeignKey(
        'comments.id', ondelete="CASCADE"  # nullable=False
                    ))

    def __repr__(self):
        return f'{self.user.username}'


class PostView(ModelView):
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
    column_list = ('id', 'title', 'date_posted', 'content', 'poster', 'likes')
    column_searchable_list = ['id','title', 'poster.username']
    column_filters = ['date_posted','poster.username']

class CommentView(ModelView):
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
    can_delete = True
    can_edit = False
    column_list = ('content', 'date_posted', 'commenter', 'post', 'likes')
    column_searchable_list = ['id','content', 'commenter.username','post.title']
