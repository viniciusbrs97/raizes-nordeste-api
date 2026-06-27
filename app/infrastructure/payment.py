import asyncio
from dataclasses import dataclass
from decimal import Decimal
from uuid import uuid4

from app.domain.enums import StatusPagamento


class GatewayIndisponivel(Exception):
    """Gateway de pagamento fora do ar."""


@dataclass(frozen=True)
class ResultadoPagamento:
    status: StatusPagamento
    referencia_externa: str


async def solicitar_pagamento(
    pedido_id: int, cliente_id: int, valor: Decimal
) -> ResultadoPagamento:
    await asyncio.sleep(0)
    return ResultadoPagamento(
        status=_resposta_gateway(valor),
        referencia_externa=f"mock-{uuid4()}",
    )


def _resposta_gateway(valor: Decimal) -> StatusPagamento:
    centavos = int(valor * 100) % 100
    if centavos == 99:
        raise GatewayIndisponivel("Gateway de pagamento indisponível (simulado)")
    if valor <= 0 or centavos == 13:
        return StatusPagamento.RECUSADO
    return StatusPagamento.APROVADO
