from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.dependencies import get_current_user, require_role
from app.api.schemas.erro import respostas_erro
from app.api.schemas.pedido import PedidoCreate, PedidoRead, StatusUpdate
from app.application.use_cases.atualizar_status_pedido import atualizar_status_pedido
from app.application.use_cases.criar_pedido import criar_pedido
from app.application.use_cases.pagar_pedido import pagar_pedido
from app.domain.enums import CanalPedido, PerfilUsuario
from app.domain.exceptions import RecursoNaoEncontrado
from app.infrastructure.database import get_db
from app.models import Pedido, Usuario

router = APIRouter(prefix="/pedidos", tags=["pedidos"])


@router.post(
    "",
    response_model=PedidoRead,
    status_code=status.HTTP_201_CREATED,
    summary="Criar pedido",
    responses=respostas_erro(401, 404, 409, 422),
)
async def criar(
    dados: PedidoCreate,
    usuario: Usuario = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Pedido:
    """
    Cria um pedido com múltiplos itens, registra o **canal de origem** e calcula o
    **valor total** automaticamente. Valida disponibilidade e estoque de cada item:
    produto indisponível ou sem estoque retorna **409**; unidade/produto inexistente
    retorna **404**. O pedido nasce com status `pendente`.
    """
    return await criar_pedido(db, usuario.id, dados)


@router.get(
    "",
    response_model=list[PedidoRead],
    summary="Listar pedidos",
    responses=respostas_erro(401, 422),
)
async def listar(
    canal_pedido: CanalPedido | None = Query(default=None, alias="canalPedido"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    usuario: Usuario = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[Pedido]:
    """
    Lista os pedidos (mais recentes primeiro), com paginação (`skip`/`limit`) e filtro
    opcional por canal de origem (`canalPedido`).
    """
    consulta = (
        select(Pedido).options(selectinload(Pedido.itens)).order_by(Pedido.id.desc())
    )
    if canal_pedido is not None:
        consulta = consulta.where(Pedido.canal_pedido == canal_pedido)
    return list((await db.scalars(consulta.offset(skip).limit(limit))).all())


@router.get(
    "/{pedido_id}",
    response_model=PedidoRead,
    summary="Consultar pedido",
    responses=respostas_erro(401, 404, 422),
)
async def obter(
    pedido_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Pedido:
    """Retorna um pedido com seus itens, status e valor total. Inexistente retorna **404**."""
    pedido = await db.scalar(
        select(Pedido).where(Pedido.id == pedido_id).options(selectinload(Pedido.itens))
    )
    if pedido is None:
        raise RecursoNaoEncontrado("Pedido não encontrado")
    return pedido


@router.patch(
    "/{pedido_id}/status",
    response_model=PedidoRead,
    summary="Atualizar status do pedido",
    responses=respostas_erro(401, 403, 404, 409, 422),
)
async def atualizar_status(
    pedido_id: int,
    dados: StatusUpdate,
    usuario: Usuario = Depends(
        require_role(
            PerfilUsuario.SUPER_ADMIN,
            PerfilUsuario.ADMIN,
            PerfilUsuario.GERENTE,
            PerfilUsuario.COZINHA,
        )
    ),
    db: AsyncSession = Depends(get_db),
) -> Pedido:
    """
    Avança o status do pedido conforme a **máquina de estados**. Restrito aos perfis
    Cozinha, Gerente e Administrador (cliente recebe **403**). Transição inválida retorna
    **409**; ao cancelar, o estoque é restaurado.
    """
    return await atualizar_status_pedido(db, pedido_id, dados.status, usuario.id)


@router.post(
    "/{pedido_id}/pagamento",
    response_model=PedidoRead,
    summary="Pagar pedido",
    responses=respostas_erro(401, 404, 409, 422, 502),
)
async def pagar(
    pedido_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Pedido:
    """
    Solicita o pagamento ao gateway externo (mock), sem armazenar dados de cartão, e
    atualiza o pedido conforme o resultado: **aprovado → confirmado**;
    **recusado → cancelado** (estoque restaurado). Pedido não pendente retorna **409**;
    gateway indisponível retorna **502**.
    """
    return await pagar_pedido(db, pedido_id, usuario.id)
