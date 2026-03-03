import subprocess
import sys
import time
import socket
import pytest
import os

from config import SERVER_PORT, NAME_SERVER_PORT


def wait_for_port(port, timeout=10):
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
    Sobe Name Server e Servidor antes dos testes.
    Derruba ao final.
    """
    
    # Limpar processos antigos
    os.system("pkill -f core.name_server")
    os.system("pkill -f core.server")

    time.sleep(1)
    
    python_exec = sys.executable
    
    name_server = subprocess.Popen([python_exec, "-m", "core.name_server"])
    
    if not wait_for_port(NAME_SERVER_PORT):
        raise RuntimeError("Name Server não iniciou.")
    
    server = subprocess.Popen([python_exec, "-m", "core.server"])
    
    if not wait_for_port(SERVER_PORT):
        raise RuntimeError("Servidor não iniciou.")
    
    yield
    
    server.terminate()
    name_server.terminate()
    
    server.wait()
    name_server.wait()
    