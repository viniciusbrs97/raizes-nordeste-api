from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.api.schemas.pedido import PedidoCreate, PedidoRead
from app.application.use_cases.criar_pedido import criar_pedido
from app.application.use_cases.pagar_pedido import pagar_pedido
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


@router.post("/{pedido_id}/pagamento", response_model=PedidoRead)
async def pagar(
    pedido_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Pedido:
    return await pagar_pedido(db, pedido_id)
