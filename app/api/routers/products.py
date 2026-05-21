from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.products import (
    create_product,
    delete_product,
    get_product,
    list_products,
    update_product,
)
from app.db.database import get_db
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=list[ProductOut])
async def get_products(db: AsyncSession = Depends(get_db)):
    return await list_products(db)


@router.get("/{product_id}", response_model=ProductOut)
async def get_product_by_id(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product_item(
    payload: ProductCreate, db: AsyncSession = Depends(get_db)
):
    return await create_product(db, payload)


@router.put("/{product_id}", response_model=ProductOut)
async def update_product_item(
    product_id: int,
    payload: ProductUpdate,
    db: AsyncSession = Depends(get_db),
):
    product = await update_product(db, product_id, payload)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.delete("/{product_id}")
async def delete_product_item(product_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return {"status": "deleted"}
