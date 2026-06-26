from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums import PerfilUsuario
from app.models.base import BaseModel, TimestampMixin
from app.models.enum_column import enum_column

if TYPE_CHECKING:
    from app.models.audit_log import AuditLog
    from app.models.movimentacao_pontos import MovimentacaoPontos
    from app.models.pedido import Pedido
    from app.models.unidade import Unidade


class Usuario(TimestampMixin, BaseModel):
    __tablename__ = "usuario"

    nome: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    senha_hash: Mapped[str] = mapped_column(String(255))
    perfil: Mapped[PerfilUsuario] = mapped_column(enum_column(PerfilUsuario))
    unidade_id: Mapped[int | None] = mapped_column(ForeignKey("unidade.id"))
    consentimento_lgpd: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=text("false")
    )
    consentimento_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    ativo: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=text("true")
    )

    unidade: Mapped["Unidade | None"] = relationship(back_populates="usuarios")
    pedidos: Mapped[list["Pedido"]] = relationship(back_populates="cliente")
    movimentacoes_pontos: Mapped[list["MovimentacaoPontos"]] = relationship(
        back_populates="usuario"
    )
    audit_logs: Mapped[list["AuditLog"]] = relationship(back_populates="usuario")
