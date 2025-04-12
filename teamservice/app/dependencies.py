from fastapi import HTTPException, Request
import jwt
from app.repositories.team import TeamRepository
from app.database import get_async_session
from app.repositories.team_memebership import TeamMembershipRepository
from app.services.broker_consumer import BrokerConsumerService
from app.services.team import TeamService
from config import config


async def get_team_membership_repository() ->TeamMembershipRepository:
    async with get_async_session() as session:
        return TeamMembershipRepository(session=session)

async def get_team_repository() ->TeamRepository:
    async with get_async_session() as session:
        return TeamRepository(session=session)

async def get_team_service() -> TeamService:
    from app.main import app

    team_repository = await get_team_repository()
    team_membership_repository = await get_team_membership_repository()

    return TeamService(team_repository=team_repository, team_memberships_repository=team_membership_repository, app_state=app.state)

async def get_broker_consumer_service() -> BrokerConsumerService:
    from app.main import app

    team_repository = await get_team_repository()
    team_membership_repository = await get_team_membership_repository()

    return BrokerConsumerService(team_membership_repository=team_membership_repository, team_repository=team_repository, app_state=app.state)


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
