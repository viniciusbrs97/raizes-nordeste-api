from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.audit import registrar_auditoria
from app.domain.enums import TipoMovimentacaoEstoque
from app.domain.exceptions import EstoqueInsuficiente, RecursoNaoEncontrado
from app.models import ProdutoUnidade


async def movimentar_estoque(
    session: AsyncSession,
    unidade_id: int,
    produto_id: int,
    tipo: TipoMovimentacaoEstoque,
    quantidade: int,
    usuario_id: int,
) -> ProdutoUnidade:
    vinculo = await session.scalar(
        select(ProdutoUnidade).where(
            ProdutoUnidade.unidade_id == unidade_id,
            ProdutoUnidade.produto_id == produto_id,
        )
    )
    if vinculo is None:
        raise RecursoNaoEncontrado("Produto não encontrado nesta unidade")

    saida = tipo == TipoMovimentacaoEstoque.SAIDA
    if saida and vinculo.quantidade_estoque < quantidade:
        raise EstoqueInsuficiente(
            f"Estoque insuficiente para saída de {quantidade} unidade(s)"
        )

    vinculo.quantidade_estoque += -quantidade if saida else quantidade

    await registrar_auditoria(
        session,
        usuario_id,
        f"ESTOQUE_{tipo.name}",
        "produto_unidade",
        vinculo.id,
        detalhe=f"unidade={unidade_id} produto={produto_id} "
        f"qtd={quantidade} saldo={vinculo.quantidade_estoque}",
    )
    await session.commit()
    await session.refresh(vinculo)
    return vinculo
