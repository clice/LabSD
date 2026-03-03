"""
run_gui.py

Script de inicialização do sistema completo com GUI.

Responsabilidades:

- Iniciar Name Server
- Iniciar Servidor
- Aguardar portas ficarem disponíveis
- Abrir GUI
- Encerrar processos corretamente ao fechar GUI

Este script é recomendado para execução durante
apresentações e uso normal da aplicação.
"""

import sys
import os

# Adiciona a raiz do projeto ao PYTHONPATH
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

import subprocess
import time
import socket

from config import NAME_SERVER_PORT, SERVER_PORT


# ======================================================
# Função para aguardar porta TCP ficar disponível
# ======================================================

def wait_for_port(port, timeout=10):
    """
    Aguarda até que a porta esteja aberta.
    Evita que a GUI tente conectar antes do servidor iniciar.
    """

    start = time.time()

    while time.time() - start < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(("127.0.0.1", port)) == 0:
                return True
        time.sleep(0.5)

    return False


# ======================================================
# Execução Principal
# ======================================================

if __name__ == "__main__":

    python_exec = sys.executable

    print("Iniciando Name Server...")
    name_server = subprocess.Popen(
        [python_exec, "-m", "core.name_server"]
    )

    if not wait_for_port(NAME_SERVER_PORT):
        print("Erro ao iniciar Name Server.")
        name_server.terminate()
        sys.exit(1)

    print("Iniciando Servidor...")
    server = subprocess.Popen(
        [python_exec, "-m", "core.server"]
    )

    if not wait_for_port(SERVER_PORT):
        print("Erro ao iniciar Servidor.")
        server.terminate()
        name_server.terminate()
        sys.exit(1)

    print("Abrindo GUI...")

    try:
        # Executa GUI no processo principal
        subprocess.run(
            [python_exec, "-m", "gui.gui_app"]
        )

    finally:
        print("Encerrando sistema...")

        server.terminate()
        name_server.terminate()

        server.wait()
        name_server.wait()

        print("Sistema encerrado com sucesso.")