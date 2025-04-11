from sqlalchemy import delete, select
from app.models.users import User


class UserRepository:

    def __init__(self, session):
        self.session = session

    async def create(self, data: dict):
        async with self.session as db:
            user = User(**data)
            db.add(user)

            await db.commit() 

            return user.id

    async def get_email(self, email: str):
        async with self.session as db:
            query = select(User).where(User.email == email)
            result = await db.execute(query)
            user = result.scalar_one_or_none()
            return user

    async def get_id(self, id):
        async with self.session as db:
            query = select(User).where(User.id == id)
            result = await db.execute(query)
            user = result.scalar_one_or_none()
            return user
        
    async def change_active(self, user: User, active: bool):
        async with self.session as db:
            user.is_active = active
            db.add(user)
            await db.commit()
        
    async def delete(self, id) -> None:
        async with self.session as db:
            query = delete(User).where(User.id == id)
            await db.execute(query)
            await db.commit()

            return None
        
    async def update(self, user: User, data: dict) -> None:
        async with self.session as db:
            for key, value in data.items():
                setattr(user, key, value)
            
            db.add(user)
            await db.commit()
            await db.refresh(user)

            return None
