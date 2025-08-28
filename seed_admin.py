import asyncio
from app.core.config import settings
from app.schemas.user import UserCreate
from app.services.user_service import create_user
from app.models.user import Role, User
from app.db.session import init_db

async def main():
    await init_db()
    exists = await User.find_one(User.email == settings.ADMIN_EMAIL)
    if exists:
        print("Admin already exists:", exists.email)
        return
    admin = await create_user(
        UserCreate(name=settings.ADMIN_NAME, email=settings.ADMIN_EMAIL, password=settings.ADMIN_PASSWORD),
        role=Role.admin,
    )
    print("Admin created:", admin.email)

if __name__ == "__main__":
    asyncio.run(main())
