from app.domain.enums import StatusPedido

# Transições permitidas do pedido. Pagamento move PENDENTE -> CONFIRMADO/CANCELADO;
# o PATCH /status usa este mapa. Estados terminais têm conjunto vazio.
TRANSICOES: dict[StatusPedido, set[StatusPedido]] = {
    StatusPedido.PENDENTE: {StatusPedido.CANCELADO},
    StatusPedido.CONFIRMADO: {StatusPedido.EM_PREPARO, StatusPedido.CANCELADO},
    StatusPedido.EM_PREPARO: {StatusPedido.PRONTO, StatusPedido.CANCELADO},
    StatusPedido.PRONTO: {StatusPedido.EM_ENTREGA, StatusPedido.ENTREGUE},
    StatusPedido.EM_ENTREGA: {StatusPedido.ENTREGUE},
    StatusPedido.ENTREGUE: set(),
    StatusPedido.CANCELADO: set(),
}
