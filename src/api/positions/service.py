import uuid

from starlette import status
from starlette.exceptions import HTTPException

from src.models import AccountModel, PositionModel, UserModel, StructAdmModel
from src.schemas.position import CreatePosition, UpdatePosition
from src.utils.base_service import BaseService
from src.utils.unit_of_work import transaction_mode


class PositionService(BaseService):
    base_repository = 'position'

    @transaction_mode
    async def create_position(self, data: CreatePosition) -> PositionModel:
        result = await self.uow.position.add_one_and_get_obj(name=data.name)
        return result

    @transaction_mode
    async def update_position(self, position_id: str, data: UpdatePosition, admin: AccountModel) -> PositionModel:
        try:
            uuid_obj = uuid.UUID(position_id)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid UUID format")

        position = await self.uow.position.get_by_query_one_or_none(id=position_id)
        if position is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Position not found")

        updated_position = await self.uow.position.update_one_by_id(position_id, {'name': data.name})
        return updated_position

    @transaction_mode
    async def delete_position(self, position_id: uuid.UUID):
        position = self.uow.position.get_by_query_one_or_none(id=position_id)

        if position is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Position not found")

        await self.uow.position.delete_by_query(id=position_id)

    @transaction_mode
    async def assign_position_to_user(self, user_id: uuid.UUID, position_id: uuid.UUID) -> None:
        user: UserModel = await self.uow.user.get_by_query_one_or_none(id=user_id)
        position: PositionModel = await self.uow.position.get_position_with_users(position_id)

        if user is None or position is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User or Position not found")

        position.users.append(user)

    @transaction_mode
    async def assign_position_to_struct(self, department_id: int, position_id: uuid.UUID) -> None:
        existing_entry = await self.uow.struct_adm_position.get_by_struct_and_position(department_id, position_id)
        if existing_entry:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Position already assigned to this department")

        department: StructAdmModel = await self.uow.struct_adm.get_department_with_positions(department_id)
        position = await self.uow.position.get_by_query_one_or_none(id=position_id)

        if department is None or position is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department or Position not found")

        department.positions.append(position)
