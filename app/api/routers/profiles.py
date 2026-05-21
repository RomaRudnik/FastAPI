from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.profiles import (
    create_profile,
    delete_profile,
    get_profile,
    list_profiles,
    update_profile,
)
from app.db.database import get_db
from app.schemas.profile import ProfileCreate, ProfileOut, ProfileUpdate

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/", response_model=list[ProfileOut])
async def get_profiles(db: AsyncSession = Depends(get_db)):
    return await list_profiles(db)


@router.get("/{profile_id}", response_model=ProfileOut)
async def get_profile_by_id(profile_id: int, db: AsyncSession = Depends(get_db)):
    profile = await get_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile


@router.post("/", response_model=ProfileOut, status_code=status.HTTP_201_CREATED)
async def create_profile_item(
    payload: ProfileCreate, db: AsyncSession = Depends(get_db)
):
    return await create_profile(db, payload)


@router.put("/{profile_id}", response_model=ProfileOut)
async def update_profile_item(
    profile_id: int,
    payload: ProfileUpdate,
    db: AsyncSession = Depends(get_db),
):
    profile = await update_profile(db, profile_id, payload)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile


@router.delete("/{profile_id}")
async def delete_profile_item(profile_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await delete_profile(db, profile_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return {"status": "deleted"}
