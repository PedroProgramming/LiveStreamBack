from ninja import Schema
from typing import Optional
from pydantic import BaseModel, model_validator
from utils.validations import validated_fields_schemas

class CreateChannelSchema(BaseModel):
    channel_name: str
    description: Optional[str] = None

    @model_validator(mode="before")
    def check_fields_not_empty(cls, values):
        return validated_fields_schemas("channel_name", values=values)
    
class DetailsChannelSchema(Schema):
    channel_name: str
    description: str
    subscribers_count: int