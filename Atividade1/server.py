"""
Servidor Multithread (server.py)

Este servidor:
    •   Escuta na porta 8000
    •   Para cada cliente, cria uma thread
    •   Recebe uma string
    •   Se for "HORARIO", responde com o horário atual
    •   Caso contrário, reverte a string e devolve
"""

import socket
import threading
import datetime


HOST = "0.0.0.0"
PORT = 8000


def handle_client(conn, addr):
    print(f"[+] Conexão estabelecida com {addr}")
    data = conn.recv(1024).decode()

    if data == "HORARIO":
        resposta = datetime.datetime.now().strftime("%H:%M:%S")
    else:
        resposta = data[::-1]  # reverte a string

    conn.send(resposta.encode())
    conn.close()
    print(f"[-] Conexão encerrada com {addr}")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"Servidor rodando na porta {PORT}...")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    main()
    