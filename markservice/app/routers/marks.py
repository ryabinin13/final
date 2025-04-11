from uuid import UUID
from fastapi import APIRouter, Depends
from app.dependencies import get_current_user_id, get_mark_service
from app.schemas.mark import CreateMarkSchema
from app.services.mark import MarkService


mark_router = APIRouter()


@mark_router.post("/marks")
async def create_mark(
    create_mark_schema: CreateMarkSchema,
    mark_service: MarkService = Depends(get_mark_service),
    current_user_id: UUID = Depends(get_current_user_id)
):
    return await mark_service.create_mark(create_mark_schema)


@mark_router.get("/marks/me")
async def get_marks(
    mark_service: MarkService = Depends(get_mark_service),
    current_user_id: UUID = Depends(get_current_user_id)
):
    return await mark_service.get_marks(current_user_id)