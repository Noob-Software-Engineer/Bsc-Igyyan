from flask import Blueprint, Response, abort
from flask import current_app as app
from flask import jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_pydantic import validate
from pymongo.collection import Collection
from pymongo import ASCENDING, DESCENDING

from app.api.common.common import get_curr_time, PyObjectId
from app.api.config.config import LocalConfig
from app.api.models.user import CreateUser, GetUser, UpdateUser, UserModel, SearchUser
from app.create_app import mongo

users_coll: Collection = mongo.db[LocalConfig.USER_COLL]
# Create a unique index on the 'field_to_index' field
users_coll.create_index("name", unique=True)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
@validate()
def register_user(body: CreateUser):
    body.validate_super_admin()
    body.last_updated_at = body.created_at = get_curr_time()
    user_id = users_coll.insert_one(body.to_bson()).inserted_id
    user = users_coll.find_one({"_id": user_id})
    return UserModel(**user).to_json()


@auth_bp.route("/login", methods=["POST"])
@validate()
def login(body: GetUser):
    user = users_coll.find_one(body.to_json())
    if user:
        # Create a JWT token
        access_token = create_access_token(
            identity=UserModel(**user).to_json(by_alias=True)
        )
        return jsonify({"access_token": access_token}), 200
    app.logger.error(f"No user found for {body.to_json()}")
    return jsonify({"detail": "No user found"}), 404


@auth_bp.route("/<user_id>", methods=["PATCH"])
@jwt_required()
@validate()
def update_user(user_id: PyObjectId, body: UpdateUser):
    current_user = UserModel(**get_jwt_identity())
    body.validate_role_change(user_id, current_user)
    body.validate_name_change(user_id, current_user)
    body.last_updated_at = get_curr_time()
    body.last_updated_by = current_user.signature
    updates = body.dict(exclude_none=True, exclude_defaults=True)
    user = users_coll.find_one_and_update(
        {"_id": user_id}, {"$set": updates}, return_document=True
    )
    if user:
        return UserModel(**user)
    app.logger.error(f"No user found for {user_id}")
    return jsonify({"detail": "No user found"}), 404


@auth_bp.route("", methods=["GET"])
@validate()
def search_user(query: SearchUser):
    current_user = UserModel(**get_jwt_identity())
    filter_criteria = query.get_criteria(current_user)
    order = ASCENDING if query.order == "asc" else DESCENDING
    user_docs = (
        users_coll.find(filter_criteria)
        .sort(query.sort_by, order)
        .skip(query.offset)
        .limit(query.limit)
    )
    total_count = users_coll.count_documents(filter_criteria)
    response = [UserModel(**doc).to_json() for doc in user_docs]

    return {"posts": response, "total_count": total_count}
