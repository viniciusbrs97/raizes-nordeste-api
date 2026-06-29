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
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "nome": "Cliente Demo",
                "email": "cliente@raizes.com",
                "perfil": "cliente",
                "unidade_id": None,
                "ativo": True,
                "created_at": "2026-06-29T01:35:13Z",
            }
        },
    )

    id: int
    nome: str
    email: EmailStr
    perfil: PerfilUsuario
    unidade_id: int | None
    ativo: bool
    created_at: datetime
