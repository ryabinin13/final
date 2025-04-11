from uuid import uuid4, UUID 
from app.repositories.team import TeamRepository
from app.repositories.team_memebership import TeamMembershipRepository
from aio_pika.abc import AbstractIncomingMessage


class BrokerConsumerService:
    def __init__(self, team_membership_repository: TeamMembershipRepository, team_repository: TeamRepository, app_state):
        self.team_membership_repository = team_membership_repository
        self.team_repository = team_repository
        self.app_state = app_state

    
    async def team_membership_create(self, message: AbstractIncomingMessage):
        async with message.process():
            message_body = message.body.decode()
            user_id, team_id = str(message_body).split()
            user_id = UUID(user_id)
            try:
                team_id = UUID(team_id)
            except:
                return None
            if await self.team_repository.get_id(team_id):
                data = {"team_id": team_id, "user_id": user_id}

                await self.team_membership_repository.create(data)
            
            else:
                print("Такой команды не существует")



        
    
    async def check_team_id_from_org(self, message: AbstractIncomingMessage):
        async with message.process():
            message = message.body.decode()
            team_id, name = str(message).split()
            try:
                team_id = UUID(team_id)
            except:
                return None
            team = await self.team_repository.get_id(team_id)

            if team:
                await self.app_state.broker_producer_service.publish_message_to_org(str(team_id) + " " + str(name))

    async def check_team_id_from_calendar(self, message: AbstractIncomingMessage):
        async with message.process():
            message = message.body.decode()
            team_id, title, discription = str(message).split()
            try:
                team_id = UUID(team_id)
            except:
                return None
            team = await self.team_repository.get_id(team_id)

            if team:
                await self.app_state.broker_producer_service.publish_message_to_calendar(str(team_id) + " " + str(title) + " " + str(discription))