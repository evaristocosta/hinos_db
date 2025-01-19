CREATE TABLE IF NOT EXISTS hino (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  coletanea_id INTEGER,
  numero TEXT,
  nome TEXT NOT NULL,
  texto TEXT,
  texto_limpo TEXT,
  texto_estruturado TEXT,
  ano_composicao INTEGER,
  tom TEXT,
  FOREIGN KEY (coletanea_id) REFERENCES coletanea (id)
);

CREATE TABLE IF NOT EXISTS autor (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  nome TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS autor_acao (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  acao TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS hino_autor (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  hino_id INTEGER NOT NULL,
  autor_id INTEGER NOT NULL,
  autor_acao_id INTEGER NOT NULL,
  FOREIGN KEY (hino_id) REFERENCES hino (id),
  FOREIGN KEY (autor_id) REFERENCES autor (id),
  FOREIGN KEY (autor_acao_id) REFERENCES autor_acao (id)
);

CREATE TABLE IF NOT EXISTS hino_de (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  hino_id INTEGER NOT NULL,
  numero INTEGER,
  nome TEXT,
  nome_traduzido TEXT,
  texto TEXT,
  texto_limpo_traduzido TEXT,
  FOREIGN KEY (hino_id) REFERENCES hino (id)
);

CREATE TABLE IF NOT EXISTS coletanea (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  nome TEXT
);