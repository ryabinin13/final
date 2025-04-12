from sqlalchemy import delete, select
from app.models.comment import Comment


class CommentRepository:
    def __init__(self, session):
            self.session = session

    async def create(self, data: dict):
        async with self.session as db:
            comment = Comment(**data)
            db.add(comment)

            await db.commit() 

            return comment.id