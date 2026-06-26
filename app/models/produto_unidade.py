from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, TimestampMixin

if TYPE_CHECKING:
    from app.models.produto import Produto
    from app.models.unidade import Unidade


class ProdutoUnidade(TimestampMixin, BaseModel):
    __tablename__ = "produto_unidade"
    __table_args__ = (
        UniqueConstraint("produto_id", "unidade_id", name="uq_produto_unidade"),
    )

    produto_id: Mapped[int] = mapped_column(ForeignKey("produto.id"))
    unidade_id: Mapped[int] = mapped_column(ForeignKey("unidade.id"))
    quantidade_estoque: Mapped[int] = mapped_column(
        Integer, default=0, server_default=text("0")
    )
    is_available: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=text("true")
    )

    produto: Mapped["Produto"] = relationship(back_populates="produtos_unidade")
    unidade: Mapped["Unidade"] = relationship(back_populates="produtos_unidade")
