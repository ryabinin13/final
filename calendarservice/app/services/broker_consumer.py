from uuid import UUID
from app.repositories.calendar import CalendarRepository
from aio_pika.abc import AbstractIncomingMessage


class BrokerConsumerService:
    def __init__(self, calendar_repository: CalendarRepository, app_state):
        self.calendar_repository = calendar_repository
        self.app_state = app_state

    async def create_calendar(self, message: AbstractIncomingMessage):
        async with message.process():
            message_body = message.body.decode()
            team_id, title, discription = str(message_body).split()

            team_id = UUID(team_id)

            data = {"team_id": team_id, "title": title, "discription": discription}

            await self.calendar_repository.create(data)

