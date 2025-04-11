from sqlalchemy import delete, select
from app.models.mark import Mark


class MarkRepository:
    def __init__(self, session):
        self.session = session


    async def create(self, data: dict):
        async with self.session as db:
            mark = Mark(**data)
            db.add(mark)

            await db.commit() 

            return mark.id
        
    async def get_marks(self, id):
        async with self.session as db:
            query = select(Mark).where(Mark.user_id == id)
            marks = await db.execute(query)
            return marks.scalars().all()
        