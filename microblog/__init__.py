from venv import create
from flask import Flask, flash,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_ckeditor import CKEditor
import os




app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://dbuser:mypassword@localhost:5432/microblog'
app.config['SECRET_KEY'] = "secret_key"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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


from microblog.auth.models import Users
from microblog.posts.models import Posts,Like,Comments


if not os.path.exists('users.db'):
    db.create_all(app=app)
    print('Created Database!')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))
