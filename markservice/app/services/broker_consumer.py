from uuid import UUID
from app.repositories.mark import MarkRepository
from aio_pika.abc import AbstractIncomingMessage


class BrokerConsumerService:
    def __init__(self, mark_repository: MarkRepository, app_state):
        self.mark_repository = mark_repository
        self.app_state = app_state


    async def task_add_user(self, message: AbstractIncomingMessage):
        async with message.process():
            message_body = message.body.decode()
            task_id, mark, user_id = str(message_body).split()
            try:
                user_id = UUID(user_id)
            except:
                raise Exception

            task_id = int(task_id)
            mark = int(mark)

            data = {"user_id": user_id, "task_id": task_id, "mark": mark}

            await self.mark_repository.create(data)

