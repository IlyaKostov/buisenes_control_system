from fastapi import APIRouter, Depends

from src.api.account.service import AccountService
from src.api.company.service import CompanyService
from src.schemas.account import CheckAccountResponse, ConfirmAccount, CreateAccountResponse, SignUpCompleteRequest
from src.schemas.company import CompanyDB, CreateCompanyResponse

router = APIRouter()


@router.post('/sign-up')
async def sign_up(
    confirm_account: ConfirmAccount,
    account_service: AccountService = Depends(AccountService),
):
    response_message: CreateAccountResponse = await account_service.check_account_invite(confirm_account)

    return CheckAccountResponse(payload=response_message)


@router.post('/sign-up-complete')
async def sign_up_complete(
        complete_data: SignUpCompleteRequest,
        company_service: CompanyService = Depends(CompanyService),
) -> CreateCompanyResponse:

    company: CompanyDB = await company_service.create_company(complete_data)

    return CreateCompanyResponse(payload=company)
