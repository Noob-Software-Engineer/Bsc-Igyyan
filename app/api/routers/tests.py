from fastapi import HTTPException
from flask import Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_pydantic import validate
from pymongo import ASCENDING, DESCENDING
from pymongo.collection import Collection

from app.api.common.common import get_curr_time, oid
from app.api.config.config import LocalConfig
from app.api.models.test import (
    CreateTestModel,
    TestModel,
    TestModelSearchParams,
    UpdateTestModel,
)
from app.api.models.user import UserData
from app.create_app import app, pymongo

tests: Collection = pymongo.db[LocalConfig.TEST_COLL]
# Create a unique index on the 'field_to_index' field
# tests.create_index([("name", 1)], unique=True)

test_bp = Blueprint("tests", __name__)


@test_bp.route("/", methods=["POST"])
@jwt_required()
@validate(response_by_alias=False, on_success_status=201)
def create_test(body: CreateTestModel):
    user = UserData(**get_jwt_identity())
    if not body.creator_id:
        body.creator_id = user.id
    body.created_by = body.last_updated_by = user.signature
    body.last_updated_at = body.created_at = get_curr_time()
    test_id = tests.insert_one(body.to_json()).inserted_id
    test = tests.find_one({"_id": test_id})
    return TestModel(**test)


@test_bp.route("/", methods=["GET"])
@jwt_required()
@validate(response_by_alias=False)
def search_test(query: TestModelSearchParams):
    user = UserData(**get_jwt_identity())
    filter_criteria = query.get_criteria()
    order = ASCENDING if query.order == "asc" else DESCENDING
    test_docs = (
        tests.find(filter_criteria).sort(query.sort_by, order).limit(query.limit)
    )
    total_count = tests.count_documents(filter_criteria)
    response = [TestModel(**doc).to_json() for doc in test_docs]

    return {"tests": response, "total_count": total_count}


@test_bp.route("/<test_id>", methods=["PATCH"])
@jwt_required()
@validate(response_by_alias=False)
def update_test_by_id(test_id: str, body: UpdateTestModel):
    user = UserData(**get_jwt_identity())
    body.last_updated_at = get_curr_time()
    body.last_updated_by = user.signature
    updates = body.dict(exclude_none=True, exclude_defaults=True)
    test = tests.find_one_and_update(
        {"_id": oid(test_id)}, {"$set": updates}, return_document=True
    )
    if test:
        return TestModel(**test)
    raise HTTPException(status_code=404, detail="No test document found")


@test_bp.route("/<test_id>", methods=["GET"])
@jwt_required()
@validate(response_by_alias=False)
def get_test_by_id(test_id: str):
    user = UserData(**get_jwt_identity())
    test = tests.find_one({"_id": oid(test_id)})
    if test:
        return TestModel(**test)
    app.logger.error(f"No test document find for {test_id}")
    raise HTTPException(status_code=404, detail="No test document found")


@test_bp.route("/<test_id>", methods=["DELETE"])
@jwt_required()
@validate(on_success_status=201)
def delete_test_by_id(test_id: str):
    count = tests.delete_one({"_id": oid(test_id)}).deleted_count
    if count == 0:
        app.logger.error(f"No test document find for {test_id}")
        raise HTTPException(status_code=404, detail="No test document found")
