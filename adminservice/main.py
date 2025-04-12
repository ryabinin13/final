import sys
import os
from typing import Any, Dict
from sqladmin import Admin, ModelView
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base
from fastapi import FastAPI

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker


current_dir = os.path.dirname(os.path.abspath(__file__))

userservice_path = os.path.abspath(os.path.join(current_dir, '..'))

sys.path.insert(0, userservice_path)

from userservice.app.models.users import User
from adminservice.config import DB_USER, DB_PORT, DB_PASS, DB_HOST
class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username]

app = FastAPI()


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{"user_db"}"

async_engine = create_async_engine(
    url=DATABASE_URL,
    echo=False
)
async_sessionmaker = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


admin_user = Admin(app, async_engine) 
admin_user.add_view(UserAdmin)

