"""
Servidor Multithread (server.py)

Este servidor:
    •   Escuta na porta 8000
    •   Para cada cliente, cria uma thread
    •   Recebe uma string
    •   Se for "HORARIO", responde com o horário atual
    •   Caso contrário, reverte a string e devolve
"""

import socket     # Biblioteca para comunicação via sockets
import threading  # Biblioteca para criação de threads
import json       # Biblioteca para manipulação de JSON


from datetime import datetime  # Biblioteca para manipulação de datas e horas


HOST = "0.0.0.0"    # Escuta em todas as interfaces
PORT = 8000         # Porta para escutar
dataPayload = 4096  # Tamanho máximo dos dados a serem recebidos


def handle_client(conn, addr): 
    """
    Função para lidar com cada cliente em uma thread separada
    """
    try:
        # Recebe mensagem do cliente
        msg_recv = conn.recv(dataPayload)
        
        print(f"[RECEBIDO] {addr}")

        # Se não recebeu nada, encerra a conexão
        if not msg_recv:
            return

        # Prepara a resposta para enviar ao cliente
        msg_sent = {
            "time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "text": msg_recv.decode()[::-1]
        }

        json_str = json.dumps(msg_sent)  # Converte a mensagem para JSON

        conn.sendall(json_str.encode())  # Envia a resposta ao cliente
        
        print(f"[ENVIADO] {addr}")
    except Exception as e:
        # Em caso de erro, exibe a mensagem de erro
        print(f"[ERRO] {addr}: {e}")
    finally:
        # Encerra a conexão com o cliente
        conn.close()


def main():
    """
    Função principal do servidor
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # Cria o socket TCP
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Permite reutilizar o endereço
    server.bind((HOST, PORT))                                     # Associa o socket ao endereço e porta
    server.listen(50)                                             # Começa a escutar por conexões

    print(f"[SERVIDOR] Escutando em {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()  # Aceita uma nova conexão
        print(f"[CONEXÃO] {addr}")

        # Cria uma thread para lidar com o cliente
        t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        t.start()  # Inicia a thread    


if __name__ == "__main__":
    main()
    