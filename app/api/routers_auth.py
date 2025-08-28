from fastapi import APIRouter, HTTPException, status
from app.schemas import UserCreate, UserLogin, Token
from core.security import get_password_hash, verify_password, create_access_token
from services.user_service import get_user_by_email, create_user

router = APIRouter(tags=["auth"])

# For User Register
@router.post("/users", response_model=UserCreate, status_code=status.HTTP_201_CREATED,tags="Register")
async def register(payload: UserCreate):
    existing = await get_user_by_email(payload.email)
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    hashed = get_password_hash(payload.password)
    user = await create_user(name=payload.name, email=payload.email, password_hash=hashed)

    return UserCreate(id=str(user.id), name=user.name, email=user.email, role=user.role)

# User Login
@router.post("/login", response_model=Token,tags="Login")
async def login(payload: UserLogin):
    user = await get_user_by_email(payload.email)
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(str(user.id))
    return Token(access_token=token, expires_in=30)
