from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    age: int | None = None
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
