"""
Cliente (client.py)

Aqui você escolhe qual teste quer fazer:
	•	"HORARIO" → servidor devolve a hora
	•	Qualquer outra string → servidor devolve a string invertida

"""

import socket

HOST = "127.0.0.1"
PORT = 8000

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    mensagem = "Olá Mundo Distribuído"  # OU: "HORARIO"
    client.send(mensagem.encode())

    resposta = client.recv(1024).decode()
    print("Resposta do servidor:", resposta)

    client.close()

if __name__ == "__main__":
    main()
    