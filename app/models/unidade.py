from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, TimestampMixin

if TYPE_CHECKING:
    from app.models.pedido import Pedido
    from app.models.produto_unidade import ProdutoUnidade
    from app.models.usuario import Usuario


class Unidade(TimestampMixin, BaseModel):
    __tablename__ = "unidade"

    nome: Mapped[str] = mapped_column(String(255))
    regiao_cidade: Mapped[str | None] = mapped_column(String(255))
    endereco: Mapped[str | None] = mapped_column(String(255))
    ativa: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=text("true")
    )

    usuarios: Mapped[list["Usuario"]] = relationship(back_populates="unidade")
    produtos_unidade: Mapped[list["ProdutoUnidade"]] = relationship(
        back_populates="unidade"
    )
    pedidos: Mapped[list["Pedido"]] = relationship(back_populates="unidade")
