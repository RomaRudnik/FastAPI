from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.crud.orders import (
    create_order,
    delete_order,
    get_order,
    list_orders,
    list_orders_by_user,
    update_order,
)
from app.db.database import get_db
from app.db.models import User
from app.schemas.order import OrderCreate, OrderOut, OrderUpdate

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/", response_model=list[OrderOut])
async def get_orders(db: AsyncSession = Depends(get_db)):
    return await list_orders(db)


@router.get("/my-orders", response_model=list[OrderOut])
async def get_my_orders(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await list_orders_by_user(db, current_user.id)


@router.get("/{order_id}", response_model=OrderOut)
async def get_order_by_id(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_order_item(payload: OrderCreate, db: AsyncSession = Depends(get_db)):
    return await create_order(db, payload)


@router.put("/{order_id}", response_model=OrderOut)
async def update_order_item(
    order_id: int,
    payload: OrderUpdate,
    db: AsyncSession = Depends(get_db),
):
    order = await update_order(db, order_id, payload)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.delete("/{order_id}")
async def delete_order_item(order_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await delete_order(db, order_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return {"status": "deleted"}
