"""
database.py

Camada de Persistência do Sistema Distribuído do Cinema

- Estrutura completa do banco
- Garantir integridade referencial (Foreign Keys)
- Gerenciar filmes, sessões, clientes e compras
- Controlar estoque de ingressos por sessão
- Executar operações transacionais

Arquitetura:
Esta é a Camada de Persistência na arquitetura N-Camadas.
Ela NÃO contém lógica de negócio distribuída (isso pertence ao server).
"""


import sqlite3
from config import DB_NAME


# ======================================================
# Conexão com o banco
# ======================================================

def conectar():
	"""
    Cria conexão com SQLite e ativa suporte a
    chaves estrangeiras (Foreign Keys).
    """

	conn = sqlite3.connect(DB_NAME)
	conn.execute("PRAGMA foreign_keys = ON")  # Habilitar chaves estrangeiras
	return conn


# ======================================================
# Inicialização do Banco
# ======================================================

def inicializar_banco():
	"""
	Criar todas as tabelas do sistema,
	caso não tenham sido criadas
	"""

	with conectar() as conn:
		cursor = conn.cursor()

		# ---------- CREATE TABLE FILMES ----------
		cursor.execute("""
            CREATE TABLE IF NOT EXISTS filmes (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				titulo TEXT NOT NULL,
				genero TEXT,
				duracao INTEGER
			)
        """)

		# ---------- CREATE TABLE SESSOES ----------
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS sessoes (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				filme_id INTEGER NOT NULL,
				horario TEXT,
				total_ingressos INTEGER NOT NULL,
				ingressos_disponiveis INTEGER NOT NULL,
				FOREIGN KEY(filme_id) REFERENCES filmes(id) ON DELETE CASCADE
			)   			
        """)

		# ---------- CREATE TABLE CLIENTES ----------
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS clientes (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				nome TEXT NOT NULL,
				email TEXT UNIQUE NOT NULL
				)   			
        """)

		# ---------- CREATE TABLE COMPRAS ----------
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS compras (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				cliente_id INTEGER NOT NULL,
				sessao_id INTEGER NOT NULL,
				quantidade INTEGER NOT NULL,
				timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
				FOREIGN KEY(cliente_id) REFERENCES clientes(id) ON DELETE CASCADE,
				FOREIGN KEY(sessao_id) REFERENCES sessoes(id) ON DELETE CASCADE
				)   			
        """)

		inserir_dados_iniciais(cursor)


def inserir_dados_iniciais(cursor):
    """
    Inserir dados iniciais no banco de dados
    apenas se as tabelas estiverem vazias, para evitar duplicações.
    """
    
    # ---------- INSERT INTO TABLE FILMES ----------
    cursor.execute("SELECT COUNT(*) FROM filmes")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO filmes (titulo, genero, duracao) 
            VALUES
            ('O Poderoso Chefão', 'Crime/Drama', 175),
			('A Origem', 'Sci-Fi/Thriller', 148),
			('Forrest Gump', 'Drama/Romance', 142),
			('Matrix', 'Sci-Fi/Ação', 136),
			('Gladiador', 'Ação/Drama', 155),
			('O Senhor dos Anéis: A Sociedade do Anel', 'Fantasia/Aventura', 178),
			('Pulp Fiction', 'Crime/Thriller', 154),
			('O Labirinto do Fauno', 'Fantasia/Drama', 118),
			('Clube da Luta', 'Drama/Thriller', 139),
			('A Viagem de Chihiro', 'Animação/Fantasia', 125),
			('Interestelar', 'Sci-Fi/Drama', 169),
            ('Oppenheimer', 'Drama/Histórico', 180),
            ('Divertida Mente', 'Animação/Drama', 102),
            ('Coringa', 'Drama/Thriller', 122),
			('Parasita', 'Thriller/Drama', 132),
			('1917', 'Guerra/Drama', 119),
			('A Bela e a Fera', 'Fantasia/Romance', 129),
			('O Rei Leão', 'Animação/Aventura', 118),
			('Vingadores: Ultimato', 'Ação/Fantasia', 181),
			('Toy Story', 'Animação/Aventura', 81)
        """)
    
    # ---------- INSERT INTO TABLE SESSOES ----------
    cursor.execute("SELECT COUNT(*) FROM sessoes")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO sessoes (filme_id, horario, total_ingressos, ingressos_disponiveis)
            VALUES
            (1, '2024-03-01 19:00', 100, 100),
			(2, '2024-03-01 21:00', 100, 100),		
			(3, '2024-03-02 18:00', 100, 100),
			(4, '2024-03-02 20:00', 100, 100),
			(5, '2024-03-03 19:00', 100, 100),
			(6, '2024-03-03 21:00', 100, 100),
			(7, '2024-03-04 18:00', 100, 100),
			(8, '2024-03-04 20:00', 100, 100),
			(9, '2024-03-05 19:00', 100, 100),
			(10, '2024-03-05 21:00', 100, 100),
			(11, '2024-03-06 18:00', 100, 100),
			(12, '2024-03-06 20:00', 100, 100),
			(13, '2024-03-07 19:00', 100, 100),
			(14, '2024-03-07 21:00', 100, 100),
			(15, '2024-03-08 18:00', 100, 100),
			(16, '2024-03-08 20:00', 100, 100),
			(17, '2024-03-09 19:00', 100, 100),
			(18, '2024-03-09 21:00', 100, 100),
			(19, '2024-03-10 18:00', 100, 100),
			(20, '2024-03-10 20:00', 100, 100)
        """)


# ======================================================
# Consultas ao banco
# ======================================================

def listar_filmes():
    """
    Listar todos os filmes disponíveis no banco de dados.
    """
    
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, titulo, genero, duracao FROM filmes")
        return cursor.fetchall()
    

def listar_sessoes_por_filme(filme_id):
    """
    Listar todas as sessões disponíveis para um filme específico.
    """
    
    with conectar() as conn:    
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, horario, total_ingressos, ingressos_disponiveis 
            FROM sessoes 
            WHERE filme_id = ?
        """, (filme_id,))
        return cursor.fetchall()
    

def buscar_ou_criar_cliente(nome, email):
	"""
	Buscar um cliente pelo email ou criar um novo cliente se não existir.
	"""

	with conectar() as conn:
		cursor = conn.cursor()

		cursor.execute("SELECT id FROM clientes WHERE email=?", (email,))
		resultado = cursor.fetchone()

		if resultado:
			return resultado[0]

		cursor.execute("INSERT INTO clientes (nome, email) VALUES (?, ?)", (nome, email))

		return cursor.lastrowid


# ======================================================
# Compra de Ingressos
# ======================================================

def comprar_ingresso(nome, email, sessao_id, quantidade):
	"""
	Realizar a compra de ingressos para uma sessão específica, 
    garantindo que haja ingressos disponíveis e atualizando o estoque.
	"""

	with conectar() as conn:
		cursor = conn.cursor()

		cursor.execute("""
			SELECT ingressos_disponiveis
			FROM sessoes
			WHERE id=?
		""", (sessao_id,))

		# Verificar se a sessão existe e obter a quantidade de ingressos disponíveis
		resultado = cursor.fetchone()

		if not resultado:
			return {
				"status": "error",
				"message": "Sessão não encontrada.",
				"data": None
			}

		# Verificar se há ingressos suficientes disponíveis
		atual = resultado[0]

		if atual < quantidade:
			return {
				"status": "error",
				"message": "Quantidade de ingressos insuficiente.",
				"data": None
			}

		# Buscar ou criar cliente
		cliente_id = buscar_ou_criar_cliente(nome, email)

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

		# Commit automático ao sair do bloco with
		return {
			"status": "success",
			"message": "Compra realizada com sucesso.",
			"data": {"restante": novo_total}
		}