from pydantic import BaseModel


class CheckInvite(BaseModel):
    token: str
