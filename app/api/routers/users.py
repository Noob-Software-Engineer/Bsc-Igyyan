from flask import Blueprint, request, jsonify, abort
from app.api.models.user import CreateUser, GetUser, User
from pymongo.collection import Collection, ReturnDocument
from app.api.config.config import LocalConfig
from app.create_app import pymongo, app
from flask_pydantic import validate
from flask_jwt_extended import create_access_token

users: Collection = pymongo.db[LocalConfig.USER_COLL]
# Create a unique index on the 'field_to_index' field
users.create_index([("name", 1)], unique=True)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
@validate()
def register_user(body: CreateUser):
    # Handle user registration using Beanie User model
    users.insert_one(body.to_json())
    return jsonify({"user": body.to_json()})


@auth_bp.route("/login", methods=["POST"])
@validate()
def login(body: GetUser):
    user = users.find_one(body.to_json())
    if user:
        # Create a JWT token
        access_token = create_access_token(identity=User(**user).to_json())
        return jsonify({"access_token": access_token}), 200
    app.logger(f"No user found for {body.to_json()}")
    abort(404, description="No user found with given details")
