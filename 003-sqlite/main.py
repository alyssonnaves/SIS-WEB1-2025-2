from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from models import ProdutoCreate
from schemas import Produto
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get ("/produtos")
def listar_produtos (db : Session = Depends(get_db)):
    return db.query(Produto).all()

@app.post("/produtos", status_code=201)
def criar(prod: ProdutoCreate, db: Session = Depends(get_db)):
    novo_prod = Produto(nome=prod.nome, preco=prod.preco)
    db.add(novo_prod)
    db.commit()
    db.refresh(novo_prod)
    return novo_prod