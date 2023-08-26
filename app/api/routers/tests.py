from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_pydantic import validate
from pymongo import ASCENDING, DESCENDING
from pymongo.collection import Collection

from app.api.common.common import get_curr_time, PyObjectId
from app.api.config.config import LocalConfig
from app.api.models.test import (
    CreateTestModel,
    TestModel,
    TestModelSearchParams,
    UpdateTestModel,
)
from flask import current_app as app
from app.api.models.user import UserModel, Role
from app.create_app import mongo

tests_coll: Collection = mongo.db[LocalConfig.TEST_COLL]
# Create a unique index on the 'field_to_index' field
# tests.create_index([("name", 1)], unique=True)

test_bp = Blueprint("tests", __name__)


@test_bp.route("", methods=["POST"])
@jwt_required()
@validate(response_by_alias=False, on_success_status=201)
def create_test(body: CreateTestModel):
    user = UserModel(**get_jwt_identity())
    if not body.creator_id:
        body.creator_id = user.id
    body.created_by = body.last_updated_by = user.signature
    body.last_updated_at = body.created_at = get_curr_time()
    test_id = tests_coll.insert_one(body.to_bson()).inserted_id
    if test_id:
        test = tests_coll.find_one({"_id": test_id})
        return TestModel(**test)
    return jsonify({"detail": "Test document could not be stored"}), 500


@test_bp.route("", methods=["GET"])
@jwt_required()
@validate(response_by_alias=False)
def search_test(query: TestModelSearchParams):
    current_user = UserModel(**get_jwt_identity())
    filter_criteria = query.get_criteria(current_user)
    order = ASCENDING if query.order == "asc" else DESCENDING
    test_docs = (
        tests_coll.find(filter_criteria)
        .sort(query.sort_by, order)
        .skip(query.offset)
        .limit(query.limit)
    )
    total_count = tests_coll.count_documents(filter_criteria)
    response = [TestModel(**doc).to_json() for doc in test_docs]

    return {"tests": response, "total_count": total_count}


@test_bp.route("/<test_id>", methods=["PATCH"])
@jwt_required()
@validate(response_by_alias=False)
def update_test_by_id(test_id: PyObjectId, body: UpdateTestModel):
    current_user = UserModel(**get_jwt_identity())
    body.last_updated_at = get_curr_time()
    body.last_updated_by = current_user.signature
    filter_criteria = {}
    filter_criteria["_id"] = test_id
    if current_user.role not in [Role.ADMIN, Role.SUPERADMIN]:
        filter_criteria["creator_id"] = current_user.id
    updates = body.dict(exclude_none=True, exclude_defaults=True)
    test = tests_coll.find_one_and_update(
        filter_criteria, {"$set": updates}, return_document=True
    )
    if test:
        return TestModel(**test)
    return jsonify({"detail": "No test document found"}), 404


@test_bp.route("/<test_id>", methods=["GET"])
@jwt_required()
@validate(response_by_alias=False)
def get_test_by_id(test_id: PyObjectId):
    current_user = UserModel(**get_jwt_identity())
    filter_criteria = {}
    filter_criteria["_id"] = test_id
    if current_user.role not in [Role.ADMIN, Role.SUPERADMIN]:
        filter_criteria["creator_id"] = current_user.id

    test = tests_coll.find_one(filter_criteria)
    if test:
        return TestModel(**test)
    app.logger.error(f"No test document find for {test_id}")
    return jsonify({"detail": "No test document found"}), 404


@test_bp.route("/<test_id>", methods=["DELETE"])
@jwt_required()
@validate()
def delete_test_by_id(test_id: PyObjectId):
    current_user = UserModel(**get_jwt_identity())
    filter_criteria = {}
    filter_criteria["_id"] = test_id
    if current_user.role not in [Role.ADMIN, Role.SUPERADMIN]:
        filter_criteria["creator_id"] = current_user.id
    count = tests_coll.delete_one(filter_criteria).deleted_count
    if count == 0:
        app.logger.error(f"No test document find for {test_id}")
        return jsonify({"detail": "No test document found"}), 404
    return jsonify({"detail": "Test document deleted"}), 200
