import click
from flask.cli import with_appcontext
from microblog.config import db
from microblog.auth.models import User
from werkzeug.security import generate_password_hash

@click.command('make_admin')
@with_appcontext
def create_test_user():
    admin_user = User(
        username='Admin',
        name='name',
        email='asldkjads@gmail.com',
        password_hash=generate_password_hash('admin', 'sha256'),
        role='admin'
        )
    try:
        db.session.add(admin_user)
        db.session.commit()
        click.echo('Admin has been added!')
    except Exception as e:
        click.echo(e)
