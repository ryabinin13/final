import uuid
from fastapi import APIRouter, Depends
from app.dependencies import get_organization_service
from app.schemas.organization import AddOrganizationSchema
from app.services.organization import OrganizationService
from app.dependencies import get_current_user_id


org_router = APIRouter()


@org_router.post("/organizations/")
async def create_organization(
    add_ord_schema: AddOrganizationSchema,
    org_service: OrganizationService = Depends(get_organization_service),
    current_user_id: uuid.UUID = Depends(get_current_user_id)
    ):
    return await org_service.create_org(add_ord_schema)


@org_router.post("/organizations/{org_id}/users/{user_id}")
async def add_user(
    org_id: int,
    user_id: uuid.UUID,
    org_service: OrganizationService = Depends(get_organization_service),
    current_user_id: uuid.UUID = Depends(get_current_user_id)
    ):
    return await org_service.add_user(org_id, user_id)


@org_router.delete("/organizations/{org_id}/users/{user_id}")
async def delete_user(
    org_id: int,
    user_id: uuid.UUID,
    org_service: OrganizationService = Depends(get_organization_service),
    current_user_id: uuid.UUID = Depends(get_current_user_id)
):
    return await org_service.delete_user(org_id, user_id)