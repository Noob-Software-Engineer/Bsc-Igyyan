from datetime import datetime
import os

from pymongo.collection import Collection, ReturnDocument

from flask import Flask, request, url_for, jsonify
from flask_pymongo import PyMongo

from app.api.config.config import LocalConfig
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)


def create_app():
    # Configure Flask & Flask-PyMongo:
    app = Flask(__name__)
    # app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    app.config["MONGO_URI"] = LocalConfig.MONGO_URI

    pymongo = PyMongo(app)
    # Configure JWT settings
    app.config[
        "JWT_SECRET_KEY"
    ] = "your-secret-key"  # Change this to a strong, random secret key
    jwt = JWTManager(app)
    return app, pymongo, jwt


app, pymongo, jwt = create_app()
