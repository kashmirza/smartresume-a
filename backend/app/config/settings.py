import json
from typing import List, Union
from pydantic import field_validator

try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
    HAS_PYDANTIC_SETTINGS = True
except ImportError:
    HAS_PYDANTIC_SETTINGS = False
    try:
        from pydantic.v1 import BaseSettings  # type: ignore
    except ImportError:
        from pydantic import BaseSettings  # type: ignore


class Settings(BaseSettings):
    """
    Application configuration settings loaded from environment variables and .env file.
    """
    # Application & Environment
    ENVIRONMENT: str = "development"
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    # Database Settings
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "smart_resume_db"

    # Security & Authentication Settings
    JWT_SECRET_KEY: str = "smartresume_ai_super_secret_jwt_key_32_bytes_minimum_length_key"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440

    # CORS Settings
    CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    if HAS_PYDANTIC_SETTINGS:
        model_config = SettingsConfigDict(
            env_file=".env",
            env_file_encoding="utf-8",
            extra="ignore",
            case_sensitive=True,
        )

        @field_validator("CORS_ORIGINS", mode="before")
        @classmethod
        def parse_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
            if isinstance(v, str):
                v_trimmed = v.strip()
                if v_trimmed.startswith("[") and v_trimmed.endswith("]"):
                    try:
                        parsed = json.loads(v_trimmed)
                        if isinstance(parsed, list):
                            return [str(item).strip() for item in parsed]
                    except Exception:
                        pass
                return [item.strip() for item in v_trimmed.split(",") if item.strip()]
            return v
    else:
        class Config:
            env_file = ".env"
            env_file_encoding = "utf-8"
            extra = "ignore"
            case_sensitive = True

    def get_cors_origins_list(self) -> List[str]:
        """
        Returns CORS_ORIGINS as a clean list of strings regardless of input format.
        """
        if isinstance(self.CORS_ORIGINS, str):
            v_trimmed = self.CORS_ORIGINS.strip()
            if v_trimmed.startswith("[") and v_trimmed.endswith("]"):
                try:
                    parsed = json.loads(v_trimmed)
                    if isinstance(parsed, list):
                        return [str(item).strip() for item in parsed]
                except Exception:
                    pass
            return [origin.strip() for origin in v_trimmed.split(",") if origin.strip()]
        return [str(item) for item in self.CORS_ORIGINS]


# Global settings singleton instance
settings = Settings()
