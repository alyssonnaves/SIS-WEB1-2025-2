from sqlalchemy.orm import Session
from app.repositories import produto as repo
from app.schemas.produto import ProdutoCreate, ProdutoUpdate
from app.models.produto import Produto

def criar_produto(db: Session, payload: ProdutoCreate) -> Produto:
    # validações de negócio (ex.: preco > 0)
    if payload.preco <= 0:
        raise ValueError("Preço deve ser maior que zero.")
    return repo.create(db, payload)