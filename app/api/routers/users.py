from flask import Blueprint, jsonify, abort, Response
from app.api.models.user import CreateUser, GetUser, UserData
from pymongo.collection import Collection
from app.api.config.config import LocalConfig
from app.create_app import mongo
from flask_pydantic import validate
from flask_jwt_extended import create_access_token
from app.api.common.common import get_curr_time
from flask import current_app as app

users: Collection = mongo.db[LocalConfig.USER_COLL]
# Create a unique index on the 'field_to_index' field
users.create_index("name", unique=True)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
@validate()
def register_user(body: CreateUser):
    body.last_updated_at = get_curr_time()
    body.created_at = get_curr_time()
    # Handle user registration using Beanie User model
    users.insert_one(body.to_bson())
    return jsonify({"user": body.to_json()})


@auth_bp.route("/login", methods=["POST"])
@validate()
def login(body: GetUser):
    user = users.find_one(body.to_json())
    if user:
        # Create a JWT token
        access_token = create_access_token(identity=UserData(**user).to_json())
        return jsonify({"access_token": access_token}), 200
    app.logger.error(f"No user found for {body.to_json()}")
    abort(Response(status=404, response="No user found"))
