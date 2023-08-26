from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_pydantic import validate
from pymongo import ASCENDING, DESCENDING
from pymongo.collection import Collection

from app.api.common.common import get_curr_time, PyObjectId
from app.api.config.config import LocalConfig
from app.api.models.post import (
    CreatePostModel,
    PostModel,
    PostModelSearchParams,
    UpdatePostModel,
)
from flask import current_app as app
from app.api.models.user import UserModel, Role
from app.create_app import mongo

posts_coll: Collection = mongo.db[LocalConfig.POST_COLL]

post_bp = Blueprint("posts", __name__)


@post_bp.route("", methods=["POST"])
@jwt_required()
@validate(response_by_alias=False, on_success_status=201)
def create_post(body: CreatePostModel):
    current_user = UserModel(**get_jwt_identity())
    if not body.creator_id:
        body.creator_id = current_user.id
    body.created_by = body.last_updated_by = current_user.signature
    body.last_updated_at = body.created_at = get_curr_time()
    post_id = posts_coll.insert_one(body.to_bson()).inserted_id
    if post_id:
        post = posts_coll.find_one({"_id": post_id})
        return PostModel(**post)
    return jsonify({"detail": "Post document could not be stored"}), 500


@post_bp.route("", methods=["GET"])
@jwt_required()
@validate(response_by_alias=False)
def search_post(query: PostModelSearchParams):
    current_user = UserModel(**get_jwt_identity())
    filter_criteria = query.get_criteria(current_user)
    order = ASCENDING if query.order == "asc" else DESCENDING
    post_docs = (
        posts_coll.find(filter_criteria)
        .sort(query.sort_by, order)
        .skip(query.offset)
        .limit(query.limit)
    )
    total_count = posts_coll.count_documents(filter_criteria)
    response = [PostModel(**doc).to_json() for doc in post_docs]

    return {"tests": response, "total_count": total_count}


@post_bp.route("/<post_id>", methods=["PATCH"])
@jwt_required()
@validate(response_by_alias=False)
def update_post_by_id(post_id: PyObjectId, body: UpdatePostModel):
    current_user = UserModel(**get_jwt_identity())
    body.last_updated_at = get_curr_time()
    body.last_updated_by = current_user.signature
    filter_criteria = {}
    filter_criteria["_id"] = post_id
    if current_user.role not in [Role.ADMIN, Role.SUPERADMIN]:
        filter_criteria["creator_id"] = current_user.id
    updates = body.dict(exclude_none=True, exclude_defaults=True)
    post = posts_coll.find_one_and_update(
        filter_criteria, {"$set": updates}, return_document=True
    )
    if post:
        return PostModel(**post)
    return jsonify({"detail": "No post document found"}), 404


@post_bp.route("/<post_id>", methods=["GET"])
@jwt_required()
@validate(response_by_alias=False)
def get_post_by_id(post_id: PyObjectId):
    current_user = UserModel(**get_jwt_identity())
    filter_criteria = {}
    filter_criteria["_id"] = post_id
    if current_user.role not in [Role.ADMIN, Role.SUPERADMIN]:
        filter_criteria["creator_id"] = current_user.id
    post = posts_coll.find_one(filter_criteria)
    if post:
        return PostModel(**post)
    app.logger.error(f"No post document find for {post_id}")
    return jsonify({"detail": "No post document found"}), 404


@post_bp.route("/<post_id>", methods=["DELETE"])
@jwt_required()
@validate()
def delete_post_by_id(post_id: PyObjectId):
    current_user = UserModel(**get_jwt_identity())
    filter_criteria = {}
    filter_criteria["_id"] = post_id
    if current_user.role not in [Role.ADMIN, Role.SUPERADMIN]:
        filter_criteria["creator_id"] = current_user.id
    count = posts_coll.delete_one(filter_criteria).deleted_count
    if count == 0:
        app.logger.error(f"No post document find for {post_id}")
        return jsonify({"detail": "No post document found"}), 404
    return jsonify({"detail": "Post document deleted"}), 200
