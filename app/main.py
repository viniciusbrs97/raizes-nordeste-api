from fastapi import FastAPI

from app.api import auth, cardapio, estoque, health, pedidos
from app.api.exception_handlers import registrar_exception_handlers
from app.api.middleware import registrar_middlewares

TAGS_METADATA = [
    {"name": "auth", "description": "Autenticação por JWT e identificação do usuário logado."},
    {"name": "cardapio", "description": "Cardápio segmentado por unidade, exibindo só os produtos disponíveis."},
    {"name": "pedidos", "description": "Ciclo de vida do pedido: criação, consulta, pagamento e transição de status."},
    {"name": "estoque", "description": "Movimentação manual de estoque por unidade, auditada."},
    {"name": "health", "description": "Verificação de disponibilidade da API."},
]

DESCRICAO = """
API da rede de lanchonetes **Raízes do Nordeste**.

**Autenticação:** faça login em `POST /auth/login` e use o `access_token` retornado
no header `Authorization: Bearer <token>` nas demais rotas.

**Padrão de erro:** toda resposta de erro segue o mesmo envelope —
`{ error, message, details, timestamp, path, requestId }` — e inclui o header
`X-Request-ID` para rastreabilidade.
"""

app = FastAPI(
    title="Raízes do Nordeste API",
    description=DESCRICAO,
    version="0.1.0",
    openapi_tags=TAGS_METADATA,
)

registrar_middlewares(app)
registrar_exception_handlers(app)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(pedidos.router)
app.include_router(cardapio.router)
app.include_router(estoque.router)
