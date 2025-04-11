from sqlalchemy import delete, select
from app.models.task import Task


class TaskRepository:
    def __init__(self, session):
            self.session = session

    async def create(self, data: dict):
        async with self.session as db:
            task = Task(**data)
            db.add(task)

            await db.commit() 

            return task.id
        

    async def update(self, task: Task, data: dict) -> None:
        async with self.session as db:
            for key, value in data.items():
                setattr(task, key, value)
            
            db.add(task)
            await db.commit()
            await db.refresh(task)

            return None
        
    
    async def get_id(self, id: int):
        async with self.session as db:
            query = select(Task).where(Task.id == id)
            result = await db.execute(query)
            user = result.scalar_one_or_none()
            return user
        

    async def delete(self, id) -> None:
        async with self.session as db:
            query = delete(Task).where(Task.id == id)
            await db.execute(query)
            await db.commit()

            return None