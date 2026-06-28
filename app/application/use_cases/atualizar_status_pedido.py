from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.application.audit import registrar_auditoria
from app.application.estoque import restaurar_estoque
from app.domain.enums import StatusPedido
from app.domain.exceptions import RecursoNaoEncontrado, TransicaoInvalida
from app.domain.transicoes import TRANSICOES
from app.models import Pedido


async def atualizar_status_pedido(
    session: AsyncSession, pedido_id: int, novo_status: StatusPedido, usuario_id: int
) -> Pedido:
    pedido = await session.scalar(
        select(Pedido).where(Pedido.id == pedido_id).options(selectinload(Pedido.itens))
    )
    if pedido is None:
        raise RecursoNaoEncontrado("Pedido não encontrado")

    if novo_status not in TRANSICOES.get(pedido.status, set()):
        raise TransicaoInvalida(
            f"Transição inválida: {pedido.status.value} -> {novo_status.value}"
        )

    status_antigo = pedido.status
    pedido.status = novo_status
    if novo_status == StatusPedido.CANCELADO:
        await restaurar_estoque(session, pedido)

    acao = (
        "PEDIDO_CANCELADO"
        if novo_status == StatusPedido.CANCELADO
        else "STATUS_ALTERADO"
    )
    await registrar_auditoria(
        session,
        usuario_id,
        acao,
        "pedido",
        pedido.id,
        detalhe=f"{status_antigo.value}->{novo_status.value}",
    )
    await session.commit()
    await session.refresh(pedido, ["itens"])
    return pedido
