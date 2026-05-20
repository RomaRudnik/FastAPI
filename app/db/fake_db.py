from app.schemas.user import UserCreate, UserInDB, UserUpdate

_users: dict[int, UserInDB] = {}
_next_id = 1


def list_users() -> list[UserInDB]:
    return list(_users.values())


def get_user(user_id: int) -> UserInDB | None:
    return _users.get(user_id)


def create_user(payload: UserCreate) -> UserInDB:
    global _next_id
    user = UserInDB(id=_next_id, **payload.model_dump())
    _users[_next_id] = user
    _next_id += 1
    return user


def update_user(user_id: int, payload: UserUpdate) -> UserInDB | None:
    existing = _users.get(user_id)
    if not existing:
        return None
    updated = existing.model_copy(update=payload.model_dump(exclude_unset=True))
    _users[user_id] = updated
    return updated


def delete_user(user_id: int) -> bool:
    return _users.pop(user_id, None) is not None
