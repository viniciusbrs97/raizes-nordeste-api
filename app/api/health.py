from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter(tags=["health"])
settings = get_settings()


@router.get("/health", summary="Healthcheck")
async def health() -> dict[str, str]:
    """Verifica se a API está no ar e retorna o ambiente atual. Não requer autenticação."""
    return {"status": "ok", "environment": settings.environment}
