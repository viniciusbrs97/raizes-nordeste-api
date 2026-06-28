from fastapi import FastAPI

from app.api import auth, cardapio, health, pedidos
from app.api.exception_handlers import registrar_exception_handlers

app = FastAPI(title="Raízes do Nordeste API")

registrar_exception_handlers(app)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(pedidos.router)
app.include_router(cardapio.router)
