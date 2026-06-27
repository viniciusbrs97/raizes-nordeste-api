from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import CanalPedido, StatusPedido


class ItemPedidoCreate(BaseModel):
    produto_id: int
    quantidade: int = Field(gt=0)


class PedidoCreate(BaseModel):
    unidade_id: int
    canal_pedido: CanalPedido
    itens: list[ItemPedidoCreate] = Field(min_length=1)


class StatusUpdate(BaseModel):
    status: StatusPedido


class ItemPedidoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    produto_id: int
    quantidade: int
    preco_unitario: Decimal


class PedidoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cliente_id: int
    unidade_id: int
    canal_pedido: CanalPedido
    status: StatusPedido
    valor_total: Decimal
    itens: list[ItemPedidoRead]
    created_at: datetime
