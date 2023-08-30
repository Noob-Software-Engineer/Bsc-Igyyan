import logging

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from flask_cors import CORS

from app.api.config.config import LocalConfig

logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s [%(levelname)s] - %(message)s"
)
mongo = PyMongo()


def create_app(set_unit_test_config=False):
    app = Flask(__name__)
    CORS(app, origins="http://127.0.0.1:3000", supports_credentials=True)
    if set_unit_test_config:
        app.config["MONGO_URI"] = LocalConfig.MONGO_TEST_URI
    else:
        app.config["MONGO_URI"] = LocalConfig.MONGO_URI
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = LocalConfig.JWT_ACCESS_TOKEN_EXPIRES
    app.config[
        "JWT_SECRET_KEY"
    ] = LocalConfig.JWT_SECRET_KEY  # Change this to a strong, random secret key
    jwt = JWTManager(app)
    mongo.init_app(app)
    return app
