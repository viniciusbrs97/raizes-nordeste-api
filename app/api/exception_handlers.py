from datetime import datetime, timezone
from uuid import uuid4

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.middleware import REQUEST_ID_HEADER
from app.domain.exceptions import DomainError
from app.infrastructure.payment import GatewayIndisponivel

_ERRO_POR_STATUS = {
    status.HTTP_401_UNAUTHORIZED: "nao-autenticado",
    status.HTTP_403_FORBIDDEN: "acesso-negado",
    status.HTTP_404_NOT_FOUND: "recurso-nao-encontrado",
    status.HTTP_405_METHOD_NOT_ALLOWED: "metodo-nao-permitido",
}


def _request_id(request: Request) -> str:
    return getattr(request.state, "request_id", None) or str(uuid4())


def _agora_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _envelope_erro(
    request: Request,
    status_code: int,
    error: str,
    message: str,
    details: list[dict[str, str]] | None = None,
    headers: dict[str, str] | None = None,
) -> JSONResponse:
    request_id = _request_id(request)
    corpo = {
        "error": error,
        "message": message,
        "details": details or [],
        "timestamp": _agora_utc(),
        "path": request.url.path,
        "requestId": request_id,
    }
    cabecalhos = {REQUEST_ID_HEADER: request_id, **(headers or {})}
    return JSONResponse(status_code=status_code, content=corpo, headers=cabecalhos)


def _detalhes_validacao(exc: RequestValidationError) -> list[dict[str, str]]:
    detalhes: list[dict[str, str]] = []
    for erro in exc.errors():
        local = [str(parte) for parte in erro["loc"] if parte != "body"]
        detalhes.append({"field": ".".join(local) or "body", "issue": erro["msg"]})
    return detalhes


def registrar_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def _domain_error(request: Request, exc: DomainError) -> JSONResponse:
        return _envelope_erro(request, exc.status_code, exc.error_code, exc.detail)

    @app.exception_handler(GatewayIndisponivel)
    async def _gateway_indisponivel(
        request: Request, exc: GatewayIndisponivel
    ) -> JSONResponse:
        return _envelope_erro(
            request,
            status.HTTP_502_BAD_GATEWAY,
            "gateway-indisponivel",
            "Gateway de pagamento indisponível, tente novamente",
        )

    @app.exception_handler(RequestValidationError)
    async def _validacao(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return _envelope_erro(
            request,
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            "erro-validacao",
            "Erro de validação nos dados enviados",
            details=_detalhes_validacao(exc),
        )

    @app.exception_handler(StarletteHTTPException)
    async def _http_error(
        request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        error = _ERRO_POR_STATUS.get(exc.status_code, "erro-http")
        message = exc.detail if isinstance(exc.detail, str) else "Erro na requisição"
        return _envelope_erro(
            request, exc.status_code, error, message, headers=exc.headers
        )

    @app.exception_handler(Exception)
    async def _erro_interno(request: Request, exc: Exception) -> JSONResponse:
        return _envelope_erro(
            request,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "erro-interno",
            "Erro interno do servidor",
        )
