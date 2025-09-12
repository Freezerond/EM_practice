import models
from bookstore import Base, engine


def create_tables():
    Base.metadata.create_all(engine)


create_tables()