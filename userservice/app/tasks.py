import asyncio

from aio_pika import connect_robust
from app.dependencies import get_broker_consumer_service
from app.repositories.user import UserRepository
from app.database import get_async_session
from app.services.broker_producer import BrokerProducerService
from config import RABBIT_CONN


async def delete_user(user_id):
    user_repository = UserRepository(session=get_async_session())

    await asyncio.sleep(24*60*60)
    user = await user_repository.get_id(user_id)
    if user.is_active:
        return None
    await user_repository.delete(user_id)


