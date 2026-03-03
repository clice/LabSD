"""
client_test.py

Cliente simples de teste para validar
o servidor distribuído de cinema.

- Conectar ao servidor via RPC
- Testar listagem de filmes
- Testar listagem de sessões
- Testar compra de ingressos
"""

from client.client_core import ClientCore


# ======================================================
# Funções do menu, interação com o usuário e print de resultados
# ======================================================

def main():
    core = ClientCore()
    
    # Tentar conectar ao servidor
    if not core.connect():
        print("Não foi possível conectar ao servidor.")
        return

    # Loop principal do menu
    while True:

        menu()
        option = input("Escolha uma opção: ")

        if option == "1":
            # Solicitar listagem de filmes ao servidor e imprimir resultado
            list_movies(core)

        elif option == "2":
            # Solicitar listagem de sessões para um filme ao servidor e imprimir resultado
            list_screenings_by_movie(core)

        elif option == "3":
            # Solicitar compra de ingressos ao servidor e imprimir resultado
            buy_tickets(core)

        elif option == "0":
            # Encerrar o programa
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
    
    if not rows:
        print("Nenhum dado encontrado.")
        return

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

def list_movies(core):
    """
    Solicita ao servidor a listagem de filmes.
    """

    result = core.list_movies()
    
    if result["status"] == "success":
        # A resposta de sucesso deve conter a lista de filmes no campo "data"
        
        movies = result["data"]        
        headers = ["ID", "Título", "Gênero", "Duração (min)"]
        
        print("\n--- Filmes Disponíveis ---")
        print_table(headers, movies)
            
    else:
        # Em caso de erro, a resposta deve conter uma mensagem de erro no campo "message"        
        print(result["message"])

def list_screenings_by_movie(core):
    """
    Solicita ao servidor a listagem de sessões para um filme.
    """

    try:
        movie_id = int(input("Digite o ID do filme: "))
    except ValueError:
        print("ID inválido.")
        return

    result = core.list_screenings_by_movie(movie_id)
    
    if result["status"] == "success":
        # A resposta de sucesso deve conter a lista de sessões no campo "data"
        screenings = result["data"]        
        headers = ["Sessão ID", "Horário", "Total", "Disponíveis"]

        print("\n--- Sessões Disponíveis ---")
        print_table(headers, screenings)
            
    else:
        # Em caso de erro, a resposta deve conter uma mensagem de erro no campo "message"        
        print(result["message"])


def buy_tickets(core):
    """
    Solicita ao servidor a compra de ingressos.
    """

    name = input("Nome: ")
    email = input("Email: ")
    screening_id = int(input("ID da Sessão: "))
    quantity = int(input("Quantidade: "))
    
    result = core.buy_tickets(name, email, screening_id, quantity)
    
    if result["status"] == "success":
        # Em caso de sucesso, a resposta deve conter os detalhes da compra no campo "data"        
        purchase = result["data"]
        
        print("\nCompra realizada com sucesso!")
        print(f"Ingressos restantes na sessão: {purchase['available_tickets']}")
        
    else:
        # Em caso de erro, a resposta deve conter uma mensagem de erro no campo "message"        
        print(result["message"])


# ======================================================
# Inicialização do programa
# ======================================================

if __name__ == "__main__":
    main()