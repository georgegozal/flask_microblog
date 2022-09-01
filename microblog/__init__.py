from flask import Flask, flash,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_admin import Admin
# from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.menu import MenuLink
import os




app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://dbuser:mypassword@localhost:5432/microblog'
app.config['SECRET_KEY'] = "secret_key"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
projectdir = os.path.abspath(os.path.dirname(__file__))
# app.config['CKEDITOR_FILE_UPLOADER'] = 'static/upload'
# https://flask-ckeditor.readthedocs.io/en/latest/plugins.html

db = SQLAlchemy(app)
# db.init_app(app)
migrate = Migrate(app,db)

# Add CKEditor
ckeditor = CKEditor(app)

from microblog import views
from microblog.posts.views import post_view
from microblog.auth.views import auth
app.register_blueprint(post_view, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')


from microblog.auth.models import Users, UserView
from microblog.posts.models import Posts,Like,Comments,PostView,CommentView


if not os.path.exists('users.db'):
    db.create_all(app=app)
    print('Created Database!')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

admin = Admin(app)
# admin.add_view(ModelView(Users, db.session))
admin.add_view(UserView(Users,db.session))
admin.add_view(PostView(Posts, db.session))
admin.add_view(CommentView(Comments, db.session))
admin.add_view(FileAdmin(projectdir + '/static/uploads', name='Static Files'))

admin.add_link(MenuLink(name="Return Home",url='/posts'))


@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))
