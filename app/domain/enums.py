from enum import StrEnum


class PerfilUsuario(StrEnum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    GERENTE = "gerente"
    COZINHA = "cozinha"
    ATENDENTE = "atendente"
    CLIENTE = "cliente"


class CanalPedido(StrEnum):
    APP = "app"
    TOTEM = "totem"
    BALCAO = "balcao"
    PICKUP = "pickup"
    WEB = "web"


class StatusPedido(StrEnum):
    PENDENTE = "pendente"
    CONFIRMADO = "confirmado"
    EM_PREPARO = "em_preparo"
    PRONTO = "pronto"
    EM_ENTREGA = "em_entrega"
    ENTREGUE = "entregue"
    CANCELADO = "cancelado"


class StatusPagamento(StrEnum):
    PENDENTE = "pendente"
    PROCESSANDO = "processando"
    APROVADO = "aprovado"
    RECUSADO = "recusado"
    ESTORNADO = "estornado"
    CANCELADO = "cancelado"


class TipoMovimentacaoPontos(StrEnum):
    CREDITO = "credito"
    DEBITO = "debito"
    ESTORNO = "estorno"
    EXPIRACAO = "expiracao"


class TipoMovimentacaoEstoque(StrEnum):
    ENTRADA = "entrada"
    SAIDA = "saida"
