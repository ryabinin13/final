from fastapi import FastAPI
from app.routers.teams import team_router
from app.lifespan import lifespan


app = FastAPI(lifespan=lifespan)
app.include_router(team_router)
