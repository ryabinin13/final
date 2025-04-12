from fastapi import FastAPI
from app.database import Base, async_engine
from app.routers.users import user_router
from app.lifespan import lifespan
import uvicorn

app = FastAPI(lifespan=lifespan)
app.include_router(user_router)



