from app.models.user import User, Role
from app.schemas.user import UserCreate
from app.core.security import get_password_hash,verify_password
from fastapi import HTTPException, status
from typing import Optional, Tuple


async def create_user(data: UserCreate, role: Role = Role.user) -> User:
    existing = await User.find_one(User.email == data.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

    user = User(
        name=data.name,
        email=data.email,
        password_hash=get_password_hash(data.password),
        role=role,
    )
    await user.insert()
    return user

from app.models import User

async def get_user_by_email(email: str) -> User | None:
    """
    Find a user by email.
    Returns User document or None.
    """
    return await User.find_one(User.email == email)

async def authenticate_user(email: str, password: str) -> Optional[User]:
    user = await User.find_one(User.email == email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

async def get_user_by_id(user_id: str) -> Optional[User]:
    return await User.find_one(User.id == user_id)

async def list_users(page: int = 1, limit: int = 20, max_limit: int = 100) -> Tuple[list[User], int]:
    if limit > max_limit:
        limit = max_limit
    total = await User.count()
    users = await User.find_all().skip((page - 1) * limit).limit(limit).to_list()
    return users, total