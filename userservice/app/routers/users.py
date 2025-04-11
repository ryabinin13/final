from uuid import UUID
from app.services.user import UserService
from config import config
from fastapi import APIRouter, HTTPException, Request, Response, BackgroundTasks
from typing import Annotated
from fastapi import Depends
from app.dependencies import get_current_user_id, get_login_service, get_registration_service, get_user_service
from app.schemas.user import UserLoginSchema, UserRegistrationSchema, UserUpdateSchema
from app.services.login import LoginService
from app.services.registration import RegistrationService
from exeptions import (UserAccountDeleted, UserAlreadyHasEmailException, UserAlreadyLoggedException, 
                       UserEmailNotFoundException, UserNotCorrectPasswordException)


user_router = APIRouter()


@user_router.post("/register")
async def registration(
    user_registration_schema: UserRegistrationSchema,
    request: Request,
    registration_service: Annotated[RegistrationService, Depends(get_registration_service)],

    ):
    try:
        id = await registration_service.registration(user_registration_schema, request)
        return id
    
    except UserAlreadyHasEmailException as e:
        raise HTTPException(status_code=409, detail="Пользователь с таким email уже существует")
    
    except UserAlreadyLoggedException as e:
        raise HTTPException(status_code=403, detail="Сначала выйдете из системы")
    


@user_router.post("/login")
async def login(
    user_login_schema: UserLoginSchema,
    response: Response,
    request: Request,
    login_service: Annotated[LoginService, Depends(get_login_service)],

    ):

    try:
        return await login_service.login_user(user_login_schema, request, response)
    
    except UserEmailNotFoundException as e:
        raise HTTPException(status_code=404, detail="Пользователя с таким email не существует")
    
    except UserNotCorrectPasswordException as e:
        raise HTTPException(status_code=401, detail="Неверный пароль")
    
    except UserAlreadyLoggedException as e:
        raise HTTPException(status_code=403, detail="Сначала выйдете из системы")


@user_router.delete("/logout")
async def logout(
    response: Response,

    ):
    response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME)
    return {"message": "Вы вышли из системы"}


@user_router.put("/users/me")
async def update(
    user_update_chema: UserUpdateSchema,
    user_service: Annotated[UserService, Depends(get_user_service)], 
    current_user_id: int = Depends(get_current_user_id),

    ):
    try:
        return await user_service.user_update(current_user_id, user_update_chema)
    except UserAccountDeleted:
        raise HTTPException(status_code=404, detail="Аккаунт удален")


@user_router.delete("/users/me")
async def delete(
    user_service: Annotated[UserService, Depends(get_user_service)], 
    bg: BackgroundTasks,
    current_user_id: int = Depends(get_current_user_id),

    ):
    return await user_service.user_delete(current_user_id, bg)


@user_router.post("/users/me")
async def restore_user(
    user_service: Annotated[UserService, Depends(get_user_service)], 
    current_user_id: int = Depends(get_current_user_id),

    ):
    return await user_service.user_restore(current_user_id)


