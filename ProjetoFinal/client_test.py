"""
client_test.py

Cliente simples de teste para validar
o servidor distribuído de cinema.

- Conectar ao servidor via RPC
- Testar listagem de filmes
- Testar listagem de sessões
- Testar compra de ingressos
"""

import rpyc


SERVER_HOST = "localhost"
SERVER_PORT = 18861


def conectar():
    """
    Estabelece conexão com servidor RPC.
    """

    try:
        conn = rpyc.connect(SERVER_HOST, SERVER_PORT)
        print("Conectado ao servidor.")
        return conn

    except Exception as e:
        print("Erro ao conectar:", e)
        return None


def menu():
    print("\n===== COMPRA DE INGRESSOS DO CINEMA =====")
    print("1 - Listar Filmes")
    print("2 - Listar Sessões")
    print("3 - Comprar Ingresso")
    print("0 - Sair")


def listar_filmes(conn):

    filmes = conn.root.listar_filmes()

    print("\n--- Filmes Disponíveis ---")

    for filme in filmes:
        print(
            f"ID: {filme[0]} | "
            f"Título: {filme[1]} | "
            f"Gênero: {filme[2]} | "
            f"Duração: {filme[3]} min"
        )


def listar_sessoes(conn):

    filme_id = int(input("Digite o ID do filme: "))

    sessoes = conn.root.listar_sessoes(filme_id)

    print("\n--- Sessões Disponíveis ---")

    for sessao in sessoes:
        print(
            f"Sessão ID: {sessao[0]} | "
            f"Horário: {sessao[1]} | "
            f"Ingressos: {sessao[2]}"
        )


def comprar_ingresso(conn):

    nome = input("Nome: ")
    email = input("Email: ")
    sessao_id = int(input("ID da Sessão: "))
    quantidade = int(input("Quantidade: "))

    resultado = conn.root.comprar_ingresso(
        nome,
        email,
        sessao_id,
        quantidade
    )

    print("\nResultado:", resultado)


def main():

    conn = conectar()

    if not conn:
        return

    while True:

        menu()
        opcao = input("Escolha: ")

        if opcao == "1":
            listar_filmes(conn)

        elif opcao == "2":
            listar_sessoes(conn)

        elif opcao == "3":
            comprar_ingresso(conn)

        elif opcao == "0":
            print("Encerrando...")
            conn.close()
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
