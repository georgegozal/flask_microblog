from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from .forms import EmptyForm
from app.auth.models import User
from app.extensions import db
from app.posts.models import Posts


followers = Blueprint('followers', __name__, template_folder='templates/followers')


@followers.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('post.list'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('followers.user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('followers.user', username=username))
    else:
        return redirect(url_for('post.list'))


@followers.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('post.index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('followers.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('followers.user', username=username))
    else:
        return redirect(url_for('post.index'))


@followers.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    form = EmptyForm()
    return render_template('user.html', user=user, form=form)


@followers.route('/<username>/posts')
@login_required
def user_posts(username):
    user = User.query.filter_by(username=username).first()
    return render_template('user_posts.html', posts=user.posts)


@followers.route('/followers/posts')
@login_required
def followed_posts():
    posts = current_user.followed_posts
    own = Posts.query.filter_by(poster_id=current_user.id)
    users_posts = posts.union(own).order_by(Posts.date_posted.desc()).all()
    return render_template('followed_posts.html', users_posts=users_posts)
