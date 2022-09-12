from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_ckeditor import CKEditor

db = SQLAlchemy()
migrate = Migrate()
# Add CKEditor
ckeditor = CKEditor()
login_manager = LoginManager()
login_manager.login_view = "auth.login"