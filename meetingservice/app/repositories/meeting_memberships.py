from app.models.meeting_memberships import MeetingMemberships


class MeetingMembershipsRepository:
    def __init__(self, session):
        self.session = session

    async def create(self, data: dict):
        async with self.session as db:
            meeting = MeetingMemberships(**data)
            db.add(meeting)

            await db.commit() 

            return meeting.id
