from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import require_role
from app.api.schemas.erro import respostas_erro
from app.api.schemas.estoque import EstoqueRead, MovimentacaoEstoqueCreate
from app.application.use_cases.movimentar_estoque import movimentar_estoque
from app.domain.enums import PerfilUsuario
from app.infrastructure.database import get_db
from app.models import ProdutoUnidade, Usuario

router = APIRouter(prefix="/unidades", tags=["estoque"])


@router.post(
    "/{unidade_id}/produtos/{produto_id}/estoque",
    response_model=EstoqueRead,
    summary="Movimentar estoque",
    responses=respostas_erro(401, 403, 404, 409, 422),
)
async def movimentar(
    unidade_id: int,
    produto_id: int,
    dados: MovimentacaoEstoqueCreate,
    usuario: Usuario = Depends(
        require_role(
            PerfilUsuario.SUPER_ADMIN,
            PerfilUsuario.ADMIN,
            PerfilUsuario.GERENTE,
            PerfilUsuario.ATENDENTE,
        )
    ),
    db: AsyncSession = Depends(get_db),
) -> ProdutoUnidade:
    """
    Registra uma **entrada** ou **saída** de estoque de um produto na unidade.

    - `tipo`: `entrada` (soma) ou `saida` (subtrai)
    - `quantidade`: inteiro > 0

    Restrito aos perfis **Gerente, Atendente e Administrador** (cliente recebe **403**).
    Saída sem saldo retorna **409**; produto não vinculado à unidade retorna **404**.
    Cada movimentação é auditada (`ESTOQUE_ENTRADA` / `ESTOQUE_SAIDA`).
    """
    return await movimentar_estoque(
        db, unidade_id, produto_id, dados.tipo, dados.quantidade, usuario.id
    )
