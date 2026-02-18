"""
database.py

Camada de Persistência do Sistema Distribuído

- Estrutura completa do banco
- Gerenciar filmes
- Gerenciar sessões
- Regisrtar clientes
- Registrar compraa
- Controlar estoque de ingressos por sessão
"""

import sqlite3

DB_NAME = "cinema.db"


def conectar():
    return sqlite3.connect(DB_NAME)


def inicializar_banco():
    """
    Cria todas as tabelas do sistema.
    """

    conn = conectar()
    cursor = conn.cursor()


    # Tabela de filmes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS filmes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            genero TEXT,
            duracao INTEGER
        )
    """)


    # Tabela de sessões
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filme_id INTEGER,
            horario TEXT,
            ingressos_disponiveis INTEGER,
            FOREIGN KEY(filme_id) REFERENCES filmes(id)
        )
    """)

    
    # Tabela de clientes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT
        )
    """)

    
    # Tabela de compras
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS compras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            sessao_id INTEGER,
            quantidade INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(cliente_id) REFERENCES clientes(id),
            FOREIGN KEY(sessao_id) REFERENCES sessoes(id)
        )
    """)


    # Inserir filmes exemplo se banco vazio
    cursor.execute("SELECT COUNT(*) FROM filmes")
    if cursor.fetchone()[0] == 0:

        cursor.execute("""
            INSERT INTO filmes (titulo, genero, duracao)
            VALUES
            ('Interestelar', 'Ficção Científica', 169),
            ('Oppenheimer', 'Drama', 180),
            ('Divertida Mente', 'Animação', 102)
        """)


    # Inserir sessões exemplo
    cursor.execute("SELECT COUNT(*) FROM sessoes")
    if cursor.fetchone()[0] == 0:

        cursor.execute("""
            INSERT INTO sessoes (filme_id, horario, ingressos_disponiveis)
            VALUES
            (1, '18:00', 20),
            (1, '21:00', 20),
            (2, '19:00', 15),
            (3, '17:00', 25)
        """)

    conn.commit()
    conn.close()
