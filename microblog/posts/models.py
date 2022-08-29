from datetime import datetime
from microblog import db
from flask_admin.contrib.sqla import ModelView


class Posts(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))# slag`ll be like a custom url

    # Foreign Key To Link Users # many 2 one
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # Foreign Key To Link Comments #one to one
    # comment_id = db.Column(db.Integer,db.ForeignKey('comments.id')) 

class Comments(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(500))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    # Foreign Key To Link Users 
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    post_id = db.Column(db.Integer,db.ForeignKey('posts.id', ondelete="CASCADE"))

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    author = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id', ondelete="CASCADE"), nullable=False)


class PostView(ModelView):
    can_create = False
    can_delete = False
    can_edit = True
    # column_exclude_list = ['password_hash',]
    # column_searchable_list = ['username','name','email']
    # column_filters = ['role']
    # column_editable_list = ['name']

class CommentView(ModelView):
    can_create = False
    can_delete = True
    can_edit = False
    # column_exclude_list = ['password_hash',]
    # column_searchable_list = ['username','name','email']
    # column_filters = ['role']
    # column_editable_list = ['name']