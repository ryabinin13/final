from uuid import UUID
from app.repositories.meeting import MeetingRepository
from app.repositories.meeting_memberships import MeetingMembershipsRepository
from aio_pika.abc import AbstractIncomingMessage


class BrokerConsumerService:
    def __init__(self, meeting_membership_repository: MeetingMembershipsRepository, meeting_repository: MeetingRepository, app_state):
        self.meeting_membership_repository = meeting_membership_repository
        self.meeting_repository = meeting_repository
        self.app_state = app_state


    async def meeting_membership_create(self, message: AbstractIncomingMessage):
        async with message.process():
            message_body = message.body.decode()
            user_id, meeting_id = str(message_body).split()[-2:]
            user_id = UUID(user_id)

            meeting_id = int(meeting_id)

            if await self.meeting_repository.get_id(meeting_id):
                data = {"meeting_id": meeting_id, "user_id": user_id}

                await self.meeting_membership_repository.create(data)
            
            else:
                print("Такой команды не существует")

            await message.ack()