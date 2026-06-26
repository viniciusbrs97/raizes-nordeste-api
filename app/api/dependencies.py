from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import TokenInvalido
from app.domain.enums import PerfilUsuario
from app.domain.service import SecurityService
from app.infrastructure.database import get_db
from app.models import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def _nao_autenticado() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não autenticado",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> Usuario:
    try:
        payload = SecurityService.decodificar_token(token)
    except TokenInvalido:
        raise _nao_autenticado() from None

    sub = payload.get("sub")
    if sub is None:
        raise _nao_autenticado()

    usuario = (
        await db.execute(select(Usuario).where(Usuario.id == int(sub)))
    ).scalar_one_or_none()
    if usuario is None or not usuario.ativo:
        raise _nao_autenticado()

    return usuario


def require_role(*perfis: PerfilUsuario):
    async def verificar(usuario: Usuario = Depends(get_current_user)) -> Usuario:
        if usuario.perfil not in perfis:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permissão insuficiente",
            )
        return usuario

    return verificar
