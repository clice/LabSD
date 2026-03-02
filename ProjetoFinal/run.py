"""
run.py

Script de inicialização automática do Sistema Distribuído.

Funcionalidades:
- Verifica depedências
- Inicia Name Server
- Inicia Servidor
- Aguarda inicialização real
- Executa Cliente
- Finaliza processos corretamente

Este script executa os componentes como módulos Python,
preservando a estrutura de pacotes do projeto.

Vantagens:
- Execução simplificada
- Ambiente consistente (usa mesma .venv)
- Encerramento automático ao finalizar cliente
- Estrutura profissional para apresentação
"""

import subprocess
import time
import sys
import socket

# Importa portas diretamente do config
from config import NAME_SERVER_PORT, SERVER_PORT


# ==================================================
# Verificar dependências
# ==================================================

def check_dependencies():
    """
    Verifica se RPyC está instalado.
    Caso não esteja, instala automaticamente.
    """
    
    try:
        import rpyc
    except ImportError:
        print("RPyC não encontrado. Instalando...")
        subprocess.run([sys.executable, "-m", "pip", "install", "rpyc"])


# ==================================================
# Função para aguardar porta abrir
# ==================================================

def wait_for_port(port, timeout=10):
    """
    Aguarda até que uma porta TCP esteja disponível.

    Parâmetros:
        port (int): Porta a ser verificada.
        timeout (int): Tempo máximo de espera em segundos.

    Retorna:
        True  -> Se a porta abriu dentro do tempo.
        False -> Se o tempo expirou.

    Isso evita race condition na inicialização dos serviços.
    """
    
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        
        # Tenta abrir a conexão TCP local
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            result = sock.connect_ex(("127.0.0.1", port))
            
            # Se connect_ex retornar 0 a porta está aberta
            if result == 0:
                return True
            
            time.sleep(0.5)
    
    return False


# ==================================================
# Execução Principal
# ==================================================

def main():
    """
    Fluxo de execução:
    - Verifica dependências
    - Inicia Name Server
    - Aguarda porta do Name Server abrir
    - Inicia Servidor
    - Aguarda porta do Servidor abrir
    - Executa Cliente
    - Finaliza todos os processos
    """
    
    check_dependencies()  # Verificar dependências antes de iniciar os serviços
    
    
    # Usa o mesmo interpretador Python da venv ativa
    python_exec = sys.executable
    
    name_server = None
    server = None

    try:
        # -------------------------------------------------
        # Iniciar Name Server
        # -------------------------------------------------
        print("Iniciando Name Server...")
        name_server = subprocess.Popen(
            [python_exec, "-m", "core.name_server"]
        )
        
        if not wait_for_port(NAME_SERVER_PORT):
            raise Exception("Name Server não iniciou corretamente dentro do tempo esperado. Verifique os logs.")

        # -------------------------------------------------
        # Iniciar Servidor
        # -------------------------------------------------
        print("Iniciando Servidor...")
        server = subprocess.Popen(
            [python_exec, "-m", "core.server"]
        )
        
        if not wait_for_port(SERVER_PORT):
            raise Exception("Servidor não iniciou corretamente dentro do tempo esperado. Verifique os logs.")

        # -------------------------------------------------
        # Iniciar Cliente Test
        # -------------------------------------------------
        print("Iniciando Cliente...")
        subprocess.run(
            [python_exec, "-m", "client.client_test"]
        )

    except KeyboardInterrupt:
        print("\nExecução interrompida pelo usuário.")
        
    except Exception as e:
        print(f"Erro durante inicialização: {e}")

    finally:
        # -------------------------------------------------
        # Encerramento seguro dos processos
        # -------------------------------------------------
        print("Encerrando serviços...")

        if server:
            server.terminate()
            server.wait()
            
        if name_server:
            name_server.terminate()
            name_server.wait()

        print("Todos os processos foram encerrados.")


if __name__ == "__main__":
    main()
