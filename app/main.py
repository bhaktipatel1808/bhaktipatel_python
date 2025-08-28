from fastapi import FastAPI
from app.api.routers_users import router as users_router
from app.api.routers_auth import router as auth_router
from app.db.session import init_db

app = FastAPI(title="User Management API (MongoDB)")

@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(auth_router, tags=["auth"])
app.include_router(users_router, tags=["users"])