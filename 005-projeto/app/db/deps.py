
from typing import Generator
from sqlalchemy.engine import Connection
from app.db.session import engine

def get_connection() -> Generator[Connection, None, None]:
    with engine.begin() as conn:
        # abre conexao e inicia transacao
        yield conn

