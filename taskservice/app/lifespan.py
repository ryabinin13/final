import asyncio
from contextlib import asynccontextmanager
import os
from aio_pika import connect, connect_robust
import aio_pika
from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from app.database import Base, async_engine
from app.dependencies import get_broker_consumer_service
from app.services.broker_producer import BrokerProducerService
from config import RABBIT_CONN
from config import RABBIT_ATTEMPTS
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) 

console_handler = logging.StreamHandler()  

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)


async def connect_to_rabbitmq() -> aio_pika.RobustConnection: 

    for attempt in range(RABBIT_ATTEMPTS):
        try:
            connection = await aio_pika.connect_robust(
                RABBIT_CONN, timeout=5
            )
            logger.info("Connected to RabbitMQ!")
            return connection
        except aio_pika.exceptions.AMQPError as e:
            logger.warning(f"Attempt {attempt+1} failed (AMQPError): {e}")
            await asyncio.sleep(2)
        except Exception as e:
            logger.exception(f"Attempt {attempt+1} failed (General Error): {e}") 
            await asyncio.sleep(2)

    raise Exception("Failed to connect to RabbitMQ after multiple attempts")


@asynccontextmanager
async def lifespan(app: FastAPI):

    # async with async_engine.begin() as conn: # используется асинхронный контекстный менеджер
    #   await conn.run_sync(Base.metadata.create_all)

    try:
        alembic_cfg = Config("alembic.ini")  # Укажите путь к вашей alembic.ini
        command.upgrade(alembic_cfg, "head") # Применяем все миграции
    except Exception as e:
        print(f"Ошибка при применении миграций: {e}")


    app.rabbit_connection = await connect_to_rabbitmq()
    app.channel = await app.rabbit_connection.channel()

    app.queue_from_user = await app.channel.declare_queue("user_to_task", durable=True)
    app.queue_to_user = await app.channel.declare_queue("user_email_from_task", durable=True)

    app.queue_from_mark = await app.channel.declare_queue("mark_to_task", durable=True)
    app.queue_to_mark = await app.channel.declare_queue("mark_from_task", durable=True)

    app.state.broker_producer_service = BrokerProducerService(app.channel)

    async def consume_user_messages():
        await app.queue_from_user.consume(get_broker_consumer_service().task_add_user)

    async def consume_mark_messages():
        await app.queue_from_mark.consume(get_broker_consumer_service().check_task_id)
    
    consumer_user_task = asyncio.create_task(consume_user_messages())

    consumer_mark_task = asyncio.create_task(consume_mark_messages())

    yield


    consumer_mark_task.cancel()
    consumer_user_task.cancel()
    await asyncio.gather(consumer_user_task, consumer_mark_task, return_exceptions=True) 

    await app.channel.close()


    await app.rabbit_connection.close()
