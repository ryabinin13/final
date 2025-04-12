from fastapi import FastAPI
from app.routers.calendar import calendar_router
from app.lifespan import lifespan


app = FastAPI(lifespan=lifespan)
app.include_router(calendar_router)
