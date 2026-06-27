from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.enums import StatusPagamento, StatusPedido
from app.infrastructure.payment import GatewayIndisponivel, solicitar_pagamento
from app.models import Pagamento, Pedido, ProdutoUnidade


async def pagar_pedido(session: AsyncSession, pedido_id: int) -> Pedido:
    pedido = await session.scalar(
        select(Pedido).where(Pedido.id == pedido_id).options(selectinload(Pedido.itens))
    )
    if pedido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado"
        )

    if pedido.status != StatusPedido.PENDENTE:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Pedido não está aguardando pagamento",
        )

    try:
        resultado = await solicitar_pagamento(
            pedido.id, pedido.cliente_id, pedido.valor_total
        )
    except GatewayIndisponivel as erro:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Gateway de pagamento indisponível, tente novamente",
        ) from erro

    session.add(
        Pagamento(
            pedido_id=pedido.id,
            status=resultado.status,
            valor=pedido.valor_total,
            referencia_externa=resultado.referencia_externa,
            processado_em=datetime.now(timezone.utc),
        )
    )

    if resultado.status == StatusPagamento.APROVADO:
        pedido.status = StatusPedido.CONFIRMADO
    else:
        pedido.status = StatusPedido.CANCELADO
        await _restaurar_estoque(session, pedido)

    await session.commit()
    await session.refresh(pedido, ["itens"])
    return pedido


async def _restaurar_estoque(session: AsyncSession, pedido: Pedido) -> None:
    for item in pedido.itens:
        vinculo = await session.scalar(
            select(ProdutoUnidade).where(
                ProdutoUnidade.produto_id == item.produto_id,
                ProdutoUnidade.unidade_id == pedido.unidade_id,
            )
        )
        if vinculo is not None:
            vinculo.quantidade_estoque += item.quantidade
