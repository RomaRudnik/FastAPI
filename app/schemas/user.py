from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr
    age: int | None = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    age: int | None = None


class UserOut(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserInDB(UserOut):
    pass
