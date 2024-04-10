from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User
import sqlalchemy as sa
from exceptions import UserNotFound, UserAlreadyExists, UsernameOrPasswordIncorrect
from utils.secret import password_manager
from schema.output import RegisterOutput
from sqlalchemy.exc import IntegrityError
from utils.jwt import JWTHandler
from schema.jwt import JWTResponsePayload


class UsersOperation:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def create(self, username:str, password:str) -> RegisterOutput:
        user_pwd = password_manager.hash(password)
        user = User(password=user_pwd, username=username)

        async with self.db_session as session:
            try:
                session.add(user)
                await session.commit()
            except IntegrityError:
                raise UserAlreadyExists

        return RegisterOutput(username=user.username, id=user.id)
    
    async def get_user_by_username(self, username:str) -> User:
        query = sa.select(User).where(User.username == username)

        async with self.db_session as session:
            user_data = await session.scalar(query)

            if user_data is None:
                raise UserNotFound
            
            return user_data
        
    async def update_username(self, old_username: str, new_username: str) -> User:
        query = sa.select(User).where(User.username == old_username)
        update_query = sa.update(User).where(User.username == old_username).values(username = new_username)

        async with self.db_session as session:
            user_data = await session.scalar(query)

            if user_data is None:
                raise UserNotFound
            
            await session.execute(update_query)
            await session.commit()
            
            user_data.username = new_username
            return user_data

    async def user_delete_account(self, username:str) -> None:
        delete_query = sa.delete(User).where(User.username == username) #type: ignore

        async with self.db_session as session:
            await session.execute(delete_query)
            await session.commit()

    async def login(self, username:str, password:str) -> JWTResponsePayload:
        query = sa.select(User).where(User.username==username)

        async with self.db_session as session:
            user = await session.scalar(query)

            if user is None:
                raise UsernameOrPasswordIncorrect
        
        if not password_manager.verify(password, user.password):
            raise UsernameOrPasswordIncorrect
        
        return JWTHandler.generate(username)
    