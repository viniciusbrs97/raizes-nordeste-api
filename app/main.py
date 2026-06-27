from fastapi import FastAPI

from app.api import auth, health, pedidos

app = FastAPI(title="Raízes do Nordeste API")

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(pedidos.router)
