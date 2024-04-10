from fastapi import FastAPI
import uvicorn
from db.engine import Base, engine
from routers.users import router as user_router
from routers.tasks import router as task_router

app = FastAPI()


@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(user_router, prefix="/users")
app.include_router(task_router, prefix="/tasks")



if __name__ == "__main__":
    uvicorn.run(app)