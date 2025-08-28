from beanie import Document
from datetime import datetime
from enum import Enum
import uuid
from pydantic import Field, EmailStr

class Role(str, Enum):
    user = "user"
    admin = "admin"

class User(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: EmailStr
    password_hash: str
    role: Role = Role.user
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"