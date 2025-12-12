"""
Servidor Multithread (server.py)

Este servidor:
    •   Escuta na porta 8000
    •   Para cada cliente, cria uma thread
    •   Recebe uma string do cliente
    •   Responde com a hora atual e a string invertida
"""

import socket                  # Biblioteca para comunicação via sockets
import threading               # Biblioteca para criação de threads


HOST = "0.0.0.0"    # Escuta em todas as interfaces
PORT = 8000         # Porta para escutar
dataPayload = 4096  # Tamanho máximo dos dados a serem recebidos


def handle_client(conn, addr): 
    """
    Função executada por uma thread (uma thread por cliente).
    Ela recebe:
      - conn: o socket da conexão com aquele cliente específico
      - addr: o endereço do cliente (IP, porta)
    """
    try:
        # Recebe mensagem do cliente, ele fica esperando chegar dados.
        msg_recv = conn.recv(dataPayload)
        
        print(f"[RECEBIDO] {addr}")

        # Se não recebeu nada, encerra a conexão
        if not msg_recv:
            return
        
        msg_sent = msg_recv.decode()[::-1]  # Inverte a string recebida

        conn.sendall(msg_sent.encode())  # Envia a resposta ao cliente
        
        print(f"[ENVIADO] {addr}")
        
    except Exception as e:
        # Em caso de erro, exibe a mensagem de erro
        print(f"[ERRO] {addr}: {e}")
        
    finally:
        # Encerra a conexão com o cliente
        conn.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # Cria o socket TCP
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Permite reutilizar o endereço
    server.bind((HOST, PORT))                                     # Associa o socket ao endereço e porta
    server.listen(50)                                             # Começa a escutar por conexões

    print(f"[SERVIDOR] Escutando em {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()  # Aceita uma nova conexão, espera alguém conectar.
        print(f"[CONEXÃO] {addr}")

        # Cria uma thread para lidar com o cliente
        # daemon=True: se você fechar o programa principal, as threads morrem junto
        t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        t.start()  # Inicia a thread    


if __name__ == "__main__":
    main()
    