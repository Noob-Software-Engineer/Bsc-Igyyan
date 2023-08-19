# models/user.py
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from app.api.common.common import PyObjectId
from enum import Enum
from datetime import datetime
from typing import Optional
from bson.objectid import ObjectId


class Role(Enum):
    STUDENT = "student"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"


class Encoder(BaseModel):
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True, by_alias=False)

    def to_bson(self):
        data = self.model_dump(by_alias=True, exclude_none=True)
        if data.get("_id") is None:
            data.pop("_id", None)
        return data


class CreateUser(Encoder):
    name: str
    email: str
    password: str
    role: Role
    created_at: Optional[datetime]
    last_updated_at: Optional[datetime]


class User(CreateUser):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")


class GetUser(Encoder):
    name: str
    password: str
