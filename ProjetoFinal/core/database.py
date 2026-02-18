"""
database.py

Camada de Persistência do Sistema Distribuído do Cinema

- Estrutura complete do banco
- Gerenciar filmes
- Gerenciar sessões
- Gerenciar clientes
- Gerenciar compras
- Controlar estoque de ingressos por sessão
"""


import sqlite3


DB_NAME = "cinema.db"


def conectar():
	"""
	Estabelecer conexão com o banco de dados SQLite
	"""

	return sqlite3.connect(DB_NAME)


def inicializar_banco():
	"""
	Criar todas as tabelas do sistema,
	caso não tenham sido criadas
	"""

	with conectar() as conn:
		cursor = conn.cursor()

		# CREATE