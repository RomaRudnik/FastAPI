from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Order
from app.schemas.order import OrderCreate, OrderUpdate


async def list_orders(db: AsyncSession) -> list[Order]:
    result = await db.execute(select(Order))
    return result.scalars().all()


async def get_order(db: AsyncSession, order_id: int) -> Order | None:
    result = await db.execute(select(Order).where(Order.id == order_id))
    return result.scalar_one_or_none()


async def create_order(db: AsyncSession, payload: OrderCreate) -> Order:
    order = Order(**payload.model_dump())
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order


async def update_order(db: AsyncSession, order_id: int, payload: OrderUpdate) -> Order | None:
    order = await get_order(db, order_id)
    if not order:
        return None
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(order, key, value)
    await db.commit()
    await db.refresh(order)
    return order


async def delete_order(db: AsyncSession, order_id: int) -> bool:
    order = await get_order(db, order_id)
    if not order:
        return False
    await db.delete(order)
    await db.commit()
    return True
