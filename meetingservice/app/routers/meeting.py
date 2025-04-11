import uuid
from fastapi import APIRouter, Depends
from app.dependencies import get_current_user_id, get_meeting_service
from app.schemas.meeting import CreateMeetingSchema, UpdateMeetingSchema, AddUserSchema
from app.services.meeting import MeetingService



meeting_router = APIRouter()


@meeting_router.post("/meetings")
async def create_meeting(
    create_meeting_schema: CreateMeetingSchema,
    meeting_service: MeetingService = Depends(get_meeting_service),
    current_user_id: int = Depends(get_current_user_id)
):
    return await meeting_service.create_meeting(create_meeting_schema)


@meeting_router.delete("/meetings/{id}")
async def delete(
    id: int,
    meeting_service: MeetingService = Depends(get_meeting_service),
    current_user_id: int = Depends(get_current_user_id),

    ):
    return await meeting_service.meeting_delete(id)


@meeting_router.put("/meetings/{id}")
async def update(
    id: int,
    update_meeting_schema: UpdateMeetingSchema,
    meeting_service: MeetingService = Depends(get_meeting_service),
    current_user_id: int = Depends(get_current_user_id),

    ):
    return await meeting_service.meeting_update(id, update_meeting_schema)


@meeting_router.post("/meetings/{meeting_id}/users")
async def add_user(
    meeting_id: int,
    add_user_schema: AddUserSchema,
    meeting_service: MeetingService = Depends(get_meeting_service),
    ):
    return await meeting_service.add_user(meeting_id, add_user_schema)