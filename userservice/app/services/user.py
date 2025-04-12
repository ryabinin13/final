from app.repositories.user import UserRepository
from app.schemas.user import UserUpdateSchema
from werkzeug.security import generate_password_hash
from fastapi import BackgroundTasks
from app.tasks import delete_user
from exeptions import UserAccountDeleted


class UserService:

    def __init__(self, repository: UserRepository):
        self.user_repository = repository

    
    async def user_update(self, current_user_id: int, user_update_schema: UserUpdateSchema):
        user = await self.user_repository.get_id(id=current_user_id)
        if not user.is_active:
            raise UserAccountDeleted
        
        user_dict = {k: v for k, v in user_update_schema.model_dump().items() if v is not None}

        if user_dict["password"]:
            password_hash = generate_password_hash(user_dict["password"])
            del user_dict["password"]
            user_dict["password_hash"] = password_hash


        return await self.user_repository.update(user=user, data=user_dict)
    

    async def user_delete(self, current_user_id, bg: BackgroundTasks):
        user = await self.user_repository.get_id(id=current_user_id)

        await self.user_repository.change_active(user, False)

        bg.add_task(delete_user, current_user_id)

    
    async def user_restore(self, current_user_id):
        user = await self.user_repository.get_id(id=current_user_id)

        return await self.user_repository.change_active(user, True)
