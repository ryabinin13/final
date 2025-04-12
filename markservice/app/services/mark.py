from app.repositories.mark import MarkRepository
from app.schemas.mark import CreateMarkSchema


class MarkService:
    def __init__(self, mark_repository, app_state):       
        self.mark_repository = mark_repository
        self.app_state = app_state

    async def create_mark(self, create_mark_schema: CreateMarkSchema):
        task_id = create_mark_schema.task_id
        mark = create_mark_schema.mark
        await self.app_state.broker_producer_service.publish_task_id_to_task(str(task_id) + " " + str(mark))

    async def get_marks(self, user_id):
        return await self.mark_repository.get_marks(user_id)