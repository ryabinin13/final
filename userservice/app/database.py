from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from config import DB_USER, DB_PORT, DB_PASS, DB_HOST, DB_NAME


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

async_engine = create_async_engine(
    url=DATABASE_URL,
    echo=False
)
get_async_session = async_sessionmaker(async_engine, autocommit=False, autoflush=False, expire_on_commit=False)

Base = declarative_base()


