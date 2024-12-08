from flask import Blueprint, jsonify, request
from app.views.posts.models import Posts
from app.views.auth.models import User
from app.extensions import db


api = Blueprint('api', __name__)


@api.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    u = {
        'id': user.id,
        'name': user.name,
        'username': user.username,
        'mail': user.email,
        'role': user.role
    }
    return jsonify(u)


@api.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = []
    for user in users:
        u = {
            'id': user.id,
            'name': user.name,
            'username': user.username,
            'mail': user.email,
            'role': user.role
        }
        user_list.append(u)
    return jsonify(user_list)


@api.route('/api/users/<int:id>/followers', methods=['GET'])
def get_followers(id):
    user = User.query.get_or_404(id)
    user_list = []
    for follower in user.followers.all():
        u = {
            'id': follower.id,
            'name': follower.name,
            'username': follower.username,
            'mail': follower.email,
            'role': follower.role
        }
        user_list.append(u)
    return jsonify(user_list)


@api.route('/api/users/<int:id>/followed', methods=['GET'])
def get_followed(id):
    user = User.query.get_or_404(id)
    user_list = []
    for follower in user.followed.all():
        u = {
            'id': follower.id,
            'name': follower.name,
            'username': follower.username,
            'mail': follower.email,
            'role': follower.role
        }
        user_list.append(u)
    return jsonify(user_list)


@api.route('/api/users', methods=['POST'])
def create_user():
    request_data = request.get_json()
    user = User(
        username=request_data['username'],
        name=request_data['name'],
        email=request_data['email'],
        )
    user.set_password(request_data['password'])
    db.session.add(user)
    db.session.commit()

    user = User.query.order_by(User.id.desc()).limit(1).first()


@api.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    pass
