from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "mongodb://localhost:27017/userdb"
    JWT_SECRET: str = "1632d7f866a478cb11124da545c44ceb"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRES_MIN: int = 60

    ADMIN_NAME: str = "Admin"
    ADMIN_EMAIL: str = "admin@gmail.com"
    ADMIN_PASSWORD: str = "Admin@123"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
