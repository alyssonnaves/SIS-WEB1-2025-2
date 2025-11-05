from fastapi import FastAPI
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
# from app.api.v1.rotas import api_rotas
from app.api.v2.rotaspg import api_rotas
from fastapi.middleware.cors import CORSMiddleware

# criar as tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)

# CORS — ajuste origin conforme seu front (ex.: http://127.0.0.1:8080)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # em produção, vc pode especificar o domínio do front
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_rotas)