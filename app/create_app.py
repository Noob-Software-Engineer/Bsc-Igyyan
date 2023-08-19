import logging

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo

from app.api.config.config import LocalConfig

logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s [%(levelname)s] - %(message)s"
)


def create_app():
    # Configure Flask & Flask-PyMongo:
    app = Flask(__name__)
    # app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    app.config["MONGO_URI"] = LocalConfig.MONGO_URI

    pymongo = PyMongo(app)
    # Configure JWT settings
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = LocalConfig.JWT_ACCESS_TOKEN_EXPIRES
    app.config[
        "JWT_SECRET_KEY"
    ] = "your-secret-key"  # Change this to a strong, random secret key
    jwt = JWTManager(app)
    return app, pymongo, jwt


app, pymongo, jwt = create_app()
