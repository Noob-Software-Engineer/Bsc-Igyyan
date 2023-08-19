from datetime import datetime, timedelta
from typing import Optional
from jose.jwt import encode
from bson.errors import InvalidId
from bson.objectid import ObjectId
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from app.api.config.config import LocalConfig


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


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class User(BaseModel):
    id: PyObjectId = Field(...)
    display_name: Optional[str]


def get_curr_time():
    current_time = datetime.now()
    milliseconds = (int(current_time.microsecond / 1000)) * 1000
    current_time = current_time.replace(microsecond=milliseconds)
    return current_time


def oid(x):
    try:
        return ObjectId(x)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ObjectId")


def get_student_token():
    payload = dict(
        id="64e0bc377d008754b4a56f55",
        name="ashraf",
        email="ashraf@gmail.com",
        password="1234",
        role="student",
    )
    return encode(
        {
            "sub": payload,  # Replace with the actual subject (user) identifier
            "exp": datetime.utcnow() + timedelta(hours=1),  # Token expiration time
        },
        key=LocalConfig.JWT_SECRET_KEY,
    )
