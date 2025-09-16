from pandas import DataFrame
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import Base, async_engine
from database.spimex_trading_results import SpimexTradingResults


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def save_to_postgres(session: AsyncSession, df: DataFrame, trade_date):
    for _, row in df.iterrows():
        exchange_product_id = row.get("exchange_product_id")
        oil_id = exchange_product_id[:4] if exchange_product_id else None
        delivery_basis_id = exchange_product_id[4:7] if exchange_product_id and len(exchange_product_id) >= 7 else None
        delivery_type_id = exchange_product_id[-1] if exchange_product_id else None

        stmt = insert(SpimexTradingResults).values(
            exchange_product_id=exchange_product_id,
            exchange_product_name=row.get("exchange_product_name"),
            oil_id=oil_id,
            delivery_basis_id=delivery_basis_id,
            delivery_basis_name=row.get("delivery_basis_name"),
            delivery_type_id=delivery_type_id,
            volume=int(row.get("volume")) if row.get("volume") is not None else None,
            total=int(row.get("total")) if row.get("total") is not None else None,
            count=int(row.get("count")) if row.get("count") is not None else None,
            date=trade_date
        ).on_conflict_do_update(
            index_elements=['date', 'exchange_product_id'],
            set_={
                'exchange_product_name': row.get("exchange_product_name"),
                'oil_id': oil_id,
                'delivery_basis_id': delivery_basis_id,
                'delivery_basis_name': row.get("delivery_basis_name"),
                'delivery_type_id': delivery_type_id,
                'volume': int(row.get("volume")) if row.get("volume") is not None else None,
                'total': int(row.get("total")) if row.get("total") is not None else None,
                'count': int(row.get("count")) if row.get("count") is not None else None,
            }
        )
        await session.execute(stmt)
    await session.commit()
