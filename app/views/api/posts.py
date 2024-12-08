from flask import Blueprint, jsonify, request
from app.views.posts.models import Posts, Like
from app.views.auth.models import User
from app.extensions import db
from flask_login import login_required, current_user


api_posts = Blueprint('api_posts', __name__)


# get all posts
@api_posts.route('/api/posts', methods=['GET'])
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


@api_posts.route("/api/posts/like", methods=['POST'])
@login_required
def like():
    data = request.get_json()

    like = Like.query.filter_by(
        author=current_user.id, post_id=data.get("postId")).first()

    like_count = Like.query.filter_by(
        post_id=data.get("postId")
    ).count()

    if like:
        db.session.delete(like)
        db.session.commit()
        like_count -= 1
        msg = {
            "success": True,
            "message": f"Post <{data.get('postId')}> remove like",
            "like_count": like_count
        }
        return jsonify(msg), 200

    like = Like(author=current_user.id, post_id=data.get('postId'))
    like_count += 1
    db.session.add(like)
    db.session.commit()
    msg = {
        "success": True,
        "message": f"Post <{data.get('postId')}> add like",
        "like_count": like_count
    }
    return jsonify(msg), 201

    # if not post:
    #     return jsonify({'error': 'Post does not exist.'}, 400)
    # elif like:
    #     db.session.delete(like)
    #     db.session.commit()
    # else:
    #     like = Like(author=current_user.id, post_id=id)
    #     db.session.add(like)
    #     db.session.commit()
    # return jsonify({"likes": len(post.likes),
    # "liked": current_user.id in map(lambda x: x.author, post.likes)})
