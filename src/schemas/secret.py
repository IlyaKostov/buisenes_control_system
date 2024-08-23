from pydantic import BaseModel, UUID4


class SecretID(BaseModel):
    id: UUID4


class CreateSecretRequest(BaseModel):
    password: str
    account_id: int


class Secret(BaseModel):
    password: bytes


class UpdateSecretRequest(CreateSecretRequest):
    pass


class SecretDB(SecretID, CreateSecretRequest):
    pass
