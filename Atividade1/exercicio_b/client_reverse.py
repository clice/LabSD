"""
Cliente (client.py)


"""

import socket  # Biblioteca para comunicação via sockets
import json    # Biblioteca para manipulação de JSON


HOST = "127.0.0.1"  # Localhost
PORT = 8000         # Mesma porta do servidor para escutar
dataPayload = 4096  # Tamanho máximo dos dados a serem recebidos


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria o socket TCP
    # Conecta ao servidor
    # Se o servidor não estiver rodando, dá erro (ConnectionRefusedError)
    client.connect((HOST, PORT)) 
    
    print(f"[CLIENTE] Escutando em {HOST}:{PORT}")
    print("----------------------------------------------")

    message = input("Envie uma mensagem ao servidor: ")  # Lê a mensagem do usuário
    
    print(f"[ENVIANDO] {message}")
    
    client.sendall(message.encode())  # Envia a mensagem ao servidor, espera chegar dados

    data = client.recv(dataPayload).decode()  # Recebe a resposta do servidor
    
    print(f"[MENSAGEM RECEBIDA]")

    message = json.loads(data)  # Converte a resposta de JSON para dicionário

    print("Horario recebido do servidor: ", message["time"])
    print("Mensagem: ", message["text"])

    client.close()  # Encerra a conexão com o servidor

if __name__ == "__main__":
    main()
    