from fastapi import APIRouter, HTTPException, status

from app.db.fake_db import create_user, delete_user, get_user, list_users, update_user
from app.schemas.user import UserCreate, UserOut, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserOut])
def get_users():
    return list_users()


@router.get("/{user_id}", response_model=UserOut)
def get_user_by_id(user_id: int):
    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user_item(payload: UserCreate):
    return create_user(payload)


@router.put("/{user_id}", response_model=UserOut)
def update_user_item(user_id: int, payload: UserUpdate):
    user = update_user(user_id, payload)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.delete("/{user_id}")
def delete_user_item(user_id: int):
    deleted = delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"status": "deleted"}
