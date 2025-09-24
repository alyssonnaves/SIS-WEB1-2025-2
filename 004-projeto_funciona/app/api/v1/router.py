# app/api/v1/router.py
from fastapi import APIRouter
from . import produto, categoria

api_router = APIRouter()
api_router.include_router(produto.router)
api_router.include_router(categoria.router)
