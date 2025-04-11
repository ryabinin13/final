import asyncio
from contextlib import asynccontextmanager
import aio_pika
from fastapi import FastAPI
from app.database import Base, async_engine
from app.dependencies import get_broker_consumer_service
from app.services.broker_producer import BrokerProducerService
from config import RABBIT_CONN
from alembic import command
from alembic.config import Config


async def connect_to_rabbitmq():
    for attempt in range(20): 
        try:
            connection = await aio_pika.connect_robust(
                RABBIT_CONN, timeout=5
            )
            print("Connected to RabbitMQ!")
            return connection
        except aio_pika.exceptions.AMQPError as e:
            print(f"Attempt {attempt+1} failed (AMQPError): {e}")
            await asyncio.sleep(2) 
        except Exception as e:  
            print(f"Attempt {attempt+1} failed (General Error): {e}")
            await asyncio.sleep(2)

    raise Exception("Failed to connect to RabbitMQ after multiple attempts")

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn: # используется асинхронный контекстный менеджер
      await conn.run_sync(Base.metadata.create_all)

    try:
        alembic_cfg = Config("alembic.ini")  # Укажите путь к вашей alembic.ini
        command.upgrade(alembic_cfg, "head") # Применяем все миграции
    except Exception as e:
        print(f"Ошибка при применении миграций: {e}")

    app.rabbit_connection = await connect_to_rabbitmq()
    app.channel = await app.rabbit_connection.channel()

    app.queue_to_team = await app.channel.declare_queue("team_from_calendar", durable=True)
    app.queue_from_team = await app.channel.declare_queue("team_to_calendar", durable=True)


    app.state.broker_producer_service = BrokerProducerService(app.channel)



    async def consume_team_messages():
        await app.queue_from_team.consume(get_broker_consumer_service().create_calendar)

    consumer_team_task = asyncio.create_task(consume_team_messages())

    yield

    await app.rabbit_connection.close()