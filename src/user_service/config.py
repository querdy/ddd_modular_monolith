from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    def get_db_string(self):
        return f"postgresql+asyncpg://{self.get('POSTGRES_USER', '')}:{self.get('POSTGRES_PASSWORD', '')}@{self.get('POSTGRES_HOST', '')}:{self.get('POSTGRES_PORT', '')}/{self.get('POSTGRES_DB', '')}"

    """Database"""
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DB_STRING: str = Field(default_factory=get_db_string)

    """JSON Web Tokens"""
    SECRET_KEY: str
    ALGORITHM: str
    # ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 30
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 30 * 24 * 30
    REFRESH_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 30

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
