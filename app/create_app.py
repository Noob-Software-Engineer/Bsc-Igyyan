import logging

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo

from app.api.config.config import LocalConfig

logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s [%(levelname)s] - %(message)s"
)


def create_app(set_unit_test_config=False):
    # Configure Flask & Flask-PyMongo:
    app = Flask(__name__)
    # app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    # if set_unit_test_config:
    app.config["MONGO_URI"] = LocalConfig.MONGO_TEST_URI
    # else:
    # app.config["MONGO_URI"] = LocalConfig.MONGO_URI
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = LocalConfig.JWT_ACCESS_TOKEN_EXPIRES
    app.config[
        "JWT_SECRET_KEY"
    ] = LocalConfig.JWT_SECRET_KEY  # Change this to a strong, random secret key
    jwt = JWTManager(app)

    pymongo = PyMongo(app)
    # Configure JWT settings
    return app, pymongo, jwt


app, pymongo, jwt = create_app()
