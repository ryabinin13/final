from fastapi import HTTPException, Request
import jwt
from app.repositories.organization import OrganizationRepository
from app.repositories.organization_membersips import OrganizationMembershipsRepository
from app.database import get_async_session
from app.services.broker_consumer import BrokerConsumerService
from app.services.organization import OrganizationService
from config import config


async def get_organization_memberships_repository() ->OrganizationMembershipsRepository:
    async with get_async_session() as session:
        return OrganizationMembershipsRepository(session=session)

async def get_organization_repository() ->OrganizationRepository:
    async with get_async_session() as session:
        return OrganizationRepository(session=session)

async def get_organization_service() -> OrganizationService:
    from app.main import app

    org_repository = await get_organization_repository()
    org_memberships_repository = await get_organization_memberships_repository()

    return OrganizationService(org_repository=org_repository, org_memberships_repository=org_memberships_repository, app_state=app.state)

async def get_broker_consumer_service() -> BrokerConsumerService:

    org_repository = await get_organization_repository()
    org_memberships_repository = await get_organization_memberships_repository()

    return BrokerConsumerService(organization_membership_repository=org_repository, organization_repository=org_memberships_repository)


def get_current_user_id(request: Request):
    token = request.cookies.get(config.JWT_ACCESS_COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=401, detail="Token not found")

    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM]) 
        user_id = payload.get("uid")
        if user_id is None:
            raise ValueError("Invalid token payload: 'uid' claim not found")
        if not isinstance(user_id, str):
            raise ValueError("Invalid token payload: 'uid' claim must be a string")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
