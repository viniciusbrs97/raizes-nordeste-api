import pytest
from pydantic import ValidationError

from app.core.config import Settings, get_settings

REQUIRED_ENV = {
    "DATABASE_URL": "postgresql+asyncpg://raizes:senha@localhost:5432/raizes_nordeste",
    "SECRET_KEY": "um-segredo-forte",
    "SUPER_ADMIN_EMAIL": "admin@raizes.com",
    "SUPER_ADMIN_USERNAME": "admin",
    "SUPER_ADMIN_PASSWORD": "troque-essa-senha",
}


def _set_required_env(monkeypatch):
    for name, value in REQUIRED_ENV.items():
        monkeypatch.setenv(name, value)


def _clear_required_env(monkeypatch):
    for name in REQUIRED_ENV:
        monkeypatch.delenv(name, raising=False)


def test_settings_loads_values_from_environment(monkeypatch):
    _set_required_env(monkeypatch)

    settings = Settings(_env_file=None)

    assert settings.secret_key == "um-segredo-forte"
    assert settings.super_admin_email == "admin@raizes.com"
    assert settings.super_admin_username == "admin"
    assert settings.database_url.scheme == "postgresql+asyncpg"


def test_settings_has_sensible_defaults_for_environment_and_debug(monkeypatch):
    _set_required_env(monkeypatch)

    settings = Settings(_env_file=None)

    assert settings.environment == "local"
    assert settings.debug is False


def test_missing_required_variable_raises_validation_error(monkeypatch):
    _clear_required_env(monkeypatch)

    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_get_settings_returns_cached_instance(monkeypatch):
    _set_required_env(monkeypatch)
    get_settings.cache_clear()

    first = get_settings()
    second = get_settings()

    assert first is second
