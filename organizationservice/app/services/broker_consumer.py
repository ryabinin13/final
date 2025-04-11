from uuid import uuid4, UUID 
from app.repositories.organization import OrganizationRepository
from app.repositories.organization_membersips import OrganizationMembershipsRepository
from aio_pika.abc import AbstractIncomingMessage


class BrokerConsumerService:
    def __init__(self, organization_membership_repository: OrganizationMembershipsRepository, organization_repository: OrganizationRepository):
        self.organization_membership_repository = organization_membership_repository
        self.organization_repository = organization_repository

    async def org_create(self, message: AbstractIncomingMessage):
        message_body = message.body.decode()
        team_id, name = str(message_body).split()
        try:
            team_id = UUID(team_id)
        except:
            return None
        
        data = {"name": name, "team_id": team_id}
        await self.organization_repository.create(data)
        

        await message.ack()


    async def org_membership_create(self, message: AbstractIncomingMessage):
        message_body = message.body.decode()
        org_id, user_id = str(message_body).split()
        try:
            user_id = UUID(user_id)
        except:
            return None
        
        data = {"id": org_id, "user_id": user_id}
        await self.organization_membership_repository.create(data)
        

        await message.ack()