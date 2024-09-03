from pydantic import UUID4, BaseModel


class SecretID(BaseModel):
    id: UUID4


class CreateSecretRequest(BaseModel):
    password: str
    account_id: int


class Secret(BaseModel):
    password: str


class UpdateSecretRequest(CreateSecretRequest):
    pass


class SecretDB(SecretID, CreateSecretRequest):
    pass
