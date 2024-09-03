from fastapi import APIRouter, Depends

from src.api.dependencies import AdminAccount
from src.api.struct_adm.service import StructAdmService
from src.models import StructAdmModel
from src.schemas.struc_adm import CreateStructAdm, StructAdmCreateResponse, UpdateStructAdm, StructAdmDeleteResponse

router = APIRouter()


@router.post("/create-department")
async def create_department(
    department_data: CreateStructAdm,
    admin_account: AdminAccount,
    department_service: StructAdmService = Depends()
):
    department: StructAdmModel = await department_service.create_department(department_data, admin_account)
    return StructAdmCreateResponse(payload=department.to_pydantic_schema())


@router.put("/update-department/{department_id}")
async def update_department(
    department_id: int,
    department_data: UpdateStructAdm,
    admin_account: AdminAccount,
    department_service: StructAdmService = Depends()
):
    updated_department: StructAdmModel = await department_service.update_department(department_id, department_data, admin_account)
    return StructAdmCreateResponse(payload=updated_department.to_pydantic_schema())


@router.delete("/delete-department/{department_id}")
async def delete_department(
    department_id: int,
    admin_account: AdminAccount,
    department_service: StructAdmService = Depends()
):
    await department_service.delete_department(department_id, admin_account)
    return StructAdmDeleteResponse(message="Department deleted successfully.")
