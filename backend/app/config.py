from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///data/consultora.db"
    jwt_secret: str = "change_me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440  # 24h
    hermes_api_key: str = "change_me"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
