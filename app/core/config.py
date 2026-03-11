import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "FastAPI User Service")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    SECRET_KEY: str = os.getenv("SECRET_KEY", "change_me")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
    )

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")


settings = Settings()