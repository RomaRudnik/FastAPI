from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Profile
from app.schemas.profile import ProfileCreate, ProfileUpdate


async def list_profiles(db: AsyncSession) -> list[Profile]:
    result = await db.execute(select(Profile))
    return result.scalars().all()


async def get_profile(db: AsyncSession, profile_id: int) -> Profile | None:
    result = await db.execute(select(Profile).where(Profile.id == profile_id))
    return result.scalar_one_or_none()


async def create_profile(db: AsyncSession, payload: ProfileCreate) -> Profile:
    profile = Profile(**payload.model_dump())
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return profile


async def update_profile(
    db: AsyncSession, profile_id: int, payload: ProfileUpdate
) -> Profile | None:
    profile = await get_profile(db, profile_id)
    if not profile:
        return None
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(profile, key, value)
    await db.commit()
    await db.refresh(profile)
    return profile


async def delete_profile(db: AsyncSession, profile_id: int) -> bool:
    profile = await get_profile(db, profile_id)
    if not profile:
        return False
    await db.delete(profile)
    await db.commit()
    return True
