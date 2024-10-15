import uuid

from pydantic import BaseModel

from src.schemas.response import BaseCreateResponse, BaseResponse


class PositionID(BaseModel):
    id: uuid.UUID


class CreatePosition(BaseModel):
    name: str


class UpdatePosition(CreatePosition):
    pass


class PositionDB(PositionID, CreatePosition):
    pass


class PositionCreateResponse(BaseCreateResponse):
    payload: PositionDB


class PositionResponse(BaseResponse):
    message: str
