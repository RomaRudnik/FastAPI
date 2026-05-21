from pydantic import BaseModel, ConfigDict


class ProfileBase(BaseModel):
    bio: str | None = None
    phone: str | None = None


class ProfileCreate(ProfileBase):
    user_id: int


class ProfileUpdate(BaseModel):
    bio: str | None = None
    phone: str | None = None


class ProfileOut(ProfileBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
