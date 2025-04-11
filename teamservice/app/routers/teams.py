import uuid
from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_team_service, get_current_user_id
from app.schemas.team import TeamCreateSchema
from app.schemas.user import UserChangeStatusSchema
from app.services.team import TeamService
from uuid import UUID

from exceptions import UserAlreadyHasTeamException

team_router = APIRouter()


@team_router.post("/teams")
async def team_create(
    team_create_schema: TeamCreateSchema,
    team_service: TeamService = Depends(get_team_service),
    current_user_id: UUID = Depends(get_current_user_id),
    ):
    try:
        return await team_service.team_create(team_create_schema, current_user_id)
    except UserAlreadyHasTeamException:
        raise HTTPException(status_code=409, detail="Пользователь уже находится в команде")


@team_router.post("/teams/{team_id}/users")
async def add_user(
    email: str,
    team_id: UUID,
    team_service: TeamService = Depends(get_team_service),
    current_user_id: UUID = Depends(get_current_user_id),
    ):
    return await team_service.add_user(team_id, email, current_user_id)


@team_router.patch("/teams/{team_id}/users/{user_id}")
async def assign_status(
    team_id: uuid.UUID,
    user_id: uuid.UUID,
    user_change_status_schema: UserChangeStatusSchema,
    team_service: TeamService = Depends(get_team_service),
    current_user_id: UUID = Depends(get_current_user_id)
    ):
    return await team_service.change_status(team_id, user_id, user_change_status_schema)

@team_router.delete("/teams/{team_id}/users/{user_id}")
async def delete_user(
    team_id: uuid.UUID,
    user_id: uuid.UUID,
    team_service: TeamService = Depends(get_team_service),
    current_user_id: UUID = Depends(get_current_user_id)
):
    return await team_service.delete_user(team_id, user_id)
