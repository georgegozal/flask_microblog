from datetime import datetime
from microblog import db


class Comments(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(500))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    # Foreign Key To Link Users 
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'))