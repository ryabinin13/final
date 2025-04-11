from fastapi import HTTPException, Request
import jwt
from app.repositories.organization import OrganizationRepository
from app.repositories.organization_membersips import OrganizationMembershipsRepository
from app.database import get_async_session
from app.services.broker_consumer import BrokerConsumerService
from app.services.organization import OrganizationService
from config import config


def get_organization_memberships_repository() ->OrganizationMembershipsRepository:
    return OrganizationMembershipsRepository(session=get_async_session())

def get_organization_repository() ->OrganizationRepository:

    return OrganizationRepository(session=get_async_session())

def get_organization_service() -> OrganizationService:
    from app.main import app
    app_state=app.state

    return OrganizationService(org_repository=get_organization_repository(), org_memberships_repository=get_organization_memberships_repository(), app_state=app.state)

def get_broker_consumer_service() -> BrokerConsumerService:
    return BrokerConsumerService(organization_membership_repository=get_organization_memberships_repository(), organization_repository=get_organization_repository())


def get_current_user_id(request: Request):
    token = request.cookies.get(config.JWT_ACCESS_COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=401, detail="Token not found")

    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM]) 
        user_id = payload.get("uid")
        if user_id is None:
            raise ValueError("Invalid token payload: 'uid' claim not found")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {e}")