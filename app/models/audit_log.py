from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.usuario import Usuario


class AuditLog(BaseModel):
    __tablename__ = "audit_log"

    usuario_id: Mapped[int | None] = mapped_column(ForeignKey("usuario.id"))
    acao: Mapped[str] = mapped_column(String(255))
    entidade: Mapped[str] = mapped_column(String(255))
    entidade_id: Mapped[int | None] = mapped_column(BigInteger)
    detalhe: Mapped[str | None] = mapped_column(Text)

    usuario: Mapped["Usuario | None"] = relationship(back_populates="audit_logs")
