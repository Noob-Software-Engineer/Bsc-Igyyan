from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_pydantic import validate
from pymongo import ASCENDING, DESCENDING
from pymongo.collection import Collection

from app.api.common.common import get_curr_time, oid
from app.api.config.config import LocalConfig
from app.api.models.post import (
    CreatePostModel,
    PostModel,
    PostModelSearchParams,
    UpdatePostModel,
)
from flask import current_app as app
from app.api.models.user import UserData
from app.create_app import mongo

posts_coll: Collection = mongo.db[LocalConfig.POST_COLL]

post_bp = Blueprint("posts", __name__)


@post_bp.route("/", methods=["POST"])
@jwt_required()
@validate(response_by_alias=False, on_success_status=201)
def create_post(body: CreatePostModel):
    user = UserData(**get_jwt_identity())
    if not body.creator_id:
        body.creator_id = user.id
    body.created_by = body.last_updated_by = user.signature
    body.last_updated_at = body.created_at = get_curr_time()
    post_id = posts_coll.insert_one(body.to_bson()).inserted_id
    if post_id:
        post = posts_coll.find_one({"_id": post_id})
        return PostModel(**post)
    return jsonify({"detail": "Post document could not be stored"}), 500


@post_bp.route("/", methods=["GET"])
@jwt_required()
@validate(response_by_alias=False)
def search_post(query: PostModelSearchParams):
    user = UserData(**get_jwt_identity())
    filter_criteria = query.get_criteria()
    order = ASCENDING if query.order == "asc" else DESCENDING
    test_docs = (
        posts_coll.find(filter_criteria)
        .sort(query.sort_by, order)
        .skip(query.offset)
        .limit(query.limit)
    )
    total_count = posts_coll.count_documents(filter_criteria)
    response = [PostModel(**doc).to_json() for doc in test_docs]

    return {"tests": response, "total_count": total_count}


@post_bp.route("/<post_id>", methods=["PATCH"])
@jwt_required()
@validate(response_by_alias=False)
def update_post_by_id(post_id: str, body: UpdatePostModel):
    user = UserData(**get_jwt_identity())
    body.last_updated_at = get_curr_time()
    body.last_updated_by = user.signature
    updates = body.dict(exclude_none=True, exclude_defaults=True)
    post = posts_coll.find_one_and_update(
        {"_id": oid(post_id)}, {"$set": updates}, return_document=True
    )
    if post:
        return PostModel(**post)
    return jsonify({"detail": "No post document found"}), 404


@post_bp.route("/<post_id>", methods=["GET"])
@jwt_required()
@validate(response_by_alias=False)
def get_post_by_id(post_id: str):
    user = UserData(**get_jwt_identity())
    post = posts_coll.find_one({"_id": oid(post_id)})
    if post:
        return PostModel(**post)
    app.logger.error(f"No post document find for {post_id}")
    return jsonify({"detail": "No post document found"}), 404


@post_bp.route("/<post_id>", methods=["DELETE"])
@jwt_required()
@validate()
def delete_post_by_id(post_id: str):
    count = posts_coll.delete_one({"_id": oid(post_id)}).deleted_count
    if count == 0:
        app.logger.error(f"No post document find for {post_id}")
        return jsonify({"detail": "No post document found"}), 404
    return jsonify({"detail": "Post document deleted"}), 200
