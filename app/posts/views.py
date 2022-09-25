from xml.dom.minidom import Attr
from flask import flash,url_for, redirect,render_template,Blueprint, request,jsonify
from flask_login import login_user, login_required, current_user
from .models import Posts,Comments, Like
from app.auth.models import User
from .forms import PostForm,SearchForm,CommentForm
from app.extensions import db

post_view = Blueprint('post',__name__,template_folder="templates/posts")


# view all posts
@post_view.route('/')
def list():
    # current_user = current_user.followed_posts()
    posts = Posts.query.order_by(Posts.date_posted.desc()).all()
    # posts = User.query.get_or_404(current_user.id).followed_posts()
    like = Like.query.all()
    return render_template(
        'list.html',
        posts=posts,
        like=like)

# view one post # add  comments
@post_view.route('/posts/<int:id>',methods=['GET','POST'])
def post(id):
    form = CommentForm()
    post = Posts.query.get_or_404(id)
    comments = Comments.query.filter_by(post_id=post.id).order_by(Comments.date_posted.desc()).all()
    like = Like.query.filter_by(post_id=post.id).all()
    try:
        can_like = Like.query.filter_by(author=current_user.id,post_id=post.id).count() > 0
    except AttributeError:
        can_like = False


    if form.validate_on_submit():
        try:
            content = form.content.data
            new_comment = Comments(
                content = content,
                poster_id = current_user.id,
                post_id = post.id
            )


            db.session.add(new_comment)
            db.session.commit()
            flash('Comment has been added!',category='success')
            return redirect(url_for('post.post',id=post.id))
        except AttributeError:
            flash('Please Log In To Leave a Comment!',category='error')
    return render_template(
        'post.html',
        post = post,
        comments=comments,
        form=form,
        like=like,
        can_like=can_like
    )

# Add Post Page
@post_view.route('/add-post',methods=['GET','POST'])
def add():
    form = PostForm()

    if form.validate_on_submit():
        post = Posts(
            title = form.title.data,
            content = form.content.data,
            # slug = form.slug.data,
            poster_id = current_user.id
        )
        # Clear the Form
        form.title.data = ''
        form.content.data = ''
        # form.slug.data = ''

        # Add post data to database
        db.session.add(post)
        db.session.commit()
        # return a message
        flash('Blog Post Submitted Successfully!',category='success')
        return redirect( url_for('post.post', id=post.id))
    return render_template(
        'add_post.html',
        form=form
    )

# edit post
@post_view.route('/posts/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        # post.slug = form.slug.data
        post.content = form.content.data
        # db.session.add(post)
        db.session.commit()
        flash('Post has been updated',category='success')
        return redirect(url_for('post.post', id=post.id))
    
    if current_user.id == post.poster_id:
        # if form.method is not post. bring post data from database
        form.title.data = post.title
        # form.slug.data = post.slug
        form.content.data = post.content
        return render_template(
            'edit.html',
            form = form,
            post=post
        )
    else:
        flash("You Aren`t Authorised To Edit This Post...",category='error')
        return redirect(url_for('post.list'))

# delete post
@post_view.route('/posts/delete/<int:id>')
def delete(id):
    
    post = Posts.query.get_or_404(id)
    if int(post.poster.id) == current_user.id:
        try:
            db.session.delete(post)
            db.session.commit()
            flash('Post has been deleted',category='success')
            return redirect(url_for('post.list'))
        except:
            flash('there was a problem deleting a post',category='error')
    else:
        flash("You Aren`t Authorized To Delete That Post!",category='error')
        return redirect(url_for('post.list'))

@post_view.route('/post/<post_id>/comments/update/<comment_id>',methods=['POST','GET'])
def update_comment(comment_id,post_id):
    form = CommentForm()
    comment = Comments.query.get_or_404(comment_id)
    post = Posts.query.get_or_404(post_id)
    comments = Comments.query.filter_by(post_id=post.id).order_by(Comments.date_posted.desc()).all()
    like = Like.query.filter_by(post_id=post.id).all()

    if form.validate_on_submit():
        comment.content = form.content.data
        db.session.commit()
        flash('Comment has been added!',category='success')
        return redirect(url_for(
            'post.post',
            id=post.id))
    if current_user.id == comment.commenter.id:
        form.content.data = comment.content

    return render_template(
        'edit_comment.html',
        post = post,
        comments=comments,
        comment=comment,
        form=form,
        like=like
    )


@post_view.route('/delete/<post_id>/<comment_id>')
@login_required
def delete_comment(post_id,comment_id):
    comment = Comments.query.get_or_404(comment_id)
    if int(comment.commenter.id) == current_user.id:
        try:
            db.session.delete(comment)
            db.session.commit()
            flash("Comment has been deleted",category='success')
            return redirect(url_for('post.post', id=post_id))
        except:
            flash('there was a problem deleting the comment',category='error')
    else:
        flash("You Aren`t Authorized To Delete That Comment!",category='error')
        return redirect(url_for('post.post', id=post_id))

@post_view.route('/posts/<id>/like')
@login_required
def like(id):
    # if request.method['POST']:
    post = Posts.query.get_or_404(id)
    like = Like.query.filter_by(
        author=current_user.id, post_id=id).first()

    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id,post_id=id)
        db.session.add(like)
        db.session.commit()
    return redirect(url_for('post.post', id=post.id))
    # return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes)})

@post_view.route('/post/<post_id>/comments/<id>/like')
def like_comment(post_id,id):
    comment = Comments.query.get_or_404(id)
    try:
        like = Like.query.filter_by(
        author=current_user.id, comment_id=id).first()
    except AttributeError:
        like = False

    if not comment:
        return jsonify({'error': 'Comment does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        try:
            like = Like(author=current_user.id,comment_id=id)
            db.session.add(like)
            db.session.commit()
        except AttributeError:
            flash("You Can`t Like Before Log In",category='error')
    return redirect(url_for('post.post', id=post_id))


@post_view.route('/search',methods=['POST'])
def search():
    form = SearchForm()
    posts = Posts.query
    if form.validate_on_submit():
        # Get data from submitted form
        post.searched = form.searched.data
        # Query the Database 

        # posts_by_content = posts.filter(Posts.content.like('%' + post.searched + '%'))
        # posts_by_title = posts.filter(Posts.title.like('%' + post.searched + '%'))

        # posts_by_content = posts.order_by(Posts.title).all()
        # posts_by_title = posts.order_by(Posts.title).all()
        # return render_template(
        #     "search.html",
        #     form=form,
        #     searched=post.searched,
        #     posts_by_content=posts_by_content,
        #     posts_by_title = posts_by_title
        #     )
        posts = posts.filter(Posts.content.like('%' + post.searched + '%'))
        posts = posts.order_by(Posts.title).all()
        return render_template(
            "search.html",
            form=form,
            searched=post.searched,
            posts=posts
            )