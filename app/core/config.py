from functools import lru_cache
from typing import Literal

from pydantic import EmailStr, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações da aplicação, carregadas do ambiente ou do arquivo .env."""

    # Ambiente
    environment: Literal["local", "test"] = "local"
    debug: bool = False

    # Banco de dados
    database_url: PostgresDsn

    # Segurança
    secret_key: str

    # Super admin (credenciais-base)
    super_admin_email: EmailStr
    super_admin_username: str
    super_admin_password: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Retorna uma instância única (cacheada) das configurações."""
    return Settings()
