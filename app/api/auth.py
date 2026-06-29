from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.api.schemas.auth import TokenResponse
from app.api.schemas.erro import respostas_erro
from app.api.schemas.usuario import UsuarioRead
from app.core.service import SecurityService
from app.infrastructure.database import get_db
from app.models import Usuario

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Autenticar (login)",
    responses=respostas_erro(401, 422),
)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    """
    Autentica por e-mail e senha e devolve um token de acesso **JWT** (Bearer).

    Envie via formulário (`application/x-www-form-urlencoded`):
    - **username**: e-mail do usuário
    - **password**: senha

    Use o `access_token` no header `Authorization: Bearer <token>` das demais rotas.
    Credenciais inválidas ou usuário inativo retornam **401**.
    """
    usuario = (
        await db.execute(select(Usuario).where(Usuario.email == form.username))
    ).scalar_one_or_none()
    if usuario is None or not SecurityService.verificar_senha(
        form.password, usuario.senha_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not usuario.ativo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário inativo",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = SecurityService.criar_access_token(
        sub=str(usuario.id), perfil=usuario.perfil
    )
    return TokenResponse(access_token=token)


@router.get(
    "/me",
    response_model=UsuarioRead,
    summary="Usuário autenticado",
    responses=respostas_erro(401),
)
async def me(usuario: Usuario = Depends(get_current_user)) -> Usuario:
    """Retorna os dados do usuário dono do token informado (sem expor a senha)."""
    return usuario
