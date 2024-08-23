from pydantic import BaseModel, EmailStr

from src.schemas.auth import AuthRequestSchema
from src.schemas.company import CreateCompanyRequest
from src.schemas.invite import CheckInvite
from src.schemas.response import BaseResponse
from src.schemas.user import CreateUserRequest


class AccountID(BaseModel):
    id: int


class CreateAccount(BaseModel):
    email: EmailStr


class UpdateAccountRequest(CreateAccount):
    pass


class AccountDB(AccountID, CreateAccount):
    is_active: bool
    is_admin: bool


class CreateAccountResponse(BaseModel):
    message: str


class CheckAccountResponse(BaseResponse):
    payload: CreateAccountResponse


class ConfirmAccount(CreateAccount, CheckInvite):
    pass


class SignUpCompleteRequest(AuthRequestSchema, CreateCompanyRequest, CreateUserRequest):
    pass
