from pydantic import BaseModel, EmailStr

from src.schemas.response import BaseResponse


class AuthRequestSchema(BaseModel):
    email: EmailStr
    password: str


class TokenInfoSchema(BaseModel):
    access_token: str
    token_type: str


class AuthResponseSchema(BaseResponse):
    payload: TokenInfoSchema
