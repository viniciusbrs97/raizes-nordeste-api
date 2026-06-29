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

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "unidade_id": 1,
                "canal_pedido": "totem",
                "itens": [
                    {"produto_id": 1, "quantidade": 2},
                    {"produto_id": 3, "quantidade": 1},
                ],
            }
        }
    )


class StatusUpdate(BaseModel):
    status: StatusPedido

    model_config = ConfigDict(json_schema_extra={"example": {"status": "em_preparo"}})


class ItemPedidoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    produto_id: int
    quantidade: int
    preco_unitario: Decimal


class PedidoRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "cliente_id": 2,
                "unidade_id": 1,
                "canal_pedido": "totem",
                "status": "pendente",
                "valor_total": "28.00",
                "itens": [
                    {"produto_id": 1, "quantidade": 2, "preco_unitario": "8.00"},
                    {"produto_id": 3, "quantidade": 1, "preco_unitario": "12.00"},
                ],
                "created_at": "2026-06-29T01:35:13Z",
            }
        },
    )

    id: int
    cliente_id: int
    unidade_id: int
    canal_pedido: CanalPedido
    status: StatusPedido
    valor_total: Decimal
    itens: list[ItemPedidoRead]
    created_at: datetime
