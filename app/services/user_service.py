from app.models.user import User, Role
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from fastapi import HTTPException, status

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
