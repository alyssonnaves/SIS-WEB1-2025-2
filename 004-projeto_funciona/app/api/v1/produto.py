# app/api/v1/produto.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.schemas.produto import ProdutoCreate, ProdutoUpdate, ProdutoOut
from app.repositories import produto as repo
from app.services.produto import criar_produto
router = APIRouter(prefix="/produtos", tags=["produtos"])

@router.post("/", response_model=ProdutoOut, status_code=status.HTTP_201_CREATED)
def create(payload: ProdutoCreate, db: Session = Depends(get_db)):
    
    return criar_produto(db, payload)
    # return repo.create(db, payload)

@router.get("/", response_model=list[ProdutoOut])
def list_all(db: Session = Depends(get_db)):
    return repo.list_(db)

@router.get("/{produto_id}", response_model=ProdutoOut)
def get_one(produto_id: int, db: Session = Depends(get_db)):
    obj = repo.get(db, produto_id)
    if not obj: raise HTTPException(404, "Produto não encontrado")
    return obj

