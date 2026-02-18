"""
database.py

Camada de Persistência do Sistema Distribuído do Cinema

- Estrutura completa do banco
- Gerenciar filmes
- Gerenciar sessões
- Regisrtar clientes
- Registrar compra
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

    with conectar() as conn:
        cursor = conn.cursor()

        # Filmes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS filmes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                genero TEXT,
                duracao INTEGER
            )
        """)

        # Sessões
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filme_id INTEGER,
                horario TEXT,
                ingressos_disponiveis INTEGER,
                FOREIGN KEY(filme_id) REFERENCES filmes(id)
            )
        """)

        # Clientes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE
            )
        """)

        # Compras
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

        inserir_dados_iniciais(cursor)


def inserir_dados_iniciais(cursor):
    """
    inserir dados iniciais.
    """
    
    cursor.execute("SELECT COUNT(*) FROM filmes")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO filmes (titulo, genero, duracao)
            VALUES
            ('Interestelar', 'Ficção Científica', 169),
            ('Oppenheimer', 'Drama', 180),
            ('Divertida Mente', 'Animação', 102)
        """)

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


# CRUD FILMES

def listar_filmes():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM filmes")
        return cursor.fetchall()


def buscar_filme_por_id(filme_id):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM filmes WHERE id=?", (filme_id,))
        return cursor.fetchone()


def inserir_filme(titulo, genero, duracao):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO filmes (titulo, genero, duracao) VALUES (?, ?, ?)",
            (titulo, genero, duracao)
        )


# CRUD SESSÕES

def listar_sessoes_por_filme(filme_id):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, horario, ingressos_disponiveis
            FROM sessoes
            WHERE filme_id=?
        """, (filme_id,))
        return cursor.fetchall()


def atualizar_ingressos(sessao_id, nova_quantidade):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE sessoes
            SET ingressos_disponiveis=?
            WHERE id=?
        """, (nova_quantidade, sessao_id))


# CRUD CLIENTES

def buscar_ou_criar_cliente(cursor, nome, email):
    """
    Busca um cliente pelo email ou cria um novo se não existir.    
    """

    cursor.execute(
        "SELECT id FROM clientes WHERE email=?",
        (email,)
    )
    resultado = cursor.fetchone()

    if resultado:
        return resultado[0]

    cursor.execute(
        "INSERT INTO clientes (nome, email) VALUES (?, ?)",
        (nome, email)
    )

    return cursor.lastrowid

    
def consultar_ingressos():
    """
    Retorna a quantidade atual de ingressos disponíveis.
    """

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT quantidade FROM ingressos WHERE id=1")
    quantidade = cursor.fetchone()[0]

    conn.close()
    return quantidade


# TRANSAÇÃO DE COMPRA

def comprar_ingresso(nome, email, sessao_id, quantidade):

    with conectar() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT ingressos_disponiveis
            FROM sessoes
            WHERE id=?
        """, (sessao_id,))

        atual = cursor.fetchone()

        if not atual:
            return "Sessão não encontrada."

        atual = atual[0]

        if atual < quantidade:
            return "Ingressos insuficientes."

        cliente_id = buscar_ou_criar_cliente(cursor, nome, email)

        novo_total = atual - quantidade

        cursor.execute("""
            UPDATE sessoes
            SET ingressos_disponiveis=?
            WHERE id=?
        """, (novo_total, sessao_id))

        cursor.execute("""
            INSERT INTO compras (cliente_id, sessao_id, quantidade)
            VALUES (?, ?, ?)
        """, (cliente_id, sessao_id, quantidade))

        return f"Compra realizada. Restam {novo_total} ingressos."