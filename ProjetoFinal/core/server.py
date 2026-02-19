"""
server.py

SErvidor do Sistema Distribuído do Cinema

- Comunicação via RPC utilizando RPyC (Middleware)
- Arquittura N-Camadas (Camada de Negócio)
- Concorrência (ThreadedServer)
- Proteger recursos compartilhados com exclusão mútua
- Utlizar SQLite como persistência durável
- Tratar falhas internas com logging estruturado

O servidor espões métodos que podem ser chamados remotamente
pelos clientes como se fossem funções locais.
"""


import rpyc
from rpyc.utils.server import ThreadedServer
import threading
import logging

import database
from config import ( 
        SERVER_PORT, 
        NAME_SERVER_HOST, NAME_SERVER_PORT, SERVICE_NAME,
        LOG_FORMAT
    )


# Configuração de logging para monitoramento e depuração
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT
)


def response(status, message, data=None):
    """
    Formata a resposta para os clientes de forma consistente.
    """
    return {
        "status": status,
        "message": message,
        "data": data
    }


class CinemaService(rpyc.Service):
    """
    Define métodos remotos disponíveis aos clientes (Serviço RPC).
    Cada método representa uma operação da lógica de negócios.
    """
    
    # Lock para garantir exclusão mútua
    lock = threading.Lock()
    
    
    def exposed_listar_filmes(self):
        """
        Retorna lista de todos os filmes cadastrados.
        """
        
        try:
            # Garantir que apenas uma thread acesse o banco de dados por vez
            
            filmes = database.listar_filmes()
            
            logging.info("Filmes listados com sucesso.")
            
            return response(
                "success", 
                "Filmes listados com sucesso.",
                filmes
            )
        
        except Exception as e:
            # Logar o erro para análise posterior
            
            logging.error(f"Erro ao listar filmes: {e}")
            
            return response(
                "error",
                "Erro interno ao listar filmes."
            )
    
    
    def exposed_listar_sessoes_por_filme(self, filme_id):
        """
        Retorna lista de sessões disponíveis para um filme específico.
        """
        
        if not isinstance(filme_id, int):
            # Logar o erro de entrada inválida
            return response(
                "error",
                "ID do filmes inválido."
            )
        
        try:
            # Garantir que apenas uma thread acesse o banco de dados por vez
            
            sessoes = database.listar_sessoes_por_filme(filme_id)
            
            logging.info(f"Sessões listadas para filme_id={filme_id}.")
            
            return response(
                "success",
                "Sessões listadas com sucesso.",
                sessoes
            )
        
        except Exception as e:
            # Logar o erro para análise posterior
            
            logging.error(f"Erro ao listar sessões: {e}")
            
            return response(
                "error",
                "Erro interno ao listar sessões."
            )
            
    
    def exposed_comprar_ingresso(self, nome, email, sessao_id, quantidade):
        """
        Processa a compra de ingressos para uma sessão específica.
        """
        
        if not isinstance(nome, str) or not nome.strip():
            return response("error", "Nome do cliente inválido.")
        
        if not isinstance(email, str) or not email.strip():
            return response("error", "E-mail do cliente inválido.")
        
        if not isinstance(sessao_id, int):
            return response("error", "ID da sessão inválida.")
        
        if not isinstance(quantidade, int) or quantidade <= 0:
            return response("error", "Quantidade de ingressos inválida.")
        
        try:
            # Garantir que apenas uma thread acesse o banco de dados por vez
            
            with CinemaService.lock:
                # Verificar disponibilidade de ingressos antes de processar a compra
                
                resultado = database.comprar_ingresso(nome, email, sessao_id, quantidade)
                
                # Se resultado já for dict padronizado (ideal)
                if isinstance(resultado, dict):
                    return resultado

                # Se banco ainda retornar string (compatibilidade)
                return response("success", resultado)

        except Exception as e:
            logging.error(f"Erro ao comprar ingresso: {e}")

            return response(
                "error",
                "Erro interno ao realizar compra."
            )
            

def registrar_no_name_server():
    """
    Registrar o serviço no Name Server para descoberta pelos clientes.
    """
    
    try:
        # Registrar o serviço no Name Server para descoberta pelos clientes
        
        # Conectar ao Name Server e registrar o serviço        
        conn = rpyc.connect(NAME_SERVER_HOST, NAME_SERVER_PORT)
        
        # Registrar o serviço com nome, host e porta do servidor principal
        conn.root.register(SERVICE_NAME, SERVER_HOST, SERVER_PORT)
        
        conn.close()
        
        logging.info("Servidor registrado no Name Server com sucesso.")
        
    except Exception as e:
        # Logar o erro para análise posterior
        logging.error(f"Erro ao registrar no Name Server: {e}")
        

if __name__ == "__main__":
    """
    Inicializa o banco de dados, 
    registra o serviço no Name Server e inicia o servidor RPC.    
    """
    
    logging.info("===================================")
    logging.info("Iniciando Servidor do Cinema...")
    logging.info("===================================")
    
    try:
        # Inicializar o banco de dados (criar tabelas e inserir dados iniciais)
        
        database.inicializar_banco()
        logging.info("Banco de dados inicializado com sucesso.")
        
        registrar_no_name_server()
        
        server = ThreadedServer(CinemaService, port=SERVER_PORT)
        
        logging.info("Servidor aguardando conexões...")
        server.start()
        
    except KeyboardInterrupt:
        # Logar a interrupção do servidor pelo usuário
        logging.info("Servidor interrompido pelo usuário.")
        
    except Exception as e:
        # Logar o erro para análise posterior
        logging.error(f"Falha ao iniciar o servidor: {e}")