from flask import Flask
from flask_admin import Admin
from flask_admin.menu import MenuLink
from app.config import Config
from app.views.auth.models import UserView, FileView, User
from app.views.posts.models import Posts, Like, Comments, PostView, CommentView
from app.commands import add_admin_command, init_db_command
from app.extensions import db, migrate, login_manager, ckeditor, mail  # bootstrap  # manager
from app.views.api.auth import api
from app.views.api.posts import api_posts
from app.views.posts.views import post_view
from app.views.auth.views import auth
from app.views.followers.views import followers
from app.errors import errors


BLUEPRINTS = [post_view, auth, followers, api, api_posts, errors]
COMMANDS = [add_admin_command, init_db_command]


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    register_commands(app)
    register_extensions(app)
    register_blueprints(app)
    register_admin_panel(app)

    @app.shell_context_processor
    def make_shell_context():
        return {
            "db": db,
            "Users": User,
            "Posts": Posts,
            "Comments": Comments,
            "Likes": Like,
            "config": Config,
        }
    return app


def register_extensions(app):

    # Setup Flask-SQLAlchemy
    db.init_app(app)

    # Setup Flask-Migrate
    migrate.init_app(app, db)

    # Setup Flask-Mail
    mail.init_app(app)

    # bootstrap.init_app(app)

    # manager.init_app(app)

    # Setup Flask-CKEditor
    ckeditor.init_app(app)

    # Flask-RESTful
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
    admin.add_view(UserView(User, db.session))
    admin.add_view(PostView(Posts, db.session))
    admin.add_view(CommentView(Comments, db.session))
    admin.add_view(FileView(
        Config.PROJECT_ROOT + '/static/uploads', name='Static Files'))
    # https://flask-admin.readthedocs.io/en/latest/api/mod_contrib_fileadmin/
    admin.add_link(MenuLink(name="Return Home", url='/'))
