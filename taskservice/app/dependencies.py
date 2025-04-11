from fastapi import HTTPException, Request
import jwt
from app.repositories.comment import CommentRepository
from app.repositories.task import TaskRepository
from app.services.task import TaskService
from app.database import get_async_session
from config import RABBIT_CONN, config
from app.services.broker_consumer import BrokerConsumerService


def get_task_repository():
    return TaskRepository(session=get_async_session())

def get_comment_repository():
    return CommentRepository(session=get_async_session())


def get_task_service() -> TaskService:
    from app.main import app

    return TaskService(task_repository=get_task_repository(), comment_repository=get_comment_repository(), app_state=app.state)

def get_broker_consumer_service() -> BrokerConsumerService:
    from app.main import app

    return BrokerConsumerService(task_repository=get_task_repository(), app_state=app.state)


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