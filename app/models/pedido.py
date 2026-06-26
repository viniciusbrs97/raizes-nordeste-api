from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums import CanalPedido, StatusPedido
from app.models.base import BaseModel, TimestampMixin
from app.models.enum_column import enum_column

if TYPE_CHECKING:
    from app.models.item_pedido import ItemPedido
    from app.models.pagamento import Pagamento
    from app.models.unidade import Unidade
    from app.models.usuario import Usuario


class Pedido(TimestampMixin, BaseModel):
    __tablename__ = "pedido"

    cliente_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"))
    unidade_id: Mapped[int] = mapped_column(ForeignKey("unidade.id"))
    canal_pedido: Mapped[CanalPedido] = mapped_column(enum_column(CanalPedido))
    status: Mapped[StatusPedido] = mapped_column(
        enum_column(StatusPedido),
        default=StatusPedido.PENDENTE,
        server_default=StatusPedido.PENDENTE.value,
    )
    valor_total: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), default=0, server_default=text("0")
    )

    cliente: Mapped["Usuario"] = relationship(back_populates="pedidos")
    unidade: Mapped["Unidade"] = relationship(back_populates="pedidos")
    itens: Mapped[list["ItemPedido"]] = relationship(
        back_populates="pedido", cascade="all, delete-orphan"
    )
    pagamento: Mapped["Pagamento | None"] = relationship(
        back_populates="pedido", uselist=False
    )
