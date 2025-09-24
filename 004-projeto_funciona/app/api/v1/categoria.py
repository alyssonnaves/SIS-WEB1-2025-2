# app/api/v1/produto.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.schemas.categoria import CategoriaCreate, CategoriaOut
from app.repositories import categoria as repo

router = APIRouter(prefix="/categoria", tags=["categoria"])

@router.post("/", response_model=CategoriaOut, status_code=status.HTTP_201_CREATED)
def create(payload: CategoriaCreate, db: Session = Depends(get_db)):
    return repo.create(db, payload)

@router.get("/", response_model=list[CategoriaOut])
def list_all(db: Session = Depends(get_db)):
    return repo.list_(db)

@router.get("/{produto_id}", response_model=CategoriaOut)
def get_one(produto_id: int, db: Session = Depends(get_db)):
    obj = repo.get(db, produto_id)
    if not obj: raise HTTPException(404, "Produto não encontrado")
    return obj

