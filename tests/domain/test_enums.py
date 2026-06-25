from enum import StrEnum

from app.domain.enums import (
    CanalPedido,
    PerfilUsuario,
    StatusPagamento,
    StatusPedido,
    TipoMovimentacaoPontos,
)

TODOS_OS_ENUMS = (
    PerfilUsuario,
    CanalPedido,
    StatusPedido,
    StatusPagamento,
    TipoMovimentacaoPontos,
)


def test_sao_string_enums():
    for enum_cls in TODOS_OS_ENUMS:
        assert issubclass(enum_cls, StrEnum)


def test_membro_se_comporta_como_string():
    assert StatusPedido.PENDENTE == "pendente"
    assert isinstance(StatusPedido.PENDENTE, str)


def test_perfil_usuario_valores():
    assert {p.value for p in PerfilUsuario} == {
        "super_admin",
        "admin",
        "gerente",
        "cozinha",
        "atendente",
        "cliente",
    }


def test_canal_pedido_valores():
    assert {c.value for c in CanalPedido} == {
        "app",
        "totem",
        "balcao",
        "pickup",
        "web",
    }


def test_status_pedido_valores():
    assert {s.value for s in StatusPedido} == {
        "pendente",
        "confirmado",
        "em_preparo",
        "pronto",
        "em_entrega",
        "entregue",
        "cancelado",
    }


def test_status_pagamento_valores():
    assert {s.value for s in StatusPagamento} == {
        "pendente",
        "processando",
        "aprovado",
        "recusado",
        "estornado",
        "cancelado",
    }


def test_tipo_movimentacao_pontos_valores():
    assert {t.value for t in TipoMovimentacaoPontos} == {
        "credito",
        "debito",
        "estorno",
        "expiracao",
    }
