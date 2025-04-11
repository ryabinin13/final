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


async def connect_to_rabbitmq():
    for attempt in range(40):  # Увеличил количество попыток
        try:
            rabbitmq_host = os.environ.get("RABBITMQ_HOST", "localhost")
            connection = await connect_robust(
                f"amqp://user:password@{rabbitmq_host}/", timeout=5  # Добавил timeout
            )
            print("Connected to RabbitMQ!")
            return connection
        except aio_pika.exceptions.AMQPError as e:  # Ловим специфичные исключения aio_pika
            print(f"Attempt {attempt+1} failed (AMQPError): {e}")
            await asyncio.sleep(2)  # Ждем перед следующей попыткой
        except Exception as e:  # Ловим другие исключения
            print(f"Attempt {attempt+1} failed (General Error): {e}")
            await asyncio.sleep(2)

    raise Exception("Failed to connect to RabbitMQ after multiple attempts")


@asynccontextmanager
async def lifespan(app: FastAPI):

    async with async_engine.begin() as conn: # используется асинхронный контекстный менеджер
      await conn.run_sync(Base.metadata.create_all)

    # try:
    #     alembic_cfg = Config("alembic.ini")  # Укажите путь к вашей alembic.ini
    #     command.upgrade(alembic_cfg, "head") # Применяем все миграции
    # except Exception as e:
    #     print(f"Ошибка при применении миграций: {e}")


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

    consumer_user_task = asyncio.create_task(consume_mark_messages())

    yield


    consumer_user_task.cancel()
    await app.rabbit_connection.close()
