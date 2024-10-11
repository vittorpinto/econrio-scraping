-- Conectar ao banco de dados
\c vestibulares;

-- Inserindo uma banca
INSERT INTO banca (nome_banca) VALUES ('EconRio');

-- Inserindo uma universidade
INSERT INTO universidade (nome_universidade, id_banca) VALUES ('Universidade X', 1);

-- Inserindo uma área
INSERT INTO area (nome_area) VALUES ('Natureza');

-- Inserindo uma matéria
INSERT INTO materia (nome_materia, id_area) VALUES ('Biologia', 1);

-- Inserindo uma submatéria
INSERT INTO submateria (nome_submateria, id_materia) VALUES ('Vitaminas', 1);

-- Inserindo uma prova
INSERT INTO prova (ano, url_prova, url_gabarito, data_aplicacao, id_universidade) 
VALUES (2025, 'url_prova_2025', 'url_gabarito_2025', '2025-01-01', 1);

-- Inserindo uma questão
INSERT INTO questao (numero, enunciado, alternativa_correta, id_prova, id_area, id_materia, id_submateria) 
VALUES (1, 'Qual é a função das vitaminas?', 'A', 1, 1, 1, 1);

-- Inserindo alternativas
INSERT INTO alternativa (texto, letra, id_questao) VALUES ('Fornecer energia', 'A', 1);
INSERT INTO alternativa (texto, letra, id_questao) VALUES ('Auxiliar na digestão', 'B', 1);
