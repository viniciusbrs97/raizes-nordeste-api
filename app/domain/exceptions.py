class DomainError(Exception):
    """Erro de regra de negócio. Cada subclasse define status_code e error_code."""

    status_code = 400
    error_code = "erro-dominio"

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)


class RecursoNaoEncontrado(DomainError):
    status_code = 404
    error_code = "recurso-nao-encontrado"


class ProdutoIndisponivel(DomainError):
    status_code = 409
    error_code = "produto-indisponivel"


class EstoqueInsuficiente(DomainError):
    status_code = 409
    error_code = "estoque-insuficiente"


class PedidoNaoPendente(DomainError):
    status_code = 409
    error_code = "pedido-nao-pendente"


class TransicaoInvalida(DomainError):
    status_code = 409
    error_code = "transicao-invalida"
