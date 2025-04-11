from fastapi import FastAPI
from app.routers.meeting import meeting_router
from app.lifespan import lifespan


app = FastAPI(lifespan=lifespan)
app.include_router(meeting_router)
