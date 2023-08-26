from pydantic import Field
from app.api.common.common import PyObjectId, Encoder, User
from enum import Enum
from datetime import datetime
from typing import Optional
from app.api.config.config import LocalConfig
from fastapi import HTTPException


class Role(str, Enum):
    STUDENT = "student"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"


class CreateUser(Encoder):
    name: str
    display_name: str = Field(
        ..., description="User's can have any duplicate name to have anonymity"
    )
    email: str
    password: str
    role: Role
    created_at: Optional[datetime]
    last_updated_at: Optional[datetime]

    def validate_super_admin(self):
        if self.role == Role.SUPERADMIN and self.name != LocalConfig.SUPER_ADMIN:
            raise HTTPException(status_code=422, detail="Pass a correct identity")


class UserModel(CreateUser):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    @property
    def signature(self):
        return User(id=self.id, display_name=self.name)


class GetUser(Encoder):
    name: str
    password: str


class UpdateUser(Encoder):
    role: Optional[Role]
    display_name: Optional[str]
    last_updated_by: Optional[User]
    last_updated_at: Optional[datetime]

    def validate_role_change(self, user_id: PyObjectId, current_user: UserModel):
        if self.role:
            if (
                self.role in [Role.SUPERADMIN, Role.ADMIN]
                and current_user.role != Role.SUPERADMIN
            ) or ():
                raise HTTPException(
                    status_code=403, detail="Not authorized to change user role"
                )
            elif (current_user.id != user_id) and (
                current_user.role != Role.SUPERADMIN
            ):
                raise HTTPException(
                    status_code=403, detail="Not authorized to change other user's role"
                )

    def validate_name_change(self, user_id: PyObjectId, current_user: UserModel):
        if self.display_name and (user_id != current_user.id):
            raise HTTPException(
                status_code=403,
                detail="Not authorized to change other user's display name",
            )
