import os
import tempfile

import pytest
from app import create_app
from app.commands.commands import create_users ,init_db, create_admin_user
from app.config import PROJECT_ROOT


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app()
    app.config.update(
        {
        'TESTING': True,
        # 'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + db_path + '.sqlite',
        'WTF_CSRF_ENABLED': False
    })

    # with app.app_context():
    #     init_db()
    #     create_users()
    #     create_admin_user()

    yield app

    # os.close(db_fd)
    # os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()



