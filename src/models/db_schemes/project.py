from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson.objectid import ObjectId


class Project(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    project_id: str = Field(..., min_length=1)

    @field_validator('project_id')
    @classmethod
    def validate_project_id(cls, value: str) -> str:
        if not value.isalnum():
            raise ValueError('Project ID must be alphanumeric')
        return value

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True