-- Criar tabela de Banca
CREATE TABLE banca (
    id_banca SERIAL PRIMARY KEY,
    nome_banca VARCHAR(255) NOT NULL
);

-- Criar tabela de Universidade
CREATE TABLE universidade (
    id_universidade SERIAL PRIMARY KEY,
    nome_universidade VARCHAR(255) NOT NULL,
    id_banca INT REFERENCES banca(id_banca) ON DELETE CASCADE
);

-- Criar tabela de Prova
CREATE TABLE prova (
    id_prova SERIAL PRIMARY KEY,
    ano INT NOT NULL,
    url_prova TEXT,
    url_gabarito TEXT,
    data_aplicacao DATE,
    id_universidade INT REFERENCES universidade(id_universidade) ON DELETE CASCADE
);

-- Criar tabela de Área
CREATE TABLE area (
    id_area SERIAL PRIMARY KEY,
    nome_area VARCHAR(255) NOT NULL
);

-- Criar tabela de Matéria
CREATE TABLE materia (
    id_materia SERIAL PRIMARY KEY,
    nome_materia VARCHAR(255) NOT NULL,
    id_area INT REFERENCES area(id_area) ON DELETE CASCADE
);

-- Criar tabela de SubMatéria
CREATE TABLE submateria (
    id_submateria SERIAL PRIMARY KEY,
    nome_submateria VARCHAR(255) NOT NULL,
    id_materia INT REFERENCES materia(id_materia) ON DELETE CASCADE
);

-- Criar tabela de Questão
CREATE TABLE questao (
    id_questao SERIAL PRIMARY KEY,
    numero INT NOT NULL,
    enunciado TEXT NOT NULL,
    alternativa_correta CHAR(1) NOT NULL,
    id_prova INT REFERENCES prova(id_prova) ON DELETE CASCADE,
    id_area INT REFERENCES area(id_area) ON DELETE CASCADE,
    id_materia INT REFERENCES materia(id_materia),
    id_submateria INT REFERENCES submateria(id_submateria)
);

-- Criar tabela de Alternativas
CREATE TABLE alternativa (
    id_alternativa SERIAL PRIMARY KEY,
    texto TEXT NOT NULL,
    letra CHAR(1) NOT NULL,
    id_questao INT REFERENCES questao(id_questao) ON DELETE CASCADE
);
