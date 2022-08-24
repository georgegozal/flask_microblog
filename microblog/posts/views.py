from flask import Flask, flash,url_for, redirect,render_template,Blueprint, request
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from .models import Posts
from .forms import PostForm,SearchForm
from microblog import db

post_view = Blueprint('posts',__name__,template_folder="templates/posts")


# view all posts
@post_view.route('/posts')
def list():
    posts = Posts.query.order_by(Posts.date_posted).all()
    return render_template('posts.html',posts=posts)

# view one post
@post_view.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template(
        'post.html',
        post = post
    )

# Add Post Page
@post_view.route('/add-post',methods=['GET','POST'])
def add():
    form = PostForm()

    if form.validate_on_submit():
        post = Posts(
            title = form.title.data,
            content = form.content.data,
            slug = form.slug.data,
            poster_id = current_user.id
        )
        # Clear the Form
        form.title.data = ''
        form.content.data = ''
        form.slug.data = ''

        # Add post data to database
        db.session.add(post)
        db.session.commit()
        # return a message
        flash('Blog Post Submitted Successfully!',category='success')
        return redirect( url_for('view.post', id=post.id))
    return render_template(
        'add_post.html',
        form=form
    )

# delete post
@post_view.route('/posts/delete/<int:id>')
def delete(id):
    
    post = Posts.query.get_or_404(id)
    if int(post.poster.id) == current_user.id:
        try:
            db.session.delete(post)
            db.session.commit()
            flash('Post has been deleted',category='success')
            return redirect(url_for('post_view.posts'))
        except:
            flash('there was a problem deleting a post',category='error')
    else:
        flash("You Aren`t Authorized To Delete That Post!",category='error')
        return redirect(url_for('post_view.posts'))

# @post_view.context_processor
# def base():
#     form = SearchForm()
#     return dict(form=form)

@post_view.route('/search',methods=['POST'])
def search():
    form = SearchForm()
    posts = Posts.query
    if form.validate_on_submit():
        # Get data from submitted form
        post.searched = form.searched.data
        # Query the Database 
        posts = posts.filter(Posts.content.like('%' + post.searched + '%'))
        posts = posts.order_by(Posts.title).all()
        return render_template(
            "search.html",
            form=form,
            searched=post.searched,
            posts=posts
            )