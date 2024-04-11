from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from config import DB_NAME, DB_PORT, DB_USER, DB_HOST, DB_PASS

DATABASE_URL = f'postgresql+asyncpg://new_user:new_user@localhost:5432/Newdatabase'

engine = create_async_engine(DATABASE_URL, echo=True)
