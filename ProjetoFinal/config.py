"""
config.py

Arquivo central de configuração do Sistema Distribuído do Cinema.
Centraliza portas, endereços, nomes de serviços, banco e outras configurações.
"""


# Configurações de rede do servidor principal
SERVER_HOST = "localhost"
SERVER_PORT = 18861


# Configurações do Name Server 
NAME_SERVER_HOST = "localhost"
NAME_SERVER_PORT = 18862
SERVICE_NAME = "cinema_service"


# Configurações do banco de dados
DB_NAME = "cinema.db"


# Configurações de logging
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_LEVEL = "INFO"