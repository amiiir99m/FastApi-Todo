from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Task
import sqlalchemy as sa
from schema.output import TaskOutput
from exceptions import TaskNotFound

class TaskOperation:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session
    
    async def create(self, title:str, user:str) -> TaskOutput:
        task = Task(title = title, user = user)

        async with self.db_session as session:
            try:
                session.add(task)
                await session.commit()
            except:
                raise 
        
        return TaskOutput(title=task.title, user = task.user, id = task.id)
    
    async def get_task_by_username(self, username:str) -> list[Task]:
        query = sa.select(Task).where(Task.user == username)

        async with self.db_session as session:
            task_data = await session.execute(query)
            datas = [task for task, in task_data]

            if task_data is None:
                raise TaskNotFound

            return datas

    async def task_update_by_title(self, username:str, old_title:str, new_title:str) -> Task:
        query = sa.select(Task).where(Task.user == username, Task.title ==old_title)
        update_query = sa.update(Task).where(Task.title == old_title).values(title = new_title)

        async with self.db_session as session:
            task_data = await session.scalar(query)

            if task_data is None:
                raise TaskNotFound
            
            await session.execute(update_query)
            await session.commit()

            task_data.title = new_title
            return task_data

    async def task_delete_by_title(self, username:str, title:str) -> None:
        query = sa.select(Task).where(Task.user == username, Task.title == title)
        delete_query = sa.delete(Task).where(Task.user == username, Task.title == title)

        async with self.db_session as session:
            task_data = await session.scalar(query)

            if task_data is None:
                raise TaskNotFound
                                             
            await session.execute(delete_query)
            await session.commit()

    async def get_task_by_title(self, username:str, title:str) -> Task:
        query = sa.select(Task).where(Task.user == username, Task.title == title)

        async with self.db_session as session:
            task_data = await session.scalar(query)

            if task_data is None:
                raise TaskNotFound
            
            return task_data