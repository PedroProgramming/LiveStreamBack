from typing import Optional
from pydantic import BaseModel, EmailStr, model_validator

from utils.validations import validated_fields_schemas

# Schemas 
class UserCreateSchema(BaseModel):
    username: Optional[str]
    email: EmailStr
    password: str
    confirm_password: str

    @model_validator(mode='before')
    def check_fields_not_empty(cls, values):
        return validated_fields_schemas(
            'email', 'password', 'confirm_password', values=values
        )


class LoginSchema(BaseModel):
    email: str
    password: str

    @model_validator(mode='before')
    def check_fields_not_empty(cls, values):
        return validated_fields_schemas('email', 'password', values=values)
