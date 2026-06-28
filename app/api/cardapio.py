from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.dependencies import get_current_user
from app.api.schemas.cardapio import ItemCardapioRead
from app.domain.exceptions import RecursoNaoEncontrado
from app.infrastructure.database import get_db
from app.models import ProdutoUnidade, Unidade, Usuario

router = APIRouter(prefix="/unidades", tags=["cardapio"])


@router.get("/{unidade_id}/cardapio", response_model=list[ItemCardapioRead])
async def listar_cardapio(
    unidade_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[ItemCardapioRead]:
    unidade = await db.get(Unidade, unidade_id)
    if unidade is None:
        raise RecursoNaoEncontrado("Unidade não encontrada")

    vinculos = (
        await db.scalars(
            select(ProdutoUnidade)
            .where(
                ProdutoUnidade.unidade_id == unidade_id,
                ProdutoUnidade.is_available.is_(True),
            )
            .options(selectinload(ProdutoUnidade.produto))
            .order_by(ProdutoUnidade.produto_id)
        )
    ).all()

    return [
        ItemCardapioRead(
            produto_id=vinculo.produto_id,
            nome=vinculo.produto.nome,
            descricao=vinculo.produto.descricao,
            categoria=vinculo.produto.categoria,
            preco=vinculo.produto.preco_base,
            quantidade_estoque=vinculo.quantidade_estoque,
        )
        for vinculo in vinculos
    ]
