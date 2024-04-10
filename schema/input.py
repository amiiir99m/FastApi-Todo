from pydantic import BaseModel


class UserInput(BaseModel):
    username: str
    password: str


class UpdateUserProfileInput(BaseModel):
    new_username: str


class TaskInput(BaseModel):
    title: str

class TaskUpdateInput(BaseModel):
    old_title: str
    new_title: str