import select
from app.models.organization import Organization


class OrganizationRepository:
    def __init__(self, session):
        self.session = session



    async def create(self, data: dict):
        async with self.session as db:
            org = Organization(**data)
            db.add(org)

            await db.commit() 

            return org.id
        

    async def get_id(self, id: int) -> Organization:
        async with self.async_session as db:
            query = select(Organization).where(Organization.id == int(id))
            org = await db.execute(query)
            return org.scalars().first()