from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.schemas.user import UserCreate, UserRead, PaginatedUsers
from app.models.user import User, Role
from app.core.security import get_current_user, require_admin
from app.services.user_service import create_user, get_user_by_id, list_users
from app.core.security import verify_password, get_password_hash


router = APIRouter()

# User creation
@router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate):
    user = await create_user(payload)
    return UserRead(id=user.id, name=user.name, email=user.email, role=user.role)

# Get user profile
@router.get("/me", response_model=UserRead,tags="Get My Profile")
async def get_me(current: User = Depends(get_current_user)):
    return UserRead(id=current.id, name=current.name, email=current.email, role=current.role)

# Get user by it's id
@router.get("/users/{user_id}", response_model=UserRead,tags="Get User By Id")
async def get_user(user_id: str, current: User = Depends(get_current_user)):
    target = await get_user_by_id(user_id)
    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if current.role != Role.admin and current.id != target.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return UserRead(id=target.id, name=target.name, email=target.email, role=target.role)

# Retrive user list wih pagination
@router.get("/users", response_model=PaginatedUsers,tags="List User Paginated")
async def get_users(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    _: User = Depends(require_admin),
):
    users, total = await list_users(page=page, limit=limit, max_limit=100)
    data = [UserRead(id=u.id, name=u.name, email=u.email, role=u.role) for u in users]
    return PaginatedUsers(data=data, page=page, limit=limit, total=total)

# For Change User Password
@router.post("/users/change-password")
async def change_password(old_password: str, new_password: str, current: User = Depends(get_current_user)):
    if not verify_password(old_password, current.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Old password incorrect")
    current.password_hash = get_password_hash(new_password)
    await current.save()
    return {"message": "Password updated successfully"}