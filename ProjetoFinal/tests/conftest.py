"""
conftest.py

Arquivo especial do pytest das configurações iniciais.

Responsável por:
- Subir automaticamente o Name Server
- Subir automaticamente o Servidor RPC
- Garantir que as portas estejam abertas antes dos testes
- Derrubar os processos ao final da execução

O uso de fixture com scope="session" garante que o sistema
seja iniciado apenas uma vez para todos os testes.
"""

import subprocess
import sys
import time
import socket
import pytest
import os

from config import SERVER_PORT, NAME_SERVER_PORT, TEST_DB_NAME


def wait_for_port(port, timeout=10):
    """
    Aguarda até que uma porta TCP esteja aberta.

    Isso evita race condition entre inicialização
    do servidor e início dos testes.
    """
    
    start = time.time()
    
    while time.time() - start < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(("127.0.0.1", port)) == 0:
                return True
        time.sleep(0.5)
    return False


@pytest.fixture(scope="session", autouse=True)
def distributed_system():
    """
    Fixture automática de sessão.

    Executa antes de qualquer teste:
        - Inicia Name Server
        - Inicia Servidor

    Executa após todos os testes:
        - Encerra os processos
    """
    
    # Limpar processos antigos
    os.system("pkill -f core.name_server")
    os.system("pkill -f core.server")
    time.sleep(1)
    
    # Remover banco de teste antigo
    if os.path.exists(TEST_DB_NAME):
        os.remove(TEST_DB_NAME)
        
    # Definir variável de ambiente para usar o banco de teste
    os.environ["CINEMA_DB"] = TEST_DB_NAME
    
    python_exec = sys.executable
    
    # Inicia Name Server
    name_server = subprocess.Popen([python_exec, "-m", "core.name_server"])
    
    if not wait_for_port(NAME_SERVER_PORT):
        raise RuntimeError("Name Server não iniciou.")
    
    # Inicia Servidor
    server = subprocess.Popen([python_exec, "-m", "core.server"])
    
    if not wait_for_port(SERVER_PORT):
        raise RuntimeError("Servidor não iniciou.")
    
    # Entrega controle para execução dos testes
    yield
    
    server.terminate()
    name_server.terminate()
    
    server.wait()
    name_server.wait()
    