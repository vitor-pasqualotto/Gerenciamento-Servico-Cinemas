-- Tabela: empresas_cinema
CREATE TABLE empresas_cinema (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cnpj VARCHAR(20) UNIQUE NOT NULL,
    contato VARCHAR(255)
);

-- Tabela: cinemas
CREATE TABLE cinemas (
    id SERIAL PRIMARY KEY,
    empresa_id INTEGER NOT NULL,
    nome VARCHAR(255) NOT NULL,
    endereco VARCHAR(255),
    CONSTRAINT fk_empresa
        FOREIGN KEY (empresa_id)
        REFERENCES empresas_cinema(id)
        ON DELETE CASCADE
);

-- Tabela: salas
CREATE TABLE salas (
    id SERIAL PRIMARY KEY,
    cinema_id INTEGER NOT NULL,
    nome VARCHAR(255) NOT NULL,
    CONSTRAINT fk_cinema
        FOREIGN KEY (cinema_id)
        REFERENCES cinemas(id)
        ON DELETE CASCADE
);

-- Tabela: usuarios
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    tipo_usuario VARCHAR(50) NOT NULL,
    empresa_id INTEGER,
    cinema_id INTEGER,
    CONSTRAINT fk_empresa_usuario
        FOREIGN KEY (empresa_id)
        REFERENCES empresas_cinema(id)
        ON DELETE SET NULL,
    CONSTRAINT fk_cinema_usuario
        FOREIGN KEY (cinema_id)
        REFERENCES cinemas(id)
        ON DELETE SET NULL
);

-- Tabela: servicos
CREATE TABLE servicos (
    id SERIAL PRIMARY KEY,
    encarregado_id INTEGER NOT NULL,
    sala_id INTEGER NOT NULL,
    tipo_servico VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL,
    observacoes TEXT,
    data TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_encarregado
        FOREIGN KEY (encarregado_id)
        REFERENCES usuarios(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_sala
        FOREIGN KEY (sala_id)
        REFERENCES salas(id)
        ON DELETE CASCADE
);

-- Tabela: fotos_servico
CREATE TABLE fotos_servico (
    id SERIAL PRIMARY KEY,
    servico_id INTEGER NOT NULL,
    url_foto VARCHAR(255) NOT NULL,
    CONSTRAINT fk_servico_foto
        FOREIGN KEY (servico_id)
        REFERENCES servicos(id)
        ON DELETE CASCADE
);

-- Tabela: historico_status
CREATE TABLE historico_status (
    id SERIAL PRIMARY KEY,
    servico_id INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL,
    status VARCHAR(50) NOT NULL,
    observacoes TEXT,
    data TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_servico_historico
        FOREIGN KEY (servico_id)
        REFERENCES servicos(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_usuario_historico
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE CASCADE
);
