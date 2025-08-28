from pydantic import BaseModel, EmailStr, Field
from enum import Enum

class Role(str, Enum):
    user = "user"
    admin = "admin"

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserRead(UserBase):
    id: str
    role: Role

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class PaginatedUsers(BaseModel):
    data: list[UserRead]
    page: int
    limit: int
    total: int