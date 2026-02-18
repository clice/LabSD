"""
client.py

Cliente da aplicação distribuída de reservas de ingressos.

Este cliente se comunica com o servidor utilizando RPC (RPyC),
sem manipular sockets diretamente, garantindo transparência de acesso.

Também implementa tolerância a falhas através de:
- Retry automático na conexão
- Retry automático em chamadas remotas
"""

import rpyc
import time

# Configurações do Servidor

SERVER_HOST = "localhost"   # Endereço do servidor
SERVER_PORT = 18861         # Porta do serviço RPC

# Parâmetros de tolerância a falhas
MAX_RETRIES = 3             # Número máximo de tentativas
RETRY_DELAY = 2             # Tempo de espera entre tentativas (segundos)


def conectar_com_retry():
    # Tenta estabelecer conexão com o servidor.
    # Caso falhe, realiza novas tentativas automaticamente.
    # Tolerância a falhas e transparência de falhas    

    tentativas = 0

    while tentativas < MAX_RETRIES:
        try:
            print(f"Tentando conectar... ({tentativas + 1}/{MAX_RETRIES})")
            
            # Conexão via RPC (middleware)
            conn = rpyc.connect(SERVER_HOST, SERVER_PORT)
            
            print("Conectado ao servidor.")
            return conn

        except Exception as e:
            print("Falha na conexão:", e)
            tentativas += 1
            time.sleep(RETRY_DELAY)

    print("Servidor indisponível após várias tentativas.")
    return None


def chamar_com_retry(funcao, *args):
    # Executa uma função remota com mecanismo de retry.    
    # Se ocorrer falha, ele tenta novamente automaticamente.    
    # Tolerância a falhas e robustez do cliente
    
    tentativas = 0

    while tentativas < MAX_RETRIES:
        try:
            return funcao(*args)

        except Exception as e:
            print("Erro na chamada remota:", e)
            tentativas += 1
            time.sleep(RETRY_DELAY)

    return "Falha após múltiplas tentativas."


def menu():
    print("\n--- Sistema de Reservas ---")
    print("1 - Consultar ingressos")
    print("2 - Reservar ingresso")
    print("3 - Status do servidor")
    print("0 - Sair")


def main():
    # Representa a Camada de Apresentação (UI).
    # Não conhece sockets.
    # Não conhece protocolo.
    # Apenas utiliza o middleware (RPyC).
    
    # Demonstra:
    # ✔ Transparência de acesso
    # ✔ Separação em N-Camadas
    
    # Conectar ao servidor
    conn = conectar_com_retry()
    if not conn:
        return

    while True:
        menu()
        opcao = input("Escolha uma opção: ")

        # Consultar ingressos
        if opcao == "1":
            resposta = chamar_com_retry(
                conn.root.consultar_ingressos
            )
            print("Ingressos disponíveis:", resposta)

        # Reservar ingresso
        elif opcao == "2":
            nome = input("Seu nome: ")
            qtd = int(input("Quantidade: "))

            resposta = chamar_com_retry(
                conn.root.reservar_ingresso,
                nome,
                qtd
            )
            print(resposta)

        # Status do servidor
        elif opcao == "3":
            status = chamar_com_retry(
                conn.root.status_servidor
            )

            if isinstance(status, dict):
                print("Horário:", status["horario"])
                print("Ingressos restantes:", status["ingressos_restantes"])
            else:
                print(status)

        # Encerrar
        elif opcao == "0":
            print("Encerrando conexão...")
            conn.close()
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
