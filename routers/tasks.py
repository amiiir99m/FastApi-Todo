from fastapi import APIRouter, Body, Depends
from schema.input import UserInput, UpdateUserProfileInput, TaskInput, TaskUpdateInput
from db.engine import get_db
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from operations.users import UsersOperation
from operations.tasks import TaskOperation

from schema.jwt import JWTPayload
from utils.jwt import JWTHandler


router = APIRouter()


@router.post("/create-task")
async def create_task(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    data: TaskInput = Body(),
    token_data : JWTPayload = Depends(JWTHandler.verify_token),
):
    user = await TaskOperation(db_session).create(title = data.title, user=token_data.username)
    return user


@router.get('/all_tasks')
async def get_tasks(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    token_data : JWTPayload = Depends(JWTHandler.verify_token),
):
    tasks = await TaskOperation(db_session).get_task_by_username(token_data.username)
    return tasks


@router.put('/update_task')
async def update_task(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    data: TaskUpdateInput = Body(),
    token_data: JWTPayload = Depends(JWTHandler.verify_token),
):
    task = await TaskOperation(db_session).task_update_by_title(token_data.username, data.old_title, data.new_title)

    return task

@router.delete('/delete_task')
async def delete_task(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    data: TaskInput = Body(),
    token_data: JWTPayload = Depends(JWTHandler.verify_token),
):
    await TaskOperation(db_session).task_delete_by_title(token_data.username, data.title)

@router.get('/{title}')
async def get_task_by_title(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    title: str,
    token_data: JWTPayload = Depends(JWTHandler.verify_token),
):
    task = await TaskOperation(db_session).get_task_by_title(token_data.username, title)

    return task
    