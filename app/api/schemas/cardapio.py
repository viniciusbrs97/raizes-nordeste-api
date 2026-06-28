from decimal import Decimal

from pydantic import BaseModel


class ItemCardapioRead(BaseModel):
    produto_id: int
    nome: str
    descricao: str | None
    categoria: str | None
    preco: Decimal
    quantidade_estoque: int
