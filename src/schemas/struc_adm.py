import uuid

from pydantic import BaseModel, field_serializer
from sqlalchemy_utils import Ltree

from src.schemas.response import BaseCreateResponse, BaseResponse


class StructAdmID(BaseModel):
    id: int


class CreateStructAdm(BaseModel):
    name: str
    parent_id: int | None = None
    manager_id: uuid.UUID | None = None


class UpdateStructAdm(CreateStructAdm):
    pass


class StructAdmDB(StructAdmID, CreateStructAdm):
    path: Ltree
    company_id: uuid.UUID

    @field_serializer('path')
    def serialize_path(self, path: Ltree, _info):
        return path.path

    class Config:
        arbitrary_types_allowed = True


class StructAdmCreateResponse(BaseCreateResponse):
    payload: StructAdmDB


class StructAdmDeleteResponse(BaseResponse):
    message: str
