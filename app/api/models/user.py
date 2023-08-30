from pydantic import Field, EmailStr, AnyHttpUrl
from app.api.common.common import PyObjectId, Encoder, User
from enum import Enum
from datetime import datetime
from typing import Optional, Literal, Any
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
    email: EmailStr
    password: str
    role: Role
    social_link: AnyHttpUrl
    is_public: bool = Field(
        default=True, description="Indicate whther user is publicaly avaiable or not"
    )
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


class SearchUser(Encoder):
    display_name: Optional[str]
    sort_by: Literal["created_at", "last_updated_at"] = "last_updated_at"
    order: Literal["asc", "desc"] = "desc"
    offset: int = Field(default=0, ge=0)
    limit: int = Field(
        default=LocalConfig.DEFAULT_ITEMS_PER_PAGE,
        le=LocalConfig.MAX_ITEMS_PER_PAGE,
        ge=0,
    )

    def get_criteria(self, current_user: UserModel):
        filter_criteria: dict[str, Any] = {}
        if current_user.role == Role.STUDENT:
            filter_criteria["is_public"] = True
        if self.display_name:
            filter_criteria["display_name"] = {
                "$regex": f"^.*{self.display_name}.*",
                "$options": "i",
            }
        return filter_criteria
