from pydantic_settings import BaseSettings


from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    app_name: str = "fastapi-user-service"
    database_url: str = "sqlite:///./app.db"
    jwt_secret: str = "change_me"
    jwt_alg: str = "HS256"
    access_token_expire_minutes: int = 120

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
