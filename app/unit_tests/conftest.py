# conftest.py

import pytest
from app.create_app import create_app

from app.api.models.user import CreateUser
from app.api.common.common import get_curr_time
from app.api.config.config import LocalConfig
from flask_pymongo import PyMongo

# from main import app


@pytest.fixture
def app():
    app = create_app(set_unit_test_config=True)  # Use the test configuration
    from app.api.routers.users import auth_bp
    from app.api.routers.tests import test_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(test_bp, url_prefix="/tests")

    yield app


@pytest.fixture
def client(app):
    with app.app_context():
        yield app.test_client()
    PyMongo(app).db[LocalConfig.USER_COLL].delete_many({})
    PyMongo(app).db[LocalConfig.TEST_COLL].delete_many({})


@pytest.fixture
def test_db(app):
    yield PyMongo(app).db


@pytest.fixture
def test_model_collection(app):
    with app.test_client() as client:
        yield client


@pytest.fixture
def setup_test_data(test_db):
    # Create and populate a testing database with data
    users = test_db[LocalConfig.USER_COLL]
    student = CreateUser(
        name="ashraf",
        email="ashraf@gmail.com",
        password="1234",
        role="student",
        display_name="ashraf",
        social_link="https://stackoverflow.com/questions/70313289/how-to-accept-urls-without-a-protocol",
        created_at=get_curr_time(),
        last_updated_at=get_curr_time(),
    )
    users.insert_many(
        [
            student.to_json(),
            # Add more test data as needed
        ]
    )
