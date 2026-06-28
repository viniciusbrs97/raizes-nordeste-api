# Raízes do Nordeste API

API de pedidos de comida do Nordeste. Multicanal (totem, app, web, balcão, pickup), com autenticação JWT, controle de estoque, sistema de pagamento mockado, máquina de estados do pedido e log de auditoria.

## Stack

- Python 3.13 
- FastAPI 
- Uvicorn
- SQLAlchemy 2.0 (async)
- PostgreSQL
- Alembic (migrations) 
- Pydantic v2 / pydantic-settings
- PyJWT bcrypt

## Pré-requisitos

- [uv](https://docs.astral.sh/uv/) instalado
- PostgreSQL rodando localmente (porta 5432)

---

## Passo a passo

### 1. Dependências

Rode na pasta do projeto:
uv sync


### 2. Banco de dados

Crie o role e a database no PostgreSQL:

No seu terminal rode:
sudo su postgres
psql

Como super User postgres rode:

CREATE ROLE raizes_nordeste SUPERUSER LOGIN PASSWORD 'raizes_nordeste';
CREATE DATABASE raizes_nordeste;
ALTER DATABASE raizes_nordeste OWNER TO raizes_nordeste;


Saia do psql (`\q`) e do shell do postgres (`exit`).

### 3. Variáveis de ambiente

Na pasta raiz do projeto rode:
cp .env.example .env


O `.env` já vem apontando para o banco criado acima. Ajuste se necessário e gere um `SECRET_KEY` forte:
openssl rand -hex 32


Cole o valor em `SECRET_KEY` no `.env`. Defina também a senha do admin em `SUPER_ADMIN_PASSWORD`.

No .env gerado cole:

ENVIRONMENT=local
DEBUG=true
DATABASE_URL=postgresql+asyncpg://raizes_nordeste:raizes_nordeste@localhost:5432/raizes_nordeste
SECRET_KEY=<gerado-com-openssl>
SUPER_ADMIN_EMAIL=admin@raizes.com
SUPER_ADMIN_PASSWORD=<sua-senha>


### 4. Migrations

No terminal do projeto rode o comando abaixo para criar as tabelas utilizando o alembic:
uv run alembic upgrade head


Cria as 9 tabelas no banco.

### 5. Seed (dados iniciais)

Rode os comandos para gerar os dados iniciais no banco:
uv run python -m scripts.seed


Cria (idempotente — pode rodar várias vezes):
- super_admin (e-mail/senha do `.env`)
- cliente demo: `cliente@raizes.com` / `cliente123`
- 1 unidade + produtos com estoque, e imprime os `produto_id` no terminal

### 6. Rodar a API

Para rodar a api:
uv run uvicorn app.main:app --reload


- API: http://localhost:8000
- Swagger (docs interativos): http://localhost:8000/docs
- Healthcheck: http://localhost:8000/health

---

## Credenciais

| Perfil | E-mail | Senha |
|--------|--------|-------|
| Super admin | `SUPER_ADMIN_EMAIL` do `.env` (ex.: `admin@raizes.com`) | `SUPER_ADMIN_PASSWORD` do `.env` |
| Cliente demo | `cliente@raizes.com` | `cliente123` |

Login: `POST /auth/login` (form `username` + `password`) → retorna `access_token` (Bearer).

## Testando com Postman

1. Importe o arquivo `docs/postman/raizes-nordeste.postman_collection.json` no Postman.
2. Ajuste a variável `senha` da coleção com o seu `SUPER_ADMIN_PASSWORD`.
3. Rode o Login (salva o token sozinho) e use o Collection Runner para a suíte completa.

Sentinelas do pagamento mockado (peça quantidade 1):
- produto_id=5 (R$ 0,13) → pagamento recusado (pedido cancelado)
- produto_id=6 (R$ 0,99) → gateway fora (HTTP 502)
- demais produtos → aprovado (pedido `confirmado`)

## Estrutura do projeto


app/
├── api/            # routers (health, auth, pedidos), schemas, dependencies, exception handlers
├── application/    # use cases (criar/pagar/atualizar status), helpers (estoque, audit)
├── core/           # config (.env) e segurança (JWT, bcrypt, SecurityService)
├── domain/         # enums, exceptions de domínio, máquina de estados (transições)
├── infrastructure/ # engine/session async e mock de pagamento
├── models/         # models SQLAlchemy
└── main.py         # instancia o FastAPI e registra routers/handlers
migrations/         # Alembic
scripts/seed.py     # seed idempotente


## Comandos úteis

TODOS SÃO RODADOS NO TERMINAL:
uv run ruff check app/ scripts/      # lint
uv run ruff format app/ scripts/     # formatação
uv run alembic revision --autogenerate -m "descricao"   # nova migration
uv run alembic upgrade head          # aplicar migrations

