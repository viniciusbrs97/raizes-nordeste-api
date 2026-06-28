from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AuditLog


async def registrar_auditoria(
    session: AsyncSession,
    usuario_id: int | None,
    acao: str,
    entidade: str,
    entidade_id: int | None,
    detalhe: str | None = None,
) -> None:
    """Adiciona um registro de auditoria à sessão (sem commit — o use case commita)."""
    session.add(
        AuditLog(
            usuario_id=usuario_id,
            acao=acao,
            entidade=entidade,
            entidade_id=entidade_id,
            detalhe=detalhe,
        )
    )
