from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App Config
    APP_NAME: str = "OpsConnect"
    ENV: str = "dev"  # dev, prod, test
    
    # Database (Postgres)
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5432/opsconnect"
    
    # Cache (Redis)
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Observability
    OTEL_SERVICE_NAME: str = "opsconnect-service"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Singleton instance
settings = Settings()