from ninja import Schema
from typing import Optional
from pydantic import BaseModel, EmailStr, model_validator

from utils.validations import validated_fields_schemas

# Schemas
class DetailsUserSchema(Schema):
    username: str
    email: str
    gender: Optional[str] = None
    phone: Optional[str] = None
    profile_picture_url: Optional[str] = None

class UpdateUserSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    gender: Optional[str] = None
    phone: Optional[str] = None

    @model_validator(mode='before')
    def check_fields_not_empty(cls, values):
        return validated_fields_schemas(
            'username', 'email', 'gender', 'phone', values=values
        )
