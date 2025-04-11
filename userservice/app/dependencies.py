from fastapi import HTTPException, Request, Depends
import jwt

from app.repositories.user import UserRepository
from app.services.broker_consumer import BrokerConsumerService
from app.services.login import LoginService
from app.services.registration import RegistrationService
from app.database import get_async_session
from config import config

async def get_app_dependencies():
    from app.main import app
    user_repository = await get_user_repository()
    return app, user_repository


async def get_user_repository() -> UserRepository:
    async with get_async_session() as session:
        return UserRepository(session=session)

async def get_registration_service() -> RegistrationService:

    app, user_repository = await get_app_dependencies()

    return RegistrationService(repository=user_repository, app_state=app.state)

async def get_login_service() -> LoginService:
    user_repository = await get_user_repository()

    return LoginService(repository=user_repository)

async def get_user_service():
    from app.services.user import UserService

    user_repository = await get_user_repository()
    return UserService(repository=user_repository)

async def get_broker_consumer_service() -> BrokerConsumerService:

    app, user_repository = await get_app_dependencies()

    return BrokerConsumerService(user_repository=user_repository, app_state=app.state)


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
