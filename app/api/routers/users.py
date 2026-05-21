from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.users import (
    create_user,
    delete_user,
    get_user,
    list_users,
    update_user,
)
from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.db.models import User
from app.schemas.user import UserCreate, UserOut, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserOut])
async def get_users(db: AsyncSession = Depends(get_db)):
    return await list_users(db)


@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=UserOut)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user_item(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, payload)


@router.put("/{user_id}", response_model=UserOut)
async def update_user_item(
    user_id: int,
    payload: UserUpdate,
    db: AsyncSession = Depends(get_db),
):
    user = await update_user(db, user_id, payload)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.delete("/{user_id}")
async def delete_user_item(user_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"status": "deleted"}
