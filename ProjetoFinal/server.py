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
            filmes = database.listar_filmes()
            logging.info("Listagem de filmes realizada.")
            return filmes

        except Exception as e:
            logging.error(f"Erro ao listar filmes: {e}")
            return "Erro interno no servidor."
    

    def exposed_listar_sessoes(self, filme_id):
        """
        Retorna sessões disponíveis para um filme.
        """

        if not isinstance(filme_id, int):
            return "ID do filme inválido."

        try:
            sessoes = database.listar_sessoes_por_filme(filme_id)
            logging.info(f"Sessões consultadas para filme {filme_id}.")
            return sessoes

        except Exception as e:
            logging.error(f"Erro ao listar sessões: {e}")
            return "Erro interno no servidor."
        
        
    def exposed_comprar_ingresso(self, nome_cliente, email, sessao_id, quantidade):
        """
        Realiza compra de ingressos.

        Valida os dados, exclusão mútua e persistência transacional
        """
        

        if not isinstance(nome_cliente, str) or not nome_cliente.strip():
            return "Nome inválido."

        if not isinstance(email, str) or not email.strip():
            return "Email inválido."

        if not isinstance(sessao_id, int):
            return "Sessão inválida."

        if not isinstance(quantidade, int) or quantidade <= 0:
            return "Quantidade inválida."
        

        try:
            with CinemaService.lock:

                resultado = database.comprar_ingresso(
                    nome_cliente,
                    email,
                    sessao_id,
                    quantidade
                )

                logging.info(
                    f"Compra realizada por {nome_cliente} "
                    f"(Sessão {sessao_id}, Qtd {quantidade})"
                )

                return resultado

        except Exception as e:
            logging.error(f"Erro ao comprar ingresso: {e}")
            return "Erro interno no servidor."
        

if __name__ == "__main__":

    logging.info("===================================")
    logging.info("Servidor de Cinema iniciado")
    logging.info("===================================")

    try:
        database.inicializar_banco()
        logging.info("Banco inicializado com sucesso.")

        server = ThreadedServer(
            CinemaService,
            port=18861
        )

        logging.info("Servidor aguardando conexões...")
        server.start()

    except Exception as e:
        logging.critical(f"Falha ao iniciar servidor: {e}")