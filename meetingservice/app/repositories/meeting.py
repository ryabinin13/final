from sqlalchemy import delete, select
from app.models.meeting import Meeting


class MeetingRepository:
    def __init__(self, session):
        self.session = session

    async def create(self, data: dict):
        async with self.session as db:
            meeting = Meeting(**data)
            db.add(meeting)

            await db.commit() 

            return meeting.id


    async def get_id(self, id):
        async with self.session as db:
            query = select(Meeting).where(Meeting.id == id)
            result = await db.execute(query)
            meeting = result.scalar_one_or_none()
            return meeting
        
        
    async def delete(self, id) -> None:
        async with self.session as db:
            query = delete(Meeting).where(Meeting.id == id)
            await db.execute(query)
            await db.commit()

            return None
        

    async def update(self, meeting: Meeting, data: dict) -> None:
        async with self.session as db:
            for key, value in data.items():
                setattr(meeting, key, value)
            
            db.add(meeting)
            await db.commit()
            await db.refresh(meeting)

            return None
