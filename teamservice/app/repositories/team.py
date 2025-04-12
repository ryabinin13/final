from uuid import UUID

from sqlalchemy import select
from app.models.team import Team


class TeamRepository:

    def __init__(self, session):
        self.session = session

    async def create(self, data: dict):
        async with self.session as db:
            team = Team(**data)
            db.add(team)

            await db.commit() 

            return team.id
        
    async def get_id(self, id: UUID):
        async with self.session as db:
            query = select(Team).where(Team.id == id)
            result = await db.execute(query)
            team = result.scalar_one_or_none()
            return team