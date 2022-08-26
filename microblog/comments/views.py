from crypt import methods
from flask import Flask, flash,url_for, redirect,render_template,Blueprint, request
from flask_login import login_user, LoginManager, login_required, logout_user, current_user

from microblog.comments.models import Comments
from microblog import db

comments = Blueprint('comments',__name__,template_folder="templates/comments")

# delete comment
@comments.route('/comments/delete/<int:id>')
def delete(id):
    pass
    # comment = Comments.query.get_or_404(id)
    # if int(comment.poster.id) == current_user.id:
    #     try:
    #         db.session.delete(post)
    #         db.session.commit()
    #         flash('Post has been deleted',category='success')
    #         return redirect(url_for('posts.list'))
    #     except:
    #         flash('there was a problem deleting a post',category='error')
    # else:
    #     flash("You Aren`t Authorized To Delete That Post!",category='error')
    #     return redirect(url_for('posts.list'))