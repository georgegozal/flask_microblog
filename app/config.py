from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
basedir = os.path.abspath(os.path.dirname(__file__))

def return_db(env='DEV'):
    if env == 'PROD':
        pg_user = 'dbuser'
        pg_pass = 'mypassword'
        pg_db = 'microblog'
        pg_host = 'localhost'
        pg_port = 5432
        return f'postgresql+psycopg2://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}'
    else:
        return 'sqlite:///users.db'



class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'asd;lkajs-90 as;doaksdasd02 ;;/A'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'users.db')
    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://dbuser:mypassword@localhost:5432/microblog'
    # CKEDITOR_FILE_UPLOADER = 'static/upload'
    # https://flask-ckeditor.readthedocs.io/en/latest/plugins.html
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # if os.environ.get('DEBUG' == '1'):
    #     SQLALCHEMY_DATABASE_URI = return_db()
    # else:
    #     SQLALCHEMY_DATABASE_URI = return_db('PROD')




