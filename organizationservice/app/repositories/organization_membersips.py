from uuid import UUID
from app.models.organization_membership import OrganizationMembership
from sqlalchemy import select, delete


class OrganizationMembershipsRepository:
    def __init__(self, session):
        self.session = session


    async def create(self, data: dict):
        async with self.session as db:
            org = OrganizationMembership(**data)
            db.add(org)

            await db.commit() 

            return org.id
        

    async def get_user_id(self, user_id: UUID):
        async with self.session as db:
            query = select(OrganizationMembership).where(OrganizationMembership.user_id == user_id)
            result = await db.execute(query)
            org_membership = result.scalar_one_or_none()
            return org_membership
        
    async def delete(self, id) -> None:
        async with self.session as db:
            query = delete(OrganizationMembership).where(OrganizationMembership.id == id)
            await db.execute(query)
            await db.commit()

            return None