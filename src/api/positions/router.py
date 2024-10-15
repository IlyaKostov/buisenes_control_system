import uuid

from fastapi import APIRouter, Depends

from src.api.dependencies import AdminAccount
from src.api.positions.service import PositionService
from src.models import PositionModel
from src.schemas.position import CreatePosition, PositionCreateResponse, PositionResponse, UpdatePosition

router = APIRouter()


@router.post('/create-position')
async def create_position(
    position_data: CreatePosition,
    admin_account: AdminAccount,
    position_service: PositionService = Depends(),
) -> PositionCreateResponse:
    position: PositionModel = await position_service.create_position(position_data)
    return PositionCreateResponse(payload=position.to_pydantic_schema())


@router.put('/position/{position_id}')
async def update_position(
    position_id: uuid.UUID,
    position_data: UpdatePosition,
    admin_account: AdminAccount,
    position_service: PositionService = Depends(),
) -> PositionCreateResponse:
    updated_position = await position_service.update_position(position_id, position_data, admin_account)
    return PositionCreateResponse(payload=updated_position.to_pydantic_schema())


@router.delete('/position/{position_id}')
async def delete_position(
    position_id: uuid.UUID,
    admin_account: AdminAccount,
    position_service: PositionService = Depends(),
) -> PositionResponse:
    await position_service.delete_position(position_id)
    return PositionResponse(message='Position deleted successfully.')


@router.post('/positions/{position_id}/assign/user/{user_id}')
async def assign_position_to_user(
    position_id: uuid.UUID,
    user_id: uuid.UUID,
    admin_account: AdminAccount,
    position_service: PositionService = Depends(),
) -> PositionResponse:
    await position_service.assign_position_to_user(user_id, position_id)
    return PositionResponse(message='Position assigned to user successfully')


@router.post('/positions/{position_id}/assign/department/{department_id}')
async def assign_position_to_department(
        position_id: uuid.UUID,
        department_id: int,
        admin_account: AdminAccount,
        position_service: PositionService = Depends(),
) -> PositionResponse:
    await position_service.assign_position_to_struct(department_id, position_id)
    return PositionResponse(message='Position assigned to department successfully')
