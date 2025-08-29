from pydantic import BaseModel

class ProdutoCreate(BaseModel):
    nome: str
    preco: float