import datetime

from sqlalchemy import text, String, Date, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from typing import Annotated

from database.database import Base, int_19

created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=datetime.datetime.utcnow
)]


class SpimexTradingResults(Base):
    __tablename__ = 'spimex_trading_results'
    __table_args__ = (
        UniqueConstraint("date", "exchange_product_id", name="spimex_trade_unique"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    exchange_product_id: Mapped[str] = mapped_column(String(11))
    exchange_product_name: Mapped[str] = mapped_column(String(512))
    oil_id: Mapped[str] = mapped_column(String(4))
    delivery_basis_id: Mapped[str] = mapped_column(String(3))
    delivery_basis_name: Mapped[str] = mapped_column(String(64))
    delivery_type_id: Mapped[str] = mapped_column(String(1))
    volume: Mapped[int_19]
    total: Mapped[int_19]
    count: Mapped[int_19]
    date: Mapped[datetime.date]
    created_on: Mapped[created_at]
    updated_on: Mapped[updated_at]
