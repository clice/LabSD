"""
client_test.py

Cliente simples de teste para validar
o servidor distribuído de cinema.

- Conectar ao servidor via RPC
- Testar listagem de filmes
- Testar listagem de sessões
- Testar compra de ingressos
"""

from wsgiref import headers

from client.client_core import ClientCore


# ======================================================
# Funções do menu, interação com o usuário e print de resultados
# ======================================================

def main():
    core = ClientCore()
    
    if not core.connect():
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

        elif opcao == "0":
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


def print_table(headers, rows):
    """
    Imprime dados em formato de tabela organizada no terminal.

    headers -> lista com nomes das colunas
    rows -> lista de tuplas ou listas
    """

    # Calcular largura máxima de cada coluna
    col_widths = []

    for col in range(len(headers)):
        max_width = len(str(headers[col]))

        for row in rows:
            max_width = max(max_width, len(str(row[col])))

        col_widths.append(max_width)

    # Função para imprimir linha separadora
    def print_separator():
        print("+", end="")
        for width in col_widths:
            print("-" * (width + 2) + "+", end="")
        print()

    # Imprimir cabeçalho
    print_separator()
    print("|", end="")

    for i, header in enumerate(headers):
        print(f" {header.ljust(col_widths[i])} |", end="")

    print()
    print_separator()

    # Imprimir linhas
    for row in rows:
        print("|", end="")
        for i, cell in enumerate(row):
            print(f" {str(cell).ljust(col_widths[i])} |", end="")
        print()

    print_separator()


# ======================================================
# Funções das opções do menu 
# Cada função deve chamar o método correspondente do ClientCore e tratar a resposta
# ======================================================

def listar_filmes(core):
    """
    Solicita ao servidor a listagem de filmes.
    """

    resposta = core.listar_filmes()
    
    if resposta["status"] == "success":
        # A resposta de sucesso deve conter a lista de filmes no campo "data"
        
        filmes = resposta["data"]
        
        headers = ["ID", "Título", "Gênero", "Duração (min)"]
        
        print("\n--- Filmes Disponíveis ---")
        print_table(headers, filmes)
            
    else:
        # Em caso de erro, a resposta deve conter uma mensagem de erro no campo "message"
        
        print(resposta["message"])

def listar_sessoes_por_filme(core):
    """
    Solicita ao servidor a listagem de sessões para um filme.
    """

    try:
        filme_id = int(input("Digite o ID do filme: "))
    except ValueError:
        print("ID inválido.")
        return

    resposta = core.listar_sessoes_por_filme(filme_id)
    
    if resposta["status"] == "success":
        # A resposta de sucesso deve conter a lista de sessões no campo "data"

        sessoes = resposta["data"]
        
        headers = ["Sessão ID", "Horário", "Total", "Disponíveis"]

        print("\n--- Sessões Disponíveis ---")
        print_table(headers, sessoes)
            
    else:
        # Em caso de erro, a resposta deve conter uma mensagem de erro no campo "message"
        
        print(resposta["message"])


def comprar_ingresso(core):
    """
    Solicita ao servidor a compra de ingressos.
    """

    nome = input("Nome: ")
    email = input("Email: ")
    sessao_id = int(input("ID da Sessão: "))
    quantidade = int(input("Quantidade: "))
    
    resposta = core.comprar_ingresso(nome, email, sessao_id, quantidade)
    
    if resposta["status"] == "success":
        # Em caso de sucesso, a resposta deve conter os detalhes da compra no campo "data"        
        compra = resposta["data"]
        
        print("\nCompra realizada com sucesso!")
        print(f"Ingressos restantes na sessão: {compra['ingressos_disponiveis']}")
        
    else:
        # Em caso de erro, a resposta deve conter uma mensagem de erro no campo "message"
        
        print(resposta["message"])


# ======================================================
# Inicialização do programa
# ======================================================

if __name__ == "__main__":
    main()