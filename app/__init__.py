from flask import Flask,render_template
from flask_admin import Admin
from flask_admin.menu import MenuLink
from app.config import Config,PROJECT_ROOT
from app.auth.models import User, UserView,FileView
from app.posts.models import Posts,Like,Comments,PostView,CommentView
from app.commands.commands import create_test_user #, init_db_command, populate_movies_command
from app.extensions import db, migrate, login_manager,ckeditor
# from app.api import api
from app import views
from app.posts.views import post_view
from app.auth.views import auth
# from app.views import app_view
from app.posts.forms import SearchForm


BLUEPRINTS = [post_view, auth]
COMMANDS = [create_test_user]#init_db_command, populate_movies_command]


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    register_commands(app)
    register_extensions(app)
    register_blueprints(app)
    register_admin_panel(app)

    # Search 
    @app.context_processor
    def base():
        searchform = SearchForm()
        return dict(searchform=searchform)

    # Invalid URL
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    # Internal Server Error
    @app.errorhandler(500)
    def page_not_found(e):
        return render_template('500.html'), 500

    return app

def register_extensions(app):

    # Setup Flask-SQLAlchemy
    db.init_app(app)

    # Setup Flask-Migrate
    migrate.init_app(app, db)

    # Setup Flask-CKEditor
    ckeditor.init_app(app)

    #Flask-RESTful
    # api.init_app(app)

    # Flask-Login
    @login_manager.user_loader
    def load_user(id_):
        return User.query.get(id_)

    login_manager.init_app(app)


def register_blueprints(app):

    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint)


def register_commands(app):

    for command in COMMANDS:
        app.cli.add_command(command)


def register_admin_panel(app):
    admin = Admin(app)
    admin.add_view(UserView(User,db.session))
    admin.add_view(PostView(Posts, db.session))
    admin.add_view(CommentView(Comments, db.session))
    admin.add_view(FileView(PROJECT_ROOT + '/static/uploads', name='Static Files'))
    #https://flask-admin.readthedocs.io/en/latest/api/mod_contrib_fileadmin/

    admin.add_link(MenuLink(name="Return Home",url='/posts'))





