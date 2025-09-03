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

@app.get("/produtos/{prod_id}", response_model=dict)
def listar_id(prod_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == prod_id).first()
    if not produto:
        return {"erro": "produto nao encontrado"}
    return {
        "id": produto.id,
        "nome": produto.nome,
        "preco": produto.preco
    }

@app.post("/produtos", status_code=201)
def criar(prod: ProdutoCreate, db: Session = Depends(get_db)):
    novo_prod = Produto(nome=prod.nome, preco=prod.preco)
    db.add(novo_prod)
    db.commit()
    db.refresh(novo_prod)
    return novo_prod

@app.delete("/produtos/{prod_id}", status_code=200)
def excluir(prod_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == prod_id).first()
    if not produto:
        return {"erro": "produto nao encontrado"}
    db.delete(produto)
    db.commit()
    return {"mensagem": f"Produto com id {id} excluido"}

