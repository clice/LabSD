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

import os
import sqlite3
from config import DB_NAME


DB_PATH = os.getenv("CINEMA_DB", DB_NAME)


# ======================================================
# Conexão com o banco
# ======================================================

def connect(db_path=DB_PATH):
	"""
    Cria conexão com SQLite e ativa suporte a
    chaves estrangeiras (Foreign Keys).
    """

	conn = sqlite3.connect(
        db_path,
		check_same_thread=False  # Importante para ThreadedServer
    )
	conn.execute("PRAGMA foreign_keys = ON")  # Habilitar chaves estrangeiras
	return conn


# ======================================================
# Inicialização do Banco
# ======================================================

def start_db():
	"""
	Criar todas as tabelas do sistema,
	caso não tenham sido criadas
	"""

	with connect() as conn:
		cursor = conn.cursor()
		create_tables(cursor)
		insert_initial_data(cursor)


# ======================================================
# Criar Tabelas dos Bancos de Dados
# ======================================================

def create_tables(cursor):

	# ---------- CREATE TABLE MOVIES ----------
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS movies (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			title TEXT NOT NULL,
			genre TEXT,
			length INTEGER
		)
	""")

	# ---------- CREATE TABLE SCREENINGS ----------
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS screenings (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			movie_id INTEGER NOT NULL,
			time TEXT,
			total_tickets INTEGER NOT NULL,
			available_tickets INTEGER NOT NULL,
			FOREIGN KEY(movie_id) REFERENCES movies(id) ON DELETE CASCADE
		)   			
	""")

	# ---------- CREATE TABLE CLIENTS ----------
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS clients (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT NOT NULL,
			email TEXT UNIQUE NOT NULL
			)   			
	""")

	# ---------- CREATE TABLE PURCHASES ----------
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS purchases (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			client_id INTEGER NOT NULL,
			screening_id INTEGER NOT NULL,
			quantity INTEGER NOT NULL,
			timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
			FOREIGN KEY(client_id) REFERENCES clients(id) ON DELETE CASCADE,
			FOREIGN KEY(screening_id) REFERENCES screenings(id) ON DELETE CASCADE
			)   			
	""")


# ======================================================
# Inserir Dados Iniciais
# ======================================================

def insert_initial_data(cursor):
    """
    Inserir dados iniciais no banco de dados
    apenas se as tabelas estiverem vazias, para evitar duplicações.
    """
    
    # ---------- INSERT INTO TABLE MOVIES ----------
    cursor.execute("SELECT COUNT(*) FROM movies")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO movies (title, genre, length) 
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
    
    # ---------- INSERT INTO TABLE SCREENINGS ----------
    cursor.execute("SELECT COUNT(*) FROM screenings")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO screenings (movie_id, time, total_tickets, available_tickets)
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

def list_movies():
    """
    Listar todos os filmes disponíveis no banco de dados.
    """
    
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, title, genre, length 
            FROM movies
            ORDER BY id
        """)
        return cursor.fetchall()
    

def list_screenings_by_movie(movie_id):
    """
    Listar todas as sessões disponíveis para um filme específico.
    """
    
    with connect() as conn:    
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, time, total_tickets, available_tickets 
            FROM screenings 
            WHERE movie_id = ?
            ORDER BY time
        """, (movie_id,))
        return cursor.fetchall()
    

def find_client(name, email, cursor):
	"""
	Buscar um cliente pelo email ou criar um novo cliente se não existir.
	"""

	cursor.execute("SELECT id FROM clients WHERE email=?", (email,))
	result = cursor.fetchone()

	if result:
		return result[0]

	cursor.execute("INSERT INTO clients (name, email) VALUES (?, ?)", (name, email))

	return cursor.lastrowid


# ======================================================
# Compra de Ingressos
# ======================================================

def buy_tickets(name, email, screening_id, quantity):
	"""
	Realizar a compra de ingressos para uma sessão específica, 
    garantindo que haja ingressos disponíveis e atualizando o estoque.
	"""

	with connect() as conn:
		cursor = conn.cursor()

		cursor.execute("""
			SELECT available_tickets
			FROM screenings
			WHERE id=?
		""", (screening_id,))

		# Verificar se a sessão existe e obter a quantidade de ingressos disponíveis
		result = cursor.fetchone()

		if not result:
			return {
				"status": "error",
				"message": "Sessão não encontrada.",
				"data": None
			}

		# Verificar se há ingressos suficientes disponíveis
		current = result[0]

		if current < quantity:
			return {
				"status": "error",
				"message": "Quantidade de ingressos insuficiente.",
				"data": None
			}

		# Buscar ou criar cliente
		client_id = find_client(name, email, cursor)

		total = current - quantity

		cursor.execute("""
			UPDATE screenings
			SET available_tickets=?
			WHERE id=?
		""", (total, screening_id))

		cursor.execute("""
			INSERT INTO purchases (client_id, screening_id, quantity)
			VALUES (?, ?, ?)
		""", (client_id, screening_id, quantity))

		# Commit automático ao sair do bloco with
		return {
			"status": "success",
			"message": "Compra realizada com sucesso.",
			"data": {"available_tickets": total}
		}


# ======================================================
# Consulta de Compras por Cliente
# ======================================================

def get_purchases_by_email(email):
    """
    Retorna todas as compras realizadas por um cliente,
    identificado pelo seu e-mail.

    Esta função realiza um JOIN entre:
    - purchases (compras)
    - screenings (sessões)
    - movies (filmes)

    Retorna:
        Lista contendo:
        - Título do filme
        - Horário da sessão
        - Quantidade comprada
        - Timestamp da compra

    Caso o cliente não exista ou não possua compras,
    retorna lista vazia.
    """

    with connect() as conn:        
        cursor = conn.cursor()
        
        # Primeiro localizar o client epelo e-mail
        cursor.execute("SELECT iD FROM clients WHERE email=?", (email,))        
        client = cursor.fetchone()
        
        # Se cliente não existir, não há compraa
        if not client:
            return []
        
        client_id = client[0]
        
        # Consulta com JOIN para trazer informações completas
        cursor.execute("""
            SELECT
				m.title,
				s.time,
				p.quantity,
				p.timestamp
			FROM purchases p
			JOIN screenings s ON p.screening_id = s.id
			JOIN movies m ON s.movie_id = m.id
			WHERE p.client_id = ?
			ORDER BY p.timestamp DESC
        """, (client_id,))
        
        return cursor.fetchall()