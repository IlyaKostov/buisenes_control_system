from pydantic import BaseModel, UUID4, Field


class UserID(BaseModel):
    id: UUID4


class CreateUserRequest(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    middle_name: str | None = Field(max_length=50, default=None)
    company_id: UUID4


class UpdateUserRequest(CreateUserRequest):
    pass


class UserDB(UserID, CreateUserRequest):
    pass
