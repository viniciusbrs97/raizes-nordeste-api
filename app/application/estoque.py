from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Pedido, ProdutoUnidade


async def restaurar_estoque(session: AsyncSession, pedido: Pedido) -> None:
    for item in pedido.itens:
        vinculo = await session.scalar(
            select(ProdutoUnidade).where(
                ProdutoUnidade.produto_id == item.produto_id,
                ProdutoUnidade.unidade_id == pedido.unidade_id,
            )
        )
        if vinculo is not None:
            vinculo.quantidade_estoque += item.quantidade
