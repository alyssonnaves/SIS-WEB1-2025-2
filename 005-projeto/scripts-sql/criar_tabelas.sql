CREATE TABLE categorias (
  id   SERIAL PRIMARY KEY,
  nome TEXT NOT NULL UNIQUE
);


CREATE TABLE produtos (
  id           SERIAL PRIMARY KEY,
  nome         TEXT NOT NULL,
  preco        NUMERIC(10,2) NOT NULL CHECK (preco > 0),
  categoria_id INTEGER NOT NULL REFERENCES categorias(id) ON DELETE RESTRICT
);

-- índices
CREATE INDEX idx_produtos_nome ON produtos (nome);
CREATE INDEX idx_produtos_categoria_id ON produtos (categoria_id);


bi


INSERT INTO categorias (nome) VALUES ('Eletrônicos'), ('Papelaria');

select * from categorias