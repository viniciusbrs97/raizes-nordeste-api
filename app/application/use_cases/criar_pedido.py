from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.schemas.pedido import PedidoCreate
from app.application.audit import registrar_auditoria
from app.domain.exceptions import (
    EstoqueInsuficiente,
    ProdutoIndisponivel,
    RecursoNaoEncontrado,
)
from app.models import ItemPedido, Pedido, ProdutoUnidade, Unidade


async def criar_pedido(
    session: AsyncSession, cliente_id: int, dados: PedidoCreate
) -> Pedido:
    unidade = await session.get(Unidade, dados.unidade_id)
    if unidade is None:
        raise RecursoNaoEncontrado("Unidade não encontrada")

    itens: list[ItemPedido] = []
    valor_total = Decimal("0")
    for item in dados.itens:
        vinculo = await session.scalar(
            select(ProdutoUnidade)
            .where(
                ProdutoUnidade.unidade_id == dados.unidade_id,
                ProdutoUnidade.produto_id == item.produto_id,
            )
            .options(selectinload(ProdutoUnidade.produto))
        )
        if vinculo is None:
            raise RecursoNaoEncontrado(
                f"Produto {item.produto_id} não encontrado nesta unidade"
            )
        if not vinculo.is_available:
            raise ProdutoIndisponivel(
                f"Produto {item.produto_id} indisponível nesta unidade"
            )
        if vinculo.quantidade_estoque < item.quantidade:
            raise EstoqueInsuficiente(
                f"Estoque insuficiente para o produto {item.produto_id}"
            )

        preco_unitario = vinculo.produto.preco_base
        vinculo.quantidade_estoque -= item.quantidade
        valor_total += preco_unitario * item.quantidade
        itens.append(
            ItemPedido(
                produto_id=item.produto_id,
                quantidade=item.quantidade,
                preco_unitario=preco_unitario,
            )
        )

    pedido = Pedido(
        cliente_id=cliente_id,
        unidade_id=dados.unidade_id,
        canal_pedido=dados.canal_pedido,
        valor_total=valor_total,
        itens=itens,
    )
    session.add(pedido)
    await session.flush()
    await registrar_auditoria(
        session,
        cliente_id,
        "PEDIDO_CRIADO",
        "pedido",
        pedido.id,
        detalhe=f"canal={dados.canal_pedido.value} valor_total={valor_total}",
    )
    await session.commit()
    await session.refresh(pedido, ["itens"])
    return pedido
