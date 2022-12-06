from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_mail import Mail
# from flask_bootstrap import Bootstrap
# from flask_script import Manager


db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
# bootstrap = Bootstrap()
# manager = Manager()
# Add CKEditor
ckeditor = CKEditor()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
