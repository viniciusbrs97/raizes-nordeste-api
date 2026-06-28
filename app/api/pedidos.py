from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.dependencies import get_current_user, require_role
from app.api.schemas.pedido import PedidoCreate, PedidoRead, StatusUpdate
from app.application.use_cases.atualizar_status_pedido import atualizar_status_pedido
from app.application.use_cases.criar_pedido import criar_pedido
from app.application.use_cases.pagar_pedido import pagar_pedido
from app.domain.enums import CanalPedido, PerfilUsuario
from app.domain.exceptions import RecursoNaoEncontrado
from app.infrastructure.database import get_db
from app.models import Pedido, Usuario

router = APIRouter(prefix="/pedidos", tags=["pedidos"])


@router.post("", response_model=PedidoRead, status_code=status.HTTP_201_CREATED)
async def criar(
    dados: PedidoCreate,
    usuario: Usuario = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Pedido:
    return await criar_pedido(db, usuario.id, dados)


@router.get("", response_model=list[PedidoRead])
async def listar(
    canal_pedido: CanalPedido | None = Query(default=None, alias="canalPedido"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    usuario: Usuario = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[Pedido]:
    consulta = (
        select(Pedido).options(selectinload(Pedido.itens)).order_by(Pedido.id.desc())
    )
    if canal_pedido is not None:
        consulta = consulta.where(Pedido.canal_pedido == canal_pedido)
    return list((await db.scalars(consulta.offset(skip).limit(limit))).all())


@router.get("/{pedido_id}", response_model=PedidoRead)
async def obter(
    pedido_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Pedido:
    pedido = await db.scalar(
        select(Pedido).where(Pedido.id == pedido_id).options(selectinload(Pedido.itens))
    )
    if pedido is None:
        raise RecursoNaoEncontrado("Pedido não encontrado")
    return pedido


@router.patch("/{pedido_id}/status", response_model=PedidoRead)
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
    return await atualizar_status_pedido(db, pedido_id, dados.status, usuario.id)


@router.post("/{pedido_id}/pagamento", response_model=PedidoRead)
async def pagar(
    pedido_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Pedido:
    return await pagar_pedido(db, pedido_id, usuario.id)
