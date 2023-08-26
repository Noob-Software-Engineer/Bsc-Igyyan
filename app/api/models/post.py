from pydantic import Field
from app.api.common.common import PyObjectId, Encoder, User
from enum import Enum
from datetime import datetime
from typing import Optional, Literal, Any
from app.api.config.config import LocalConfig
from app.api.models.user import UserModel, Role


class PostTag(str, Enum):
    JOB = "job"
    INTERNSHIP = "internship"
    APTITUDE = "aptitude"
    PROGRAMMING = "programming"
    INTERVIEW_TIPS = "interview_tips"
    RESUME_BUILDING = "resume_building"
    CAREER_ADVICE = "career_advice"


class CreatePostModel(Encoder):
    creator_id: Optional[PyObjectId]
    title: str
    content: str
    tag: Optional[PostTag]
    created_by: Optional[User]
    created_at: Optional[datetime]
    last_updated_by: Optional[User]
    last_updated_at: Optional[datetime]


class PostModel(CreatePostModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")


class UpdatePostModel(Encoder):
    title: Optional[str]
    content: Optional[str]
    tag: Optional[PostTag]
    review: Optional[int] = Field(ge=0, le=5)
    last_updated_by: Optional[User]
    last_updated_at: Optional[datetime]


class PostModelSearchParams(Encoder):
    offset: int = Field(default=0, ge=0)
    limit: int = Field(
        default=LocalConfig.DEFAULT_ITEMS_PER_PAGE,
        le=LocalConfig.MAX_ITEMS_PER_PAGE,
        ge=0,
    )
    sort_by: Literal["created_at", "last_updated_at"] = "last_updated_at"
    order: Literal["asc", "desc"] = "desc"
    creator_id: Optional[PyObjectId]
    tag: Optional[PostTag]
    title: Optional[str]

    def get_criteria(self, current_user: UserModel):
        filter_criteria: dict[str, Any] = {}
        if current_user.role not in [Role.SUPERADMIN, Role.ADMIN]:
            self.creator_id = current_user.id
        if self.creator_id:
            filter_criteria["creator_id"] = self.creator_id
        if self.tag:
            filter_criteria["tag"] = self.tag
        if self.title:
            filter_criteria["title"] = {"$regex": f"^.*{self.title}.*", "$options": "i"}
        return filter_criteria
