from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.domain.enums import PerfilUsuario


class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    perfil: PerfilUsuario
    unidade_id: int | None = None
    consentimento_lgpd: bool = False


class UsuarioRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    email: EmailStr
    perfil: PerfilUsuario
    unidade_id: int | None
    ativo: bool
    created_at: datetime
