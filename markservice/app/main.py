from fastapi import FastAPI
from app.routers.marks import mark_router
from app.lifespan import lifespan


app = FastAPI(lifespan=lifespan)
app.include_router(mark_router)