from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.categories import (
    create_category,
    delete_category,
    get_category,
    list_categories,
    update_category,
)
from app.db.database import get_db
from app.schemas.category import CategoryCreate, CategoryOut, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=list[CategoryOut])
async def get_categories(db: AsyncSession = Depends(get_db)):
    return await list_categories(db)


@router.get("/{category_id}", response_model=CategoryOut)
async def get_category_by_id(category_id: int, db: AsyncSession = Depends(get_db)):
    category = await get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category


@router.post("/", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
async def create_category_item(
    payload: CategoryCreate, db: AsyncSession = Depends(get_db)
):
    return await create_category(db, payload)


@router.put("/{category_id}", response_model=CategoryOut)
async def update_category_item(
    category_id: int,
    payload: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
):
    category = await update_category(db, category_id, payload)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category


@router.delete("/{category_id}")
async def delete_category_item(category_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await delete_category(db, category_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return {"status": "deleted"}
