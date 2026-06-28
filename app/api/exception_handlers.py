from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.domain.exceptions import DomainError
from app.infrastructure.payment import GatewayIndisponivel


def registrar_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def _domain_error(request: Request, exc: DomainError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.error_code, "message": exc.detail},
        )

    @app.exception_handler(GatewayIndisponivel)
    async def _gateway_indisponivel(
        request: Request, exc: GatewayIndisponivel
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content={
                "error": "gateway-indisponivel",
                "message": "Gateway de pagamento indisponível, tente novamente",
            },
        )
