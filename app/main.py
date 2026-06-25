from fastapi import FastAPI

from app.api import health

app = FastAPI(title="Raízes do Nordeste API")

app.include_router(health.router)
