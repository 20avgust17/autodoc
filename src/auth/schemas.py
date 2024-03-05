from pydantic import BaseModel
from pydantic.v1 import validator


class CreateUser(BaseModel):
    name: str
    description: str
    hashed_password: str

    @validator('password', always=True)
    def validate_password(cls, value):
        if len(value) < 6:
            raise ValueError('Password length can not be less then 6 characters')
        return value


class CurrentUser(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
