"""
Cliente (client_time.py)

Este cliente:
    •   Conecta ao servidor na porta 8000
    •   Envia uma mensagem solicitando a hora
    •   Recebe e exibe a hora atual enviada pelo servidor
"""

import socket  # Biblioteca para comunicação via sockets


HOST = "127.0.0.1"  # Localhost
PORT = 8000         # Mesma porta do servidor para escutar
dataPayload = 4096  # Tamanho máximo dos dados a serem recebidos


def main():
    # Cria o socket TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    
    # Conecta ao servidor
    # Se o servidor não estiver rodando, dá erro (ConnectionRefusedError)
    client.connect((HOST, PORT)) 
    
    print(f"[CLIENTE] Escutando em {HOST}:{PORT}")
        
    client.sendall(b"HORA")  # Envia a mensagem ao servidor, espera chegar dados

    data = client.recv(dataPayload).decode()  # Recebe a resposta do servidor
    
    print(f"[MENSAGEM RECEBIDA]")

    print("Horario recebido do servidor:", data)

    client.close()  # Encerra a conexão com o servidor

if __name__ == "__main__":
    main()
    