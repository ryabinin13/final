from uuid import UUID

from sqlalchemy import select, delete
from app.models.team_memberships import TeamMemberships


class TeamMembershipRepository:

    def __init__(self, session):
        self.session = session

    async def create(self, data: dict):
        async with self.session as db:
            team = TeamMemberships(**data)
            db.add(team)

            await db.commit() 

            return team.user_id
        

    async def get_user_id(self, user_id: UUID):
        async with self.session as db:
            query = select(TeamMemberships).where(TeamMemberships.user_id == user_id)
            result = await db.execute(query)
            team_membership = result.scalar_one_or_none()
            return team_membership
    

    async def update(self, team_membership: TeamMemberships, data: dict) -> None:
        async with self.session as db:
            for key, value in data.items():
                setattr(team_membership, key, value)
            
            db.add(team_membership)
            await db.commit()
            await db.refresh(team_membership)

            return None
        
    async def delete(self, id) -> None:
        async with self.session as db:
            query = delete(TeamMemberships).where(TeamMemberships.id == id)
            await db.execute(query)
            await db.commit()

            return None