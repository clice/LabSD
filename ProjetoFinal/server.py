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


class TicketService(rpyc.Service):
    # Classe que define os métodos remotos disponíveis aos clientes.
    # Esta classe representa a Camada de Lógica de Negócio
    # dentro da arquitetura em N-Camadas.

    # Lock para garantir exclusão mútua
    lock = threading.Lock()

    def exposed_consultar_ingressos(self):
        # Consultar ingressos disponíveis
        # Retorna a quantidade de ingressos disponíveis.
        # O prefixo 'exposed_' indica que o método pode
        # ser chamado remotamente via RPC.
        # Demonstra a conexão via RPC, o acesso a camada de 
        # persistência e o tratamento de exceções
        
        try:
            quantidade = database.consultar_ingressos()
            logging.info("Consulta de ingressos realizada.")
            return quantidade

        except Exception as e:
            logging.error(f"Erro ao consultar ingressos: {e}")
            return "Erro interno no servidor."
    

    def exposed_reservar_ingresso(self, nome_cliente, quantidade):
        # Realizar a reserva ingresso
        # Com validação de entrada, exclusão mútua para proteger o recurso compartilhado
        # estoque de ingressos (persistência) e tratamento de exceções.
        
        # Validação de cliente
        if not isinstance(nome_cliente, str) or not nome_cliente.strip():
            return "Nome do cliente inválido."

        # Validação de quantidade de ingressos
        if not isinstance(quantidade, int) or quantidade <= 0:
            return "Quantidade inválida."

        try:
            # Garantir que apenas uma reserva seja processada por vez para evitar condições de corrida
            with TicketService.lock:

                sucesso, restante = database.reservar_ingresso(
                    nome_cliente,
                    quantidade
                )

                if sucesso:
                    # Log de reserva bem-sucedida
                    logging.info(
                        f"Reserva realizada por {nome_cliente} "
                        f"({quantidade} ingressos)."
                    )

                    return (
                        f"Reserva confirmada para {nome_cliente}. "
                        f"Ingressos restantes: {restante}"
                    )
                else:
                    # Log de tentativa de reserva falhada por falta de estoque
                    logging.warning(
                        f"Tentativa de reserva falhou "
                        f"(estoque insuficiente)."
                    )
                    return "Ingressos insuficientes."

        except Exception as e:
            # Log de erro detalhado para facilitar a depuração
            logging.error(f"Erro ao reservar ingresso: {e}")
            return "Erro interno no servidor."
        

if __name__ == "__main__":
    # Inicialização do Servidor
    # Ponto de entrada do servidor.
    # Utiliza ThreadedServer para permitir múltiplos clientes
    # simultaneamente (modelo multithread).
    # Concorrência no servidor e capacidade de atender múltiplos nós
    
    logging.info("===================================")
    logging.info("Servidor de Reservas iniciado")
    logging.info("===================================")

    try:
        # Inicializa banco de dados
        database.inicializar_banco()
        logging.info("Banco de dados inicializado com sucesso.")

        # Servidor concorrente
        server = ThreadedServer(
            TicketService,
            port=18861
        )

        logging.info("Servidor aguardando conexões...")
        server.start()

    except Exception as e:
        logging.critical(f"Falha ao iniciar servidor: {e}")
