from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Finance Tracking System"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "supersecretkey-for-interview-purpose-only"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./finance.db"

settings = Settings()
