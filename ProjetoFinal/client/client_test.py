"""
client_test.py

Cliente simples de teste para validar
o servidor distribuído de cinema.

- Conectar ao servidor via RPC
- Testar listagem de filmes
- Testar listagem de sessões
- Testar compra de ingressos
"""

from client_core import ClientCore


def main():
    core = ClientCore()
    
    if not core.conectar():
        print("Não foi possível conectar ao servidor.")
        return

    while True:

        menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            listar_filmes(core)

        elif opcao == "2":
            listar_sessoes_por_filme(core)

        elif opcao == "3":
            comprar_ingresso(core)

        elif opcao == "4":
            print("Encerrando...")
            core.close()
            break

        else:
            print("Opcao inválida.")


def menu():
    """
    Exibe menu de opções para o usuário.
    """
    
    print("\n===== COMPRA DE INGRESSOS DO CINEMA =====")
    print("1 - Listar Filmes")
    print("2 - Listar Sessões")
    print("3 - Comprar Ingresso")
    print("0 - Sair")


def listar_filmes(core):
    """
    Solicita ao servidor a listagem de filmes.
    """

    filmes = core.listar_filmes()

    # Se o resultado for uma string, é uma mensagem de erro
    if isinstance(filmes, str):
        print(filmes)
        return

    print("\n--- Filmes Disponíveis ---")

    for filme in filmes:
        print(
            f"ID: {filme[0]} | "
            f"Título: {filme[1]} | "
            f"Gênero: {filme[2]} | "
            f"Duração: {filme[3]} min"
        )

def listar_sessoes_por_filme(core):
    """
    Solicita ao servidor a listagem de sessões para um filme.
    """

    filme_id = int(input("Digite o ID do filme: "))

    sessoes = core.root.listar_sessoes(filme_id)

    print("\n--- Sessões Disponíveis ---")

    for sessao in sessoes:
        print(
            f"Sessão ID: {sessao[0]} | "
            f"Horário: {sessao[1]} | "
            f"Ingressos: {sessao[2]}"
        )


def comprar_ingresso(core):
    """
    Solicita ao servidor a compra de ingressos.
    """

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


if __name__ == "__main__":
    main()