import asyncio
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.service import SecurityService
from app.domain.enums import PerfilUsuario
from app.infrastructure.database import async_session, engine
from app.models import Produto, ProdutoUnidade, Unidade, Usuario

NOME_UNIDADE = "Raízes - Recife Centro"
PRODUTOS = [
    ("Cuscuz", Decimal("8.00"), True),
    ("Tapioca", Decimal("10.00"), True),
    ("Bolo de macaxeira", Decimal("12.00"), True),
    ("Bode guisado", Decimal("35.00"), False),
]


async def seed_super_admin(session: AsyncSession) -> bool:
    settings = get_settings()
    ja_existe = await session.scalar(
        select(Usuario).where(Usuario.email == settings.super_admin_email)
    )
    if ja_existe is not None:
        return False

    session.add(
        Usuario(
            nome="Super Admin",
            email=settings.super_admin_email,
            senha_hash=SecurityService.hash_senha(settings.super_admin_password),
            perfil=PerfilUsuario.SUPER_ADMIN,
            ativo=True,
        )
    )
    await session.commit()
    return True


async def seed_dados_apoio(session: AsyncSession) -> None:
    unidade = await session.scalar(select(Unidade).where(Unidade.nome == NOME_UNIDADE))
    if unidade is None:
        unidade = Unidade(
            nome=NOME_UNIDADE,
            regiao_cidade="Recife - PE",
            endereco="Rua da Aurora, 100",
        )
        session.add(unidade)
        await session.flush()

    for nome, preco, disponivel in PRODUTOS:
        produto = await session.scalar(select(Produto).where(Produto.nome == nome))
        if produto is None:
            produto = Produto(nome=nome, preco_base=preco, categoria="Comida nordestina")
            session.add(produto)
            await session.flush()

        vinculo = await session.scalar(
            select(ProdutoUnidade).where(
                ProdutoUnidade.produto_id == produto.id,
                ProdutoUnidade.unidade_id == unidade.id,
            )
        )
        if vinculo is None:
            session.add(
                ProdutoUnidade(
                    produto_id=produto.id,
                    unidade_id=unidade.id,
                    quantidade_estoque=50,
                    is_available=disponivel,
                )
            )

    await session.commit()


async def _imprimir_ids(session: AsyncSession) -> None:
    unidade = await session.scalar(select(Unidade).where(Unidade.nome == NOME_UNIDADE))
    vinculos = (
        await session.scalars(
            select(ProdutoUnidade).where(ProdutoUnidade.unidade_id == unidade.id)
        )
    ).all()
    por_produto = {v.produto_id: v for v in vinculos}
    produtos = (await session.scalars(select(Produto).order_by(Produto.id))).all()

    print(f"\nunidade_id={unidade.id}  ({unidade.nome})")
    print("produtos (use nos itens do pedido):")
    for p in produtos:
        v = por_produto.get(p.id)
        estoque = v.quantidade_estoque if v else "-"
        marca = "" if (v and v.is_available) else "  [INDISPONIVEL]"
        print(f"  produto_id={p.id}  {p.nome}  R$ {p.preco_base}  estoque={estoque}{marca}")


async def _run() -> None:
    async with async_session() as session:
        criado = await seed_super_admin(session)
        await seed_dados_apoio(session)
        print("super_admin criado" if criado else "super_admin ja existe")
        print("dados de apoio: unidade + produtos + estoque (idempotente)")
        await _imprimir_ids(session)
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(_run())
