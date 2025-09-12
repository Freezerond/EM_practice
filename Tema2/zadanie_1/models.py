import datetime
from typing import Annotated, Optional
from sqlalchemy import text, Numeric
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from bookstore import Base, str_64

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]


class Genre(Base):
    __tablename__ = 'genres'

    id: Mapped[intpk]
    title: Mapped[str_64]

    books: Mapped[list["Book"]] = relationship(back_populates="genre")


class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[intpk]
    name: Mapped[str_64]

    books: Mapped[list["Book"]] = relationship(back_populates="author")


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[intpk]
    title: Mapped[str_64]
    price: Mapped[float] = mapped_column(Numeric(10, 2))
    quantity: Mapped[int] = mapped_column(default=0)
    genre_id: Mapped[Optional[int]] = mapped_column(ForeignKey('genres.id', ondelete='SET NULL'))
    author_id: Mapped[Optional[int]] = mapped_column(ForeignKey('authors.id', ondelete='SET NULL'))

    author: Mapped["Author"] = relationship(back_populates="books")
    genre: Mapped["Genre"] = relationship(back_populates="books")
    orders_with_book: Mapped[list["Order"]] = relationship(back_populates="books_in_order", secondary="order_books")


class City(Base):
    __tablename__ = 'cities'

    id: Mapped[intpk]
    name: Mapped[str_64]
    delivery_time_days: Mapped[int]

    clients: Mapped[list["Client"]] = relationship(back_populates="city")


class Client(Base):
    __tablename__ = 'clients'

    id: Mapped[intpk]
    name: Mapped[str_64]
    mail: Mapped[str_64] = mapped_column(unique=True)
    city_id: Mapped[Optional[int]] = mapped_column(ForeignKey('cities.id', ondelete='SET NULL'))

    city: Mapped["City"] = relationship(back_populates="clients")
    orders: Mapped[list["Order"]] = relationship(back_populates="client")


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[intpk]
    comment: Mapped[Optional[str]]
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id', ondelete='CASCADE'))

    client: Mapped["Client"] = relationship(back_populates="orders")
    books_in_order: Mapped[list["Book"]] = relationship(back_populates="orders_with_book", secondary="order_books")
    steps: Mapped[list["Step"]] = relationship(back_populates="orders", secondary="order_steps")


class OrderBook(Base):
    __tablename__ = 'order_books'

    quantity: Mapped[int] = mapped_column(default=1)
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id', ondelete='CASCADE'), primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id', ondelete='CASCADE'), primary_key=True)


class Step(Base):
    __tablename__ = 'steps'

    id: Mapped[intpk]
    name: Mapped[str_64]

    orders: Mapped[list["Order"]] = relationship(back_populates="steps", secondary="order_steps")


class OrderStep(Base):
    __tablename__ = 'order_steps'

    start_date: Mapped[created_at]
    end_date: Mapped[Optional[datetime.datetime]]
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id', ondelete='CASCADE'), primary_key=True)
    step_id: Mapped[int] = mapped_column(ForeignKey('steps.id', ondelete='CASCADE'), primary_key=True)
