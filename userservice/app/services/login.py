import datetime

from fastapi import Request, Response
import jwt
from app.repositories.user import UserRepository
from app.schemas.user import UserLoginSchema
from config import config
from exeptions import UserEmailNotFoundException, UserNotCorrectPasswordException, UserAlreadyLoggedException
from werkzeug.security import check_password_hash


class LoginService:
    def __init__(self, repository: UserRepository):
        self.user_repository = repository

    async def _authenticate_user(self, user_login_schema: UserLoginSchema):
        user = await self.user_repository.get_email(user_login_schema.email)
        if not user:
            raise UserEmailNotFoundException
        
        if not check_password_hash(user.password_hash, user_login_schema.password):
            raise UserNotCorrectPasswordException

        return user
    
    async def _generate_token(self, user_id: int):
        payload = {
            "uid": str(user_id),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=config.JWT_ACCESS_TOKEN_EXPIRES) 
        }
        try:
            encoded_jwt = jwt.encode(payload, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)
            return encoded_jwt
        except Exception as e:
            raise 
        
    async def login_user(self, user_login: UserLoginSchema, request: Request, response: Response) -> dict:
        token = request.cookies.get(config.JWT_ACCESS_COOKIE_NAME)
        if not token:
            user = await self._authenticate_user(user_login)
            token = await self._generate_token(user.id)
            response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
            return {"access_token": token}
        raise UserAlreadyLoggedException
        




    