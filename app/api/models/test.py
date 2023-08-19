from pydantic import Field
from app.api.common.common import PyObjectId, Encoder, User
from enum import Enum
from datetime import datetime
from typing import Optional, Literal, Any
from app.api.config.config import LocalConfig


class TestType(Enum):
    pass


class Tags(Enum):
    pass


class CreateTestModel(Encoder):
    creator_id: Optional[PyObjectId]
    title: str
    content: str
    type: Optional[TestType]
    tags: Optional[Tags]
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
    tags: Optional[Tags]
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
    tags: Optional[Tags] = Field(description="single string reprensting the tag")
    review: Optional[int] = Field(ge=0, le=5)

    def get_criteria(self):
        filter_criteria: dict[str, Any] = {}
        if self.creator_id:
            filter_criteria["creator_id"] = self.creator_id
        if self.type:
            filter_criteria["type"] = self.type
        if self.tags:
            filter_criteria["tags"] = self.tags
        if self.review:
            filter_criteria["review"] = self.review
        return filter_criteria
