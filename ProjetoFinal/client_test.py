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


def descobrir_servidor():
    """
    Descobre o endereço do servidor de cinema através do Name Server.
    """
        
    try:
        # Conectar ao Name Server e solicitar o endereço do serviço de cinema
        conn = rpyc.connect("localhost", 18862)

        endereco = conn.root.lookup("cinema_service")

        conn.close()

        if endereco:
            return endereco

        print("Serviço não encontrado.")
        return None

    except Exception as e:
        print("Erro ao conectar ao Name Server:", e)
        return None


def conectar():
    """
    Estabelece conexão com servidor RPC.
    """

    endereco = descobrir_servidor()

    if not endereco:
        return None

    host, port = endereco

    try:
        # Conectar ao servidor de cinema usando o endereço descoberto
        conn = rpyc.connect(host, port)
        print("Conectado ao servidor via Name Server.")
        return conn

    except Exception as e:
        # Logar o erro para análise posterior, 
        # mas continuar tentando conexão direta
        print("Erro ao conectar ao servidor:", e)
        return None


def menu():
    """
    Exibe menu de opções para o usuário.
    """
    
    print("\n===== COMPRA DE INGRESSOS DO CINEMA =====")
    print("1 - Listar Filmes")
    print("2 - Listar Sessões")
    print("3 - Comprar Ingresso")
    print("0 - Sair")


def listar_filmes(conn):
    """
    Solicita ao servidor a listagem de filmes.
    """
    
    filmes = conn.root.listar_filmes()
    
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


def listar_sessoes(conn):
    """
    Solicita ao servidor a listagem de sessões para um filme.
    """

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


def main():
    """
    Função principal do cliente de teste.
    """

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
