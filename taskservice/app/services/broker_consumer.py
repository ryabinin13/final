from uuid import uuid4, UUID 
from app.repositories.task import TaskRepository
from aio_pika.abc import AbstractIncomingMessage


class BrokerConsumerService:
    def __init__(self, task_repository: TaskRepository, app_state):
        self.task_repository = task_repository
        self.app_state = app_state

    
    async def task_add_user(self, message: AbstractIncomingMessage):
        async with message.process():
            message_body = message.body.decode()
            user_id, task_id = str(message_body).split()[-2:]
            user_id = UUID(user_id)

            task_id = int(task_id)

            task = await self.task_repository.get_id(task_id)
            if task:
                data = {"user_id": user_id}

                await self.task_repository.update(task, data)



    
    async def check_task_id(self, message: AbstractIncomingMessage):
        async with message.process():
            message_body = message.body.decode()
            task_id, mark = str(message_body).split()

            task_id = int(task_id)
            task = await self.task_repository.get_id(task_id)
            if task:
                await self.app_state.broker_producer_service.publish_mark_to_mark(str(task_id) + " " + str(mark) + " " + str(task.user_id))
                
                
            
