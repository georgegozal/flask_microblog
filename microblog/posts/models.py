from datetime import datetime
from microblog import db


class Posts(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))# slag`ll be like a custom url

    # Foreign Key To Link Users # many 2 one
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # Foreign Key To Link Comments #one to one
    commenter_id = db.Column(db.Integer,db.ForeignKey('comments.id')) 