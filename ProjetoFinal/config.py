"""
config.py

Arquivo central de configuração do Sistema Distribuído do Cinema.
Centraliza portas, endereços, nomes de serviços, banco e outras configurações.
"""

import os


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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")

DB_NAME = os.path.join(DATA_DIR, "cinema.db")
TEST_DB_NAME = os.path.join(DATA_DIR, "cinema_test.db")


# ===============================
# Logging
# ===============================

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_LEVEL = "INFO"