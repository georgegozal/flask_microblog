import click
from flask.cli import with_appcontext
from app.extensions import db
from app.auth.models import User
from werkzeug.security import generate_password_hash


@click.command('make_admin')
@with_appcontext
def create_admin_user():
    admin_user = User(
        username='admin',
        name='Admin',
        email='admin@gmail.com',
        password_hash=generate_password_hash('admin', 'sha256'),
        role='admin'
            )
    try:
        db.session.add(admin_user)
        db.session.commit()
        click.echo('Admin has been added!')
    except Exception as e:
        click.echo(e)


users = [
    {
        'username': 'user1',
        'name': 'user1',
        'email': 'user1@gmail.com',
        'password_hash': 'user11'
    },
    {
        'username': 'user2',
        'name': 'user2',
        'email': 'user2@gmail.com',
        'password_hash': 'user22'
    },
    {
        'username': 'user3',
        'name': 'user3',
        'email': 'user3@gmail.com',
        'password_hash': 'user3'
    },
]


@click.command('create_users')
@with_appcontext
def create_users():
    for user in users:
        new_user = User(
            username=user['username'],
            name=user['name'],
            email=user['email'],
            password_hash=generate_password_hash(
                user['password_hash'], 'sha256'),
            )
        try:
            db.session.add(new_user)
            db.session.commit()
            click.echo(f'User {new_user.username} has been added!')
        except Exception as e:
            click.echo(e)


@click.command('init_db')
@with_appcontext
def init_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    click.echo("Created database")
