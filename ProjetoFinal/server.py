"""
server.py

Servidor do Sistema Distribuído do Cinema

- Comunicação via RPC utilizando RPyC (Middleware)
- Arquitetura N-Camadas (Camada de Negócio)
- Concorrência (ThreadedServer)
- Proteger recursos compartilhados com exclusão mútua
- Utilizar SQLite como persistência durável
- Tratar falhas internas com logging estruturado

O servidor expõe métodos que podem ser chamados remotamente
pelos clientes como se fossem funções locais.
"""

import rpyc
from rpyc.utils.server import ThreadedServer
import threading
import logging
import database

# Configurações de conexão e serviço
NAME_SERVER_HOST = "localhost"
NAME_SERVER_PORT = 18862
SERVICE_NAME = "cinema_service"


# Configuração de logging para monitoramento e depuração
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class CinemaService(rpyc.Service):
    """
    Define métodos remotos disponíveis aos clientes.

    Cada método representa uma operação da lógica de negócio.
    """

    # Lock para garantir exclusão mútua
    lock = threading.Lock()

    def exposed_listar_filmes(self):
        """
        Retorna lista de todos os filmes cadastrados.
        """        
        
        try:
            # Logar a consulta de filmes para monitoramento
            filmes = database.listar_filmes()
            logging.info("Listagem de filmes realizada.")
            return filmes

        except Exception as e:
            # Logar o erro para análise posterior
            logging.error(f"Erro ao listar filmes: {e}")
            return "Erro interno no servidor."
    

    def exposed_listar_sessoes(self, filme_id):
        """
        Retorna sessões disponíveis para um filme.
        """

        # Validar que o ID do filme é um inteiro positivo
        if not isinstance(filme_id, int):
            return "ID do filme inválido."

        try:
            # Logar a consulta de sessões para monitoramento
            sessoes = database.listar_sessoes_por_filme(filme_id)
            logging.info(f"Sessões consultadas para filme {filme_id}.")
            return sessoes

        except Exception as e:
            # Logar o erro para análise posterior
            logging.error(f"Erro ao listar sessões: {e}")
            return "Erro interno no servidor."
        
        
    def exposed_comprar_ingresso(self, nome_cliente, email, sessao_id, quantidade):
        """
        Realiza compra de ingressos.

        Valida os dados, exclusão mútua e persistência transacional
        """        

        # Validação básica dos dados de entrada para evitar erros comuns
        if not isinstance(nome_cliente, str) or not nome_cliente.strip():
            return "Nome inválido."

        # Validação simples de email (pode ser aprimorada com regex)
        if not isinstance(email, str) or not email.strip():
            return "Email inválido."

        # Validar que sessao_id e quantidade são inteiros positivos
        if not isinstance(sessao_id, int):
            return "Sessão inválida."

        # Validar que a quantidade é um inteiro positivo
        if not isinstance(quantidade, int) or quantidade <= 0:
            return "Quantidade inválida."        

        try:
            # Garantir que apenas uma compra seja processada por vez 
            # para evitar estouro de ingressos
            with CinemaService.lock:
                # O método comprar_ingresso do database já lida com a lógica de transação
                
                # Logar a tentativa de compra para monitoramento
                resultado = database.comprar_ingresso(
                    nome_cliente,
                    email,
                    sessao_id,
                    quantidade
                )

                # Logar o resultado da compra (sucesso ou falha) para análise posterior
                logging.info(
                    f"Compra realizada por {nome_cliente} "
                    f"(Sessão {sessao_id}, Qtd {quantidade})"
                )

                return resultado

        except Exception as e:
            # Logar o erro para análise posterior
            logging.error(f"Erro ao comprar ingresso: {e}")
            return "Erro interno no servidor."
        

def registrar_no_name_server():
    """
    Registra o serviço no Name Server para que clientes possam descobri-lo.
    """
    
    
    try:
        # Conectar ao Name Server e registrar o serviço com seu endereço
        conn = rpyc.connect(
            NAME_SERVER_HOST,
            NAME_SERVER_PORT
        )

        conn.root.register(
            SERVICE_NAME,
            "localhost",
            18861
        )

        conn.close()

        logging.info("Registrado no Name Server.")

    except Exception as e:
        # Logar o erro para análise posterior, mas continuar 
        # rodando o servidor localmente
        logging.error(
            f"Erro ao registrar no Name Server: {e}"
        )


if __name__ == "__main__":
    """
    Ponto de entrada do servidor.
    """    

    logging.info("===================================")
    logging.info("Servidor de Cinema iniciado")
    logging.info("===================================")

    try:
        # Inicializar banco de dados (criar tabelas e dados iniciais)
        database.inicializar_banco()
        logging.info("Banco inicializado com sucesso.")
        
        # Registrar o serviço no Name Server para descoberta pelos clientes
        registrar_no_name_server()

        # Iniciar servidor RPC com suporte a múltiplas conexões
        server = ThreadedServer(
            CinemaService,
            port=18861
        )

        # Logar que o servidor está pronto para aceitar conexões
        logging.info("Servidor aguardando conexões...")
        server.start()

    except Exception as e:
        # Logar falha crítica ao iniciar o servidor para análise posterior
        logging.critical(f"Falha ao iniciar servidor: {e}")