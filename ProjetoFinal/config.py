"""
config.py

Arquivo central de configuração do Sistema Distribuído do Cinema.
Centraliza portas, endereços, nomes de serviços, banco e outras configurações.
"""


# ===============================
# Servidor principal
# ===============================

SERVER_HOST = "localhost"
SERVER_PORT = 18861


# ===============================
# Name Server
# ===============================

NAME_SERVER_HOST = "localhost"
NAME_SERVER_PORT = 18862
SERVICE_NAME = "cinema_service"


# ===============================
# Banco de dados
# ===============================

DB_NAME = "cinema.db"


# ===============================
# Logging
# ===============================

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_LEVEL = "INFO"