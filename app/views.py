from flask import render_template
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from microblog import app
from microblog.posts.forms import SearchForm

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

@app.route('/')
def index():
    return render_template(
        'home.html'
    )


@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)