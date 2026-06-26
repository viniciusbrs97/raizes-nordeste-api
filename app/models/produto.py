from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, TimestampMixin

if TYPE_CHECKING:
    from app.models.item_pedido import ItemPedido
    from app.models.produto_unidade import ProdutoUnidade


class Produto(TimestampMixin, BaseModel):
    __tablename__ = "produto"

    nome: Mapped[str] = mapped_column(String(255))
    descricao: Mapped[str | None] = mapped_column(Text)
    preco_base: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    categoria: Mapped[str | None] = mapped_column(String(100))

    produtos_unidade: Mapped[list["ProdutoUnidade"]] = relationship(
        back_populates="produto"
    )
    itens_pedido: Mapped[list["ItemPedido"]] = relationship(back_populates="produto")
