from ninja import Schema
from typing import Optional
from pydantic import BaseModel, model_validator
from utils.validations import validated_fields_schemas

class CreateVideoSchema(BaseModel):
    title: str
    description: Optional[str] = None

    @model_validator(mode="before")
    def check_fields_not_empty(cls, values):
        return validated_fields_schemas("title", values=values)
    
class VideoSchema(Schema):
    id: int
    identifier: str
    title: str
    description: str
    thumbnail_url: str
    views: int
    likes: int
    dislikes: int
    video_url: str

class VideoResponseSchema(Schema):
    videos: list[VideoSchema]