import os
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


def return_db(env='DEV'):
    if env == 'PROD':
        pg_user = 'dbuser'
        pg_pass = 'mypassword'
        pg_db = 'microblog'
        pg_host = 'localhost'
        pg_port = 5432
        return f'postgresql+psycopg2://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}'
    else:
        return 'sqlite:///db.sqlite'


class Config(object):

    PROJECT_NAME = "flask_microblog"
    PROJECT_ROOT = PROJECT_ROOT
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(PROJECT_ROOT, 'db.sqlite')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'asd;lkajs-90 as;doaksdasd02 ;;/A'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = os.environ.get('EMAIL_ADDRESS') or 'microblog@gmail.com'
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('email') or 'microblog@gmail.com'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    if os.environ.get('FLASK_ENV') == 'production':
        # SQLALCHEMY_DATABASE_URI = return_db('PROD')
        FLASK_DEBUG=False
        FLASK_ENV='production'

    else:
        # SQLALCHEMY_DATABASE_URI = return_db()
        FLASK_DEBUG=True
        FLASK_ENV='development'
