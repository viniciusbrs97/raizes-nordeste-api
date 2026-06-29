from pydantic import BaseModel, ConfigDict


class DetalheErro(BaseModel):
    field: str
    issue: str


class ErroResponse(BaseModel):
    error: str
    message: str
    details: list[DetalheErro] = []
    timestamp: str
    path: str
    requestId: str | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "error": "recurso-nao-encontrado",
                "message": "Pedido não encontrado",
                "details": [],
                "timestamp": "2026-06-29T01:35:13Z",
                "path": "/pedidos/1",
                "requestId": "9d1a50f4-a332-4e37-aa41-afdfb26eca5e",
            }
        }
    )


_DESCRICOES_ERRO = {
    400: "Requisição inválida",
    401: "Não autenticado",
    403: "Permissão insuficiente",
    404: "Recurso não encontrado",
    409: "Conflito de regra de negócio",
    422: "Erro de validação",
    502: "Gateway de pagamento indisponível",
}


def respostas_erro(*codigos: int) -> dict:
    """Monta o dict de `responses` do FastAPI para os códigos de erro informados."""
    return {
        codigo: {"model": ErroResponse, "description": _DESCRICOES_ERRO[codigo]}
        for codigo in codigos
    }
