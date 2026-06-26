from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.config import get_settings


class TokenInvalido(Exception):
    """Token ausente, expirado ou com assinatura inválida (vira 401 nas dependencies)."""


def hash_senha(senha: str) -> str:
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()


def verificar_senha(senha: str, senha_hash: str) -> bool:
    return bcrypt.checkpw(senha.encode(), senha_hash.encode())


def criar_access_token(sub: str, perfil: str | None = None) -> str:
    settings = get_settings()
    expira_em = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload: dict[str, object] = {"sub": sub, "exp": expira_em}
    if perfil is not None:
        payload["perfil"] = perfil
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def decodificar_token(token: str) -> dict:
    settings = get_settings()
    try:
        return jwt.decode(
            token, settings.secret_key, algorithms=[settings.jwt_algorithm]
        )
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as erro:
        raise TokenInvalido("Token inválido ou expirado") from erro
