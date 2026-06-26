from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums import StatusPagamento
from app.models.base import BaseModel, TimestampMixin
from app.models.enum_column import enum_column

if TYPE_CHECKING:
    from app.models.pedido import Pedido


class Pagamento(TimestampMixin, BaseModel):
    __tablename__ = "pagamento"

    pedido_id: Mapped[int] = mapped_column(ForeignKey("pedido.id"), unique=True)
    status: Mapped[StatusPagamento] = mapped_column(
        enum_column(StatusPagamento),
        default=StatusPagamento.PENDENTE,
        server_default=StatusPagamento.PENDENTE.value,
    )
    valor: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    referencia_externa: Mapped[str | None] = mapped_column(String(255))
    processado_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    pedido: Mapped["Pedido"] = relationship(back_populates="pagamento")
