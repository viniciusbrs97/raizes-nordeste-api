from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.application.audit import registrar_auditoria
from app.application.estoque import restaurar_estoque
from app.domain.enums import StatusPagamento, StatusPedido
from app.domain.exceptions import PedidoNaoPendente, RecursoNaoEncontrado
from app.infrastructure.payment import solicitar_pagamento
from app.models import Pagamento, Pedido


async def pagar_pedido(session: AsyncSession, pedido_id: int, usuario_id: int) -> Pedido:
    pedido = await session.scalar(
        select(Pedido).where(Pedido.id == pedido_id).options(selectinload(Pedido.itens))
    )
    if pedido is None:
        raise RecursoNaoEncontrado("Pedido não encontrado")

    if pedido.status != StatusPedido.PENDENTE:
        raise PedidoNaoPendente("Pedido não está aguardando pagamento")

    # GatewayIndisponivel propaga para o exception handler (vira 502).
    resultado = await solicitar_pagamento(
        pedido.id, pedido.cliente_id, pedido.valor_total
    )

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
        acao = "PEDIDO_PAGO"
    else:
        pedido.status = StatusPedido.CANCELADO
        await restaurar_estoque(session, pedido)
        acao = "PEDIDO_RECUSADO"

    await registrar_auditoria(
        session,
        usuario_id,
        acao,
        "pedido",
        pedido.id,
        detalhe=f"resultado={resultado.status.value} ref={resultado.referencia_externa}",
    )
    await session.commit()
    await session.refresh(pedido, ["itens"])
    return pedido
