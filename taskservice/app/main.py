from fastapi import FastAPI
from app.routers.task import task_router
from app.lifespan import lifespan


app = FastAPI(lifespan=lifespan)
app.include_router(task_router)