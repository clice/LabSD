import rpyc

if __name__ == "__main__":
    print("Conectando ao servidor...")

    conn = rpyc.connect("localhost", 18861) # Conecta ao servidor RPC rodando na máquina local (localhost) na porta 18861.

    horario = conn.root.get_horario() # Chama o método remoto "get_horario" definido no servidor para obter o horário atual.

    print("Horário recebido do servidor:", horario)

    conn.close() # Encerra a conexão com o servidor RPC.
    print("Conexão encerrada.")
