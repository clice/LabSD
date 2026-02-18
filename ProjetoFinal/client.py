import rpyc
import time

SERVER_HOST = "localhost"
SERVER_PORT = 18861

def conectar():
    try:
        conn = rpyc.connect(SERVER_HOST, SERVER_PORT)
        return conn
    except Exception as e:
        print("Erro ao conectar ao servidor:", e)
        return None

def menu():
    print("\n--- Sistema de Reservas ---")
    print("1 - Consultar ingressos")
    print("2 - Reservar ingresso")
    print("3 - Status do servidor")
    print("0 - Sair")

def main():
    conn = conectar()
    if not conn:
        return

    while True:
        menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("Ingressos disponíveis:", conn.root.consultar_ingressos())

        elif opcao == "2":
            nome = input("Seu nome: ")
            qtd = int(input("Quantidade: "))
            resposta = conn.root.reservar_ingresso(nome, qtd)
            print(resposta)

        elif opcao == "3":
            status = conn.root.status_servidor()
            print("Horário:", status["horario"])
            print("Ingressos restantes:", status["ingressos_restantes"])

        elif opcao == "0":
            print("Encerrando...")
            conn.close()
            break

        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
