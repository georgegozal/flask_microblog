from venv import create
from flask import Flask, flash,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_ckeditor import CKEditor
import os




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://dbuser:mypassword@localhost:5432/users'
app.config['SECRET_KEY'] = "secret_key"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app,db)
# Add CKEditor
ckeditor = CKEditor(app)

from microblog.posts.views import posts
from microblog.auth.views import auth
app.register_blueprint(posts)
app.register_blueprint(auth)

from microblog.auth.models import Users
from microblog.posts.models import Posts

if not os.path.exists('users.db'):
    db.create_all(app=app)
    print('Created Database!')


