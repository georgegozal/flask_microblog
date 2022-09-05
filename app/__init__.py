from flask import Flask, flash,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_admin import Admin
# from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.menu import MenuLink
from microblog.commands.commands import create_test_user
from microblog.config import Config,db,basedir
import os


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app,db)

# Add CKEditor
ckeditor = CKEditor(app)

from microblog import views
from microblog.posts.views import post_view
from microblog.auth.views import auth
app.register_blueprint(post_view, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')


from microblog.auth.models import User, UserView
from microblog.posts.models import Posts,Like,Comments,PostView,CommentView


# if not os.path.exists('user.db'):
#     db.create_all(app=app)
#     print('Created Database!')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

admin = Admin(app)
# admin.add_view(ModelView(User, db.session))
admin.add_view(UserView(User,db.session))
admin.add_view(PostView(Posts, db.session))
admin.add_view(CommentView(Comments, db.session))
admin.add_view(FileAdmin(basedir + '/static/uploads', name='Static Files'))
#https://flask-admin.readthedocs.io/en/latest/api/mod_contrib_fileadmin/

admin.add_link(MenuLink(name="Return Home",url='/posts'))

#add cli commands
app.cli.add_command(create_test_user)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
