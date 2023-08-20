from pydantic import Field
from app.api.common.common import PyObjectId, Encoder, User
from enum import Enum
from datetime import datetime
from typing import Optional


class Role(Enum):
    STUDENT = "student"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"


class CreateUser(Encoder):
    name: str
    email: str
    password: str
    role: Role
    created_at: Optional[datetime]
    last_updated_at: Optional[datetime]


class UserData(CreateUser):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    @property
    def signature(self):
        return User(id=self.id, display_name=self.name)


class GetUser(Encoder):
    name: str
    password: str
