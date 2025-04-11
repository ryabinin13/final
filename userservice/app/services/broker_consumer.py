from uuid import UUID
from app.repositories.user import UserRepository
from aio_pika.abc import AbstractIncomingMessage


class BrokerConsumerService:
    def __init__(self, user_repository: UserRepository, app_state):
        self.user_repository = user_repository
        self.app_state = app_state

    
    async def check_email_from_team(self, message: AbstractIncomingMessage):
        async with message.process():
            message = message.body.decode()

            team_id, email = str(message).split()
            user = await self.user_repository.get_email(email=email)
            if user:
                await self.app_state.broker_producer_service.publish_user_data_to_team(str(user.id) + " " + team_id)
            return None
        
        
    async def check_email_from_task(self, message: AbstractIncomingMessage):
        async with message.process():
            message = message.body.decode()

            task_id, email = str(message).split()
            user = await self.user_repository.get_email(email=email)
            if user:
                await self.app_state.broker_producer_service.publish_user_data_to_task(str(user.id) + " " + task_id)
            return None
        

    async def check_email_from_meeting(self, message: AbstractIncomingMessage):
        async with message.process():
            message = message.body.decode()

            meeting_id, email = str(message).split()
            user = await self.user_repository.get_email(email=email)
            if user:
                await self.app_state.broker_producer_service.publish_user_data_to_meeting(str(user.id) + " " + meeting_id)
            return None
        
    
    async def check_email_from_org(self, message: AbstractIncomingMessage):
        async with message.process():
            message = message.body.decode()

            org_id, email = str(message).split()
            user = await self.user_repository.get_email(email=email)
            if user:
                await self.app_state.broker_producer_service.publish_user_data_to_org(str(user.id) + " " + str(org_id))
            return None