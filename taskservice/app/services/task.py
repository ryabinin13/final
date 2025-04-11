
from app.repositories.comment import CommentRepository
from app.repositories.task import TaskRepository
from app.schemas.task import CreateTaskSchema
from datetime import datetime

class TaskService:
    def __init__(self, task_repository: TaskRepository, comment_repository: CommentRepository, app_state):
        self.task_repository = task_repository
        self.comment_repository = comment_repository
        self.app_state = app_state


    async def create_task(self, create_task_schema: CreateTaskSchema):

        data = create_task_schema.model_dump()
        return await self.task_repository.create(data)


    async def add_user(self, task_id, email):
        await self.app_state.broker_producer_service.publish_add_user_in_task(task_id, email)
        
    async def update_task(self, task_id, update_task_schema):

        task = await self.task_repository.get_id(task_id)
        if not task:
            raise Exception

        task_dict = {k: v for k, v in update_task_schema.model_dump().items() if v is not None}

        return await self.task_repository.update(task=task, data=task_dict)
    

    async def delete_task(self, task_id):
        return await self.task_repository.delete(task_id)
    

    async def add_comment(self, task_id, text):
        date_comm = datetime.now()
        data_comment = {"task_id": task_id, "date": date_comm, "text": text}
        return await self.comment_repository.create(data_comment)
    
    async def change_status(self, task_id, status):
        task = await self.task_repository.get_id(task_id)
        if task:
            data = {"status", status}

            return await self.task_repository.update(task, data)