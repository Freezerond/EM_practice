from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import URL, create_engine, text

from config import settings

engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True
)
