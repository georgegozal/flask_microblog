from app.extensions import db
from datetime import datetime


class Follow(db.Model):
    __tablename__ = 'follow'

    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'follower_id: {self.follower_id}\nfollowed_id: {self.followed_id}'

# file:///home/george/Desktop/Flask_Web_Development_Developing.pdf 174
