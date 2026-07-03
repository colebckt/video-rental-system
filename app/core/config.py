from functools import lru_cache
from os import getenv

from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self):
        self.service_name = getenv("SERVICE_NAME", "analytics-service")
        self.environment = getenv("ENVIRONMENT", "development")
        self.log_level = getenv("LOG_LEVEL", "INFO")
        self.cors_origins = getenv("CORS_ORIGINS", "*")
        self.cors_allow_credentials = getenv("CORS_ALLOW_CREDENTIALS", "false").lower() == "true"
        self.supabase_url = getenv("SUPABASE_URL")
        self.supabase_key = getenv("SUPABASE_KEY")

    @property
    def allowed_origins(self):
        if self.cors_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def allow_credentials(self):
        return self.cors_allow_credentials and self.allowed_origins != ["*"]

    def validate(self):
        missing = []
        if not self.supabase_url:
            missing.append("SUPABASE_URL")
        if not self.supabase_key:
            missing.append("SUPABASE_KEY")
        if missing:
            raise RuntimeError(f"Faltan variables de entorno obligatorias: {', '.join(missing)}")


@lru_cache
def get_settings():
    settings = Settings()
    settings.validate()
    return settings


settings = get_settings()
