"""
run.py

Script de inicialização automática do Sistema Distribuído.

Responsável por iniciar, na ordem correta:

- Name Server (Descoberta de Serviço)
- Servidor RPC (Lógica de Negócio)
- Cliente de Teste

Este script executa os componentes como módulos Python,
preservando a estrutura de pacotes do projeto.

Vantagens:
- Execução simplificada
- Ambiente consistente (usa mesma venv)
- Encerramento automático ao finalizar cliente
- Estrutura profissional para apresentação
"""

import subprocess
import time
import sys


def main():
    """
    Fluxo de execução:

    - Inicia Name Server
    - Aguarda estabilização
    - Inicia Servidor
    - Aguarda estabilização
    - Inicia Cliente
    - Ao finalizar cliente, encerra serviços
    """

    # Usa o mesmo interpretador Python da venv ativa
    python_exec = sys.executable

    try:
        # -------------------------------------------------
        # Iniciar Name Server
        # -------------------------------------------------
        print("Iniciando Name Server...")
        name_server = subprocess.Popen(
            [python_exec, "-m", "core.name_server"]
        )

        # Pequena pausa para garantir que o serviço subiu
        time.sleep(2)

        # -------------------------------------------------
        # Iniciar Servidor
        # -------------------------------------------------
        print("Iniciando Servidor...")
        server = subprocess.Popen(
            [python_exec, "-m", "core.server"]
        )

        time.sleep(2)

        # -------------------------------------------------
        # Iniciar Cliente
        # -------------------------------------------------
        print("Iniciando Cliente...")
        subprocess.run(
            [python_exec, "-m", "client.client_test"]
        )

    except KeyboardInterrupt:
        print("\nExecução interrompida pelo usuário.")

    finally:
        # -------------------------------------------------
        # Encerramento seguro dos processos
        # -------------------------------------------------
        print("Encerrando serviços...")

        try:
            name_server.terminate()
        except:
            pass

        try:
            server.terminate()
        except:
            pass

        print("Todos os processos foram encerrados.")


if __name__ == "__main__":
    main()
