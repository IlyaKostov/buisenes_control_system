from sqlalchemy import Result, select, text
from sqlalchemy.orm import selectinload
from sqlalchemy_utils import Ltree

from src.models import StructAdmModel
from src.utils.custom_types import id_seq
from src.utils.repository import SQLAlchemyRepository


class StructAdmRepository(SQLAlchemyRepository):
    model = StructAdmModel

    async def get_by_name_and_parent(self, name, parent_id):
        stmt = (
            select(self.model)
            .filter_by(name=name, parent_id=parent_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_id(self):
        result = await self.session.execute(id_seq)
        return result

    async def get_children_by_id(self, parent_id: int):
        stmt = select(self.model).filter_by(parent_id=parent_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_child_paths(self, old_path: Ltree, new_path: Ltree, department_id: int):
        query = text(
            """
            UPDATE struct_adm
            SET path = :new_path || subpath(path, nlevel(:old_path))
            WHERE path <@ :old_path AND id != :department_id;
            """,
        )

        params = {
                'new_path': str(new_path),
                'old_path': str(old_path),
                'department_id': department_id,
            }

        await self.session.execute(query, params)

    async def get_department_with_positions(self, struct_adm_id: int):
        stmt = (
            select(self.model)
            .options(selectinload(self.model.positions))
            .filter_by(id=struct_adm_id)
        )
        result: Result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
