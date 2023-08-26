from pydantic import Field
from app.api.common.common import PyObjectId, Encoder, User
from enum import Enum
from datetime import datetime
from typing import Optional, Literal, Any
from app.api.config.config import LocalConfig
from app.api.models.user import UserModel, Role


class TestType(str, Enum):
    PLACEMENT = "Placement Test"
    PRACTICE = "Practice Test"
    MOCK = "Mock Test"
    OTHER = "Other"


class Tag(str, Enum):
    DSA = "Data Structures and Algorithms"
    DBMS = "Database Management Systems"
    OS = "Operating Systems"
    OOP = "Object-Oriented Programming"
    NETWORKING = "Computer Networking"
    AI = "Artificial Intelligence"
    ML = "Machine Learning"
    WEB_DEV = "Web Development"
    OTHER = "Other"


class CreateTestModel(Encoder):
    creator_id: Optional[PyObjectId]
    title: str
    content: str
    type: Optional[TestType]
    tag: Optional[Tag]
    review: Optional[int] = Field(ge=0, le=5)
    created_by: Optional[User]
    created_at: Optional[datetime]
    last_updated_by: Optional[User]
    last_updated_at: Optional[datetime]


class TestModel(CreateTestModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")


class UpdateTestModel(Encoder):
    title: Optional[str]
    content: Optional[str]
    type: Optional[TestType]
    tag: Optional[Tag]
    review: Optional[int] = Field(ge=0, le=5)
    last_updated_by: Optional[User]
    last_updated_at: Optional[datetime]


class TestModelSearchParams(Encoder):
    offset: int = Field(default=0, ge=0)
    limit: int = Field(
        default=LocalConfig.DEFAULT_ITEMS_PER_PAGE,
        le=LocalConfig.MAX_ITEMS_PER_PAGE,
        ge=0,
    )
    sort_by: Literal["created_at", "last_updated_at"] = "last_updated_at"
    order: Literal["asc", "desc"] = "desc"
    creator_id: Optional[PyObjectId]
    type: Optional[TestType]
    tag: Optional[Tag] = Field(description="single string reprensting the tag")
    review: Optional[int] = Field(ge=0, le=5)
    title: Optional[str]

    def get_criteria(self, current_user: UserModel):
        filter_criteria: dict[str, Any] = {}
        if current_user.role not in [Role.SUPERADMIN, Role.ADMIN]:
            self.creator_id = current_user.id
        if self.creator_id:
            filter_criteria["creator_id"] = self.creator_id
        if self.type:
            filter_criteria["type"] = self.type
        if self.tag:
            filter_criteria["tag"] = self.tag
        if self.review:
            filter_criteria["review"] = self.review
        if self.title:
            filter_criteria["title"] = {"$regex": f"^.*{self.title}.*", "$options": "i"}
        return filter_criteria
