from ninja import Schema
from typing import Optional
from pydantic import BaseModel, model_validator
from utils.validations import validated_fields_schemas


class LiveStreamSchema(Schema):
    id: int
    stream_key: str
    title: str
    description: str
    # thumbnail_url: str

class LiveResponseSchema(Schema):
    lives: list[LiveStreamSchema]