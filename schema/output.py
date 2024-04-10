from uuid import UUID

from pydantic import BaseModel


class RegisterOutput(BaseModel):
    username: str
    id: UUID


class TaskOutput(BaseModel):
    title: str
    user: str
    id: UUID