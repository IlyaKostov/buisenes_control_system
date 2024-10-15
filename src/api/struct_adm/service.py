import uuid

from sqlalchemy_utils import Ltree
from starlette import status
from starlette.exceptions import HTTPException

from src.models import AccountModel, StructAdmModel
from src.schemas.struc_adm import CreateStructAdm, UpdateStructAdm
from src.utils.base_service import BaseService
from src.utils.unit_of_work import transaction_mode


class StructAdmService(BaseService):
    base_repository = 'struct_adm'

    @transaction_mode
    async def create_department(self, data: CreateStructAdm, admin: AccountModel) -> StructAdmModel:

        await self.check_department(data, admin)

        if data.manager_id:
            await self.check_manager(data.manager_id, admin)

        department_id = await self.uow.struct_adm.get_id()
        company_id = admin.user.company_id
        path = await self.generate_ltree_path(data, company_id, department_id)

        new_department: dict[str, str] = {
            'id': department_id,
            'name': data.name,
            'parent_id': data.parent_id,
            'company_id': company_id,
            'manager_id': data.manager_id,
            'path': path,
        }

        department: StructAdmModel = await self.uow.struct_adm.add_one_and_get_obj(**new_department)

        return department

    @transaction_mode
    async def update_department(
        self,
        department_id: int,
        data: UpdateStructAdm,
        admin: AccountModel,
    ) -> StructAdmModel:

        department = await self.uow.struct_adm.get_by_query_one_or_none(id=department_id)

        if department is None or department.company_id != admin.user.company_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Department not found.')

        await self.check_department(data, admin)

        if data.manager_id:
            await self.check_manager(data.manager_id, admin)

        company_id = admin.user.company_id
        path = await self.generate_ltree_path(data, company_id, department_id)

        await self.uow.struct_adm.update_child_paths(department.path, path, department_id)

        department.path = path

        update_department: dict[str, str] = {
            'name': data.name,
            'parent_id': data.parent_id,
            'manager_id': data.manager_id,
        }
        await self.uow.struct_adm.update_one_by_id(department_id, update_department)

        return department

    @transaction_mode
    async def delete_department(self, department_id: uuid.UUID, admin: AccountModel) -> None:
        department = await self.uow.struct_adm.get_by_query_one_or_none(id=department_id)

        if not department:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Department not found')

        if department.company_id != admin.user.company_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail='Insufficient rights to delete this department')

        await self.uow.struct_adm.delete_by_query(id=department_id)

    async def generate_ltree_path(self, data: CreateStructAdm, company_id: uuid.UUID, department_id: int) -> Ltree:
        """Метод для генерации пути ltree для нового подразделения."""

        if data.parent_id:
            parent_department = await self.uow.struct_adm.get_by_query_one_or_none(id=data.parent_id)
            if not parent_department or parent_department.company_id != company_id:
                raise HTTPException(
                    status_code=(status.HTTP_404_NOT_FOUND if not parent_department
                                 else status.HTTP_403_FORBIDDEN),
                    detail=('Parent Department Not found' if not parent_department
                            else 'Insufficient rights to create a department under the specified parent.'),
                )
            return Ltree(f'{parent_department.path}.{department_id}_{data.name}')
        return Ltree(f'{department_id}_{data.name}')

    async def check_manager(self, manager_id: uuid.UUID, admin: AccountModel) -> None:
        manager = await self.uow.user.get_by_query_one_or_none(id=manager_id)
        if manager is None or manager.company_id != admin.user.company_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    async def check_department(self, data: CreateStructAdm, admin: AccountModel) -> None:
        existing_department = await self.uow.struct_adm.get_by_name_and_parent(data.name, data.parent_id)
        if existing_department and existing_department.company_id == admin.user.company_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Department with this name already exists under the specified parent.')
