from flask import Blueprint, jsonify
from app.posts.models import Posts
from app.auth.models import User

api = Blueprint('api', __name__,)


# get all posts
@api.route('/api/posts', methods=['GET'])
def get_all_posts():
    posts = Posts.query.all()
    posts_list = []
    for post in posts:
        p = {
            "id": post.id,
            "title": post.title,
            "date_posted": post.date_posted,
            "author": User.query.get_or_404(post.poster_id).username,
            "content": post.content
        }
        posts_list.append(p)
    return jsonify(posts_list)
