from fastapi import FastAPI
from app.routers.organization import org_router
from app.lifespan import lifespan


app = FastAPI(lifespan=lifespan)
app.include_router(org_router)