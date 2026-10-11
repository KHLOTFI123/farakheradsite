from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_WEAK_SECRETS = {
    "",
    "change-this-to-a-long-random-secret",
    "secret",
    "changeme",
}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./data/farakherad.db"
    secret_key: str = "change-this-to-a-long-random-secret"
    admin_username: str = "admin"
    admin_password: str = "admin123"
    reset_admin_password: bool = False
    access_token_expire_minutes: int = 480
    upload_dir: Path = Path("/app/uploads")
    static_dir: Path = Path("/app/static")
    algorithm: str = "HS256"
    site_url: str = "https://farakheradgroup.ir"
    environment: str = "development"
    cors_origins: str = ""
    max_upload_bytes: int = 5 * 1024 * 1024
    login_rate_limit: int = 10
    contact_rate_limit: int = 8

    @field_validator("environment")
    @classmethod
    def normalize_environment(cls, value: str) -> str:
        return (value or "development").strip().lower()

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    def allowed_cors_origins(self) -> list[str]:
        if self.cors_origins.strip():
            return [item.strip() for item in self.cors_origins.split(",") if item.strip()]
        origins = {
            self.site_url.rstrip("/"),
            "http://127.0.0.1:3000",
            "http://localhost:3000",
            "http://127.0.0.1:5173",
            "http://localhost:5173",
            "http://127.0.0.1:8000",
            "http://localhost:8000",
        }
        return sorted(origins)

    def validate_runtime(self) -> None:
        if not self.is_production:
            return
        if self.secret_key in _WEAK_SECRETS or len(self.secret_key) < 32:
            raise RuntimeError(
                "In production, SECRET_KEY must be a strong random value of at least 32 characters."
            )
        if self.admin_password in {"admin123", "admin", "password", "123456"}:
            raise RuntimeError(
                "In production, ADMIN_PASSWORD must not be a default or trivial password."
            )


settings = Settings()
settings.validate_runtime()

if not settings.upload_dir.exists():
    local_uploads = Path(__file__).resolve().parent.parent / "uploads"
    settings.upload_dir = local_uploads
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
