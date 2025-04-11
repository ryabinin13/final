from fastapi import Request
from app.repositories.user import UserRepository
from app.schemas.user import UserRegistrationSchema
from werkzeug.security import generate_password_hash
from exeptions import UserAlreadyHasEmailException, UserAlreadyLoggedException
from config import config


class RegistrationService:

    def __init__(self, repository: UserRepository, app_state):
        self.user_repository = repository
        self.app_state = app_state


    async def registration(self, user_registration_schema: UserRegistrationSchema, request: Request):

        token = request.cookies.get(config.JWT_ACCESS_COOKIE_NAME)
        if token:
            raise UserAlreadyLoggedException

        user = await self.user_repository.get_email(email=user_registration_schema.email)
        if user:
            raise UserAlreadyHasEmailException
        
        team_id = user_registration_schema.team_id
        password_hash = generate_password_hash(user_registration_schema.password1)
        user_dict = user_registration_schema.model_dump(exclude=["password2", "password1", "team_id"])
        user_dict["password_hash"] = password_hash

        id = await self.user_repository.create(user_dict)
        
        if team_id:
            await self.app_state.broker_producer_service.publish_user_data_to_team(str(id) + " " + team_id)
        return id