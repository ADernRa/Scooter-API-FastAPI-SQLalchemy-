from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    PROJECT_NAME: str = "SCOOTER API"
    DEBUG: bool = False
    ADMIN_TOKEN: str = "super-secret-admin-token-123" 

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

settings = Settings()