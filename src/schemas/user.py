from pydantic import BaseModel, UUID4, Field

from src.schemas.response import BaseCreateResponse, BaseResponse


class UserID(BaseModel):
    id: UUID4


class CreateUserRequest(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    middle_name: str | None = Field(max_length=50, default=None)


class UserRelationship(BaseModel):
    company_id: UUID4
    account_id: int


class UpdateUserRequest(CreateUserRequest):
    pass


class UserDB(UserID, CreateUserRequest, UserRelationship):
    pass


class CreateUserResponse(BaseCreateResponse):
    payload: UserDB


class UpdateUserResponse(BaseResponse):
    payload: UserDB
