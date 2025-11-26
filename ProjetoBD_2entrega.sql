DROP DATABASE IF EXISTS consuladodigital;
CREATE DATABASE IF NOT EXISTS consuladodigital;
USE consuladodigital;

-- TABELA: Passaporte
CREATE TABLE passaporte (
    id_passaporte INT AUTO_INCREMENT PRIMARY KEY,   
    numero_passaporte VARCHAR(20) NOT NULL UNIQUE,  
    data_emissao DATE NOT NULL,
    data_validade DATE NOT NULL,
    pais_emissor VARCHAR(50)
);

-- TABELA: Solicitante
CREATE TABLE solicitante (
    id_solicitante INT AUTO_INCREMENT PRIMARY KEY,    
    nome VARCHAR(100) NOT NULL,
    data_nascimento DATE NOT NULL,
    nacionalidade VARCHAR(50),
    endereco VARCHAR(150),
    contato VARCHAR(100),
    id_passaporte INT NOT NULL,                      
    FOREIGN KEY (id_passaporte) REFERENCES passaporte(id_passaporte)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- TABELA: Visto
CREATE TABLE visto (
    id_visto INT AUTO_INCREMENT PRIMARY KEY,          
    tipo_visto VARCHAR(50) NOT NULL,
    data_solicitacao DATE NOT NULL,
    status VARCHAR(20),
    id_solicitante INT NOT NULL,                      
    FOREIGN KEY (id_solicitante) REFERENCES solicitante(id_solicitante)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- TABELA: Entrevista
CREATE TABLE entrevista (
    id_entrevista INT AUTO_INCREMENT PRIMARY KEY,     
    data_hora DATETIME NOT NULL,
    local VARCHAR(100),
    observacoes TEXT,
    id_visto INT NOT NULL,                            
    FOREIGN KEY (id_visto) REFERENCES visto(id_visto)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- TABELA: Funcionário
CREATE TABLE funcionario (
    id_funcionario INT AUTO_INCREMENT PRIMARY KEY,    
    nome VARCHAR(100) NOT NULL,
    cargo VARCHAR(50),
    departamento VARCHAR(50),
    contato VARCHAR(100),
    Salario DECIMAL(10,2) DEFAULT 0.00
);

-- TABELA: Funcionário_Entrevista
CREATE TABLE funcionario_entrevista (
    id_funcionario INT NOT NULL,                      
    id_entrevista INT NOT NULL,                       
    PRIMARY KEY (id_funcionario, id_entrevista),      
    FOREIGN KEY (id_funcionario) REFERENCES funcionario(id_funcionario)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (id_entrevista) REFERENCES entrevista(id_entrevista)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Inserts de 3 instâncias por tabela
INSERT INTO passaporte (numero_passaporte, data_emissao, data_validade, pais_emissor)
VALUES
('BR1234567', '2020-05-10', '2030-05-10', 'Brasil'),
('US9876543', '2021-03-22', '2031-03-22', 'Estados Unidos'),
('PT1122334', '2019-11-15', '2029-11-15', 'Portugal');

INSERT INTO solicitante (nome, data_nascimento, nacionalidade, endereco, contato, id_passaporte)
VALUES
('João Pereira', '1990-04-15', 'Brasileiro', 'Rua do Inatel, 123 - Santa Rita do Sapucai', 'joao@email.com', 1),
('Maria Costa', '1985-09-30', 'Americana', 'Av. Central, 456 - Nova York', 'maria@email.com', 2),
('Rui Andrade', '1992-02-11', 'Português', 'Rua do Sol, 89 - Lisboa', 'rui@email.com', 3);

INSERT INTO visto (tipo_visto, data_solicitacao, status, id_solicitante)
VALUES
('Turismo', '2024-05-10', 'Aprovado', 1),
('Trabalho', '2024-06-18', 'Em Análise', 2),
('Estudante', '2024-07-25', 'Reprovado', 3);

INSERT INTO entrevista (data_hora, local, observacoes, id_visto)
VALUES
('2024-05-15 10:00:00', 'Consulado do Brasil em Lisboa', 'Candidato apresentou documentos completos.', 1),
('2024-06-20 14:30:00', 'Consulado dos EUA em São Paulo', 'Faltou um comprovante de residência.', 2),
('2024-07-30 09:00:00', 'Consulado de Portugal em Nova York', 'Entrevista tranquila, candidato inseguro.', 3);

INSERT INTO funcionario (nome, cargo, departamento, contato)
VALUES
('Ana Bezerra', 'Analista Consular', 'Vistos', 'ana.bezerra@consulado.gov'),
('Carlos Tavares', 'Entrevistador', 'Recursos Humanos', 'carlos.tavares@consulado.gov'),
('Fernanda Souza', 'Chefe de Setor', 'Administração', 'fernanda.souza@consulado.gov');

INSERT INTO funcionario_entrevista (id_funcionario, id_entrevista)
VALUES
(1, 1),
(2, 2),
(3, 3);

-- Deletes solicitados
DELETE FROM entrevista WHERE id_entrevista = 3;
DELETE FROM funcionário WHERE id_funcionario = 2;
-- Updates solicitados
UPDATE visto SET status = 'Aprovado' WHERE id_visto = 2;
DELETE FROM funcionário WHERE id_funcionario = 2;

-- Alter que adiciona uma nova coluna de salario na tabela de funcionario 
ALTER TABLE funcionário ADD COLUMN salario DECIMAL(10,2) DEFAULT 0.00 AFTER contato;
-- Drop que exclui a tabela de funcionario_entrevista
DROP TABLE funcionario_entrevista;

-- Função usando Function que gera o email institucional do funcionário
DELIMITER $$

CREATE FUNCTION criaEmailFuncionario(nome VARCHAR(100), departamento VARCHAR(50))
RETURNS VARCHAR(150)
DETERMINISTIC
BEGIN
    RETURN CONCAT(nome, '@', departamento, '.consulado.gov');
END $$

DELIMITER ;

-- Função usando Procedure que insere funcionários automaticamente usando a função acima
DELIMITER $$

CREATE PROCEDURE insereFuncionarioPadrao()
BEGIN
    INSERT INTO funcionario (nome, cargo, departamento, contato)
    VALUES
        ('Juliana Lima', 'Analista de Vistos', 'vistos', criaEmailFuncionario('Juliana.Lima', 'vistos')),
        ('Rafael Campos', 'Entrevistador', 'recursos', criaEmailFuncionario('Rafael.Campos', 'recursos')),
        ('Beatriz Gomes', 'Supervisora', 'administracao', criaEmailFuncionario('Beatriz.Gomes', 'administracao'));
END$$

DELIMITER ;

-- Função usando View que mostra apenas solicitantes com visto aprovado
CREATE VIEW view_vistos_aprovados AS
SELECT 
    s.nome AS solicitante,
    v.tipo_visto,
    v.status
FROM visto v
JOIN solicitante s ON v.id_solicitante = s.id_solicitante
WHERE v.status = 'Aprovado';

-- Criando um novo usuário chamado 'consulado_user' com senha segura e dando algumas permissões
CREATE USER 'consulado_user'@'localhost' IDENTIFIED BY 'SenhaForte123!';
GRANT SELECT, INSERT, UPDATE, DELETE
ON consuladodigital.*
TO 'consulado_user'@'localhost';
FLUSH PRIVILEGES;

