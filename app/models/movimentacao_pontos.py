from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums import TipoMovimentacaoPontos
from app.models.base import BaseModel
from app.models.enum_column import enum_column

if TYPE_CHECKING:
    from app.models.pedido import Pedido
    from app.models.usuario import Usuario


class MovimentacaoPontos(BaseModel):
    __tablename__ = "movimentacao_pontos"

    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"))
    pedido_id: Mapped[int | None] = mapped_column(ForeignKey("pedido.id"))
    tipo: Mapped[TipoMovimentacaoPontos] = mapped_column(
        enum_column(TipoMovimentacaoPontos)
    )
    pontos: Mapped[int] = mapped_column(Integer)

    usuario: Mapped["Usuario"] = relationship(back_populates="movimentacoes_pontos")
    pedido: Mapped["Pedido | None"] = relationship()
