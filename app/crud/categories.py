from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


async def list_categories(db: AsyncSession) -> list[Category]:
    result = await db.execute(select(Category))
    return result.scalars().all()


async def get_category(db: AsyncSession, category_id: int) -> Category | None:
    result = await db.execute(select(Category).where(Category.id == category_id))
    return result.scalar_one_or_none()


async def create_category(db: AsyncSession, payload: CategoryCreate) -> Category:
    category = Category(**payload.model_dump())
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


async def update_category(
    db: AsyncSession, category_id: int, payload: CategoryUpdate
) -> Category | None:
    category = await get_category(db, category_id)
    if not category:
        return None
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(category, key, value)
    await db.commit()
    await db.refresh(category)
    return category


async def delete_category(db: AsyncSession, category_id: int) -> bool:
    category = await get_category(db, category_id)
    if not category:
        return False
    await db.delete(category)
    await db.commit()
    return True
