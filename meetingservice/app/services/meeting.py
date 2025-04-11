from datetime import timezone
from app.repositories.meeting import MeetingRepository
from app.repositories.meeting_memberships import MeetingMembershipsRepository
from app.schemas.meeting import CreateMeetingSchema


class MeetingService:
    def __init__(self, meeting_repository: MeetingRepository, meeting_memberships_repository: MeetingMembershipsRepository, app_state):
        self.meeting_repository = meeting_repository
        self.meeting_memberships_repository = meeting_memberships_repository
        self.app_state = app_state


    async def create_meeting(self, create_meeting_service: CreateMeetingSchema):

        data = create_meeting_service.model_dump()

        data["date"] = data["date"].replace(tzinfo=None)

        return await self.meeting_repository.create(data)
    

    async def meeting_delete(self, id):
        meeting = await self.meeting_repository.get_id(id=id)
        if meeting:
            return await self.meeting_repository.delete(id)


    async def meeting_update(self, id, update_meeting_schema):
        meeting = await self.meeting_repository.get_id(id=id)
        if meeting:
            meeting_dict = {k: v for k, v in update_meeting_schema.model_dump().items() if v is not None}

            if meeting_dict["date"]:
                meeting_dict["date"] = meeting_dict["date"].replace(tzinfo=None)

            return await self.meeting_repository.update(meeting=meeting, data=meeting_dict)


    async def add_user(self, meeting_id, email):

        await self.app_state.broker_producer_service.publish_message_to_user(str(meeting_id) + " " + str(email))
