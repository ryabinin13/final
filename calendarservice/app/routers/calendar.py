import uuid
from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_calendar_service
from app.schemas.calendar import CreateEventSchema
from app.services.calendar import CalendarService


calendar_router = APIRouter()


@calendar_router.post("/calendars/")
async def create_event(
    create_event_schema: CreateEventSchema,
    calendar_service: CalendarService = Depends(get_calendar_service)
):
    return await calendar_service.create_event(create_event_schema)
