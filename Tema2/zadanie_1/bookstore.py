from typing import Annotated

from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine, String, text

from config import settings

engine = create_engine(url=settings.DATABASE_URL_psycopg)
session_factory = sessionmaker(engine)

str_64 = Annotated[str, 64]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_64: String(64)
    }
