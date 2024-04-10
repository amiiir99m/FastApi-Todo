from fastapi import APIRouter, Body, Depends
from schema.input import UserInput, UpdateUserProfileInput
from db.engine import get_db
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from operations.users import UsersOperation
from schema.jwt import JWTPayload
from utils.jwt import JWTHandler


router = APIRouter()


@router.post("/register")
async def register(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    data: UserInput = Body()
):
    user = await UsersOperation(db_session).create(username=data.username, password=data.password)
    return user


@router.post("/login")
async def login(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    data: UserInput = Body()

):
    token = await UsersOperation(db_session).login(data.username, data.password)

    return token


@router.get("/{username}")
async def get_user_profile(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    username: str
):
    user_profile = await UsersOperation(db_session).get_user_by_username(username)
    return user_profile


@router.put("/")
async def update_user_profile(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    data: UpdateUserProfileInput = Body(),
    token_data : JWTPayload = Depends(JWTHandler.verify_token),
):
    user = await UsersOperation(db_session).update_username(token_data.username, data.new_username)

    return user


@router.delete("/")
async def delete_user_account(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    token_data : JWTPayload = Depends(JWTHandler.verify_token),


):
    await UsersOperation(db_session).user_delete_account(token_data.username)

 

