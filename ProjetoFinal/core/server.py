"""
server.py

Servidor do Sistema Distribuído do Cinema

Este módulo representa a Camada de Lógica de Negócio
na arquitetura N-Camadas do sistema.

- Comunicação via RPC utilizando RPyC (Middleware)
- Arquittura N-Camadas (Camada de Negócio)
- Concorrência (ThreadedServer)
- Proteger recursos compartilhados com exclusão mútua
- Utlizar SQLite como persistência durável
- Tratar falhas internas com logger estruturado

O servidor espões métodos que podem ser chamados remotamente
pelos clientes como se fossem funções locais (transparência de acesso).
"""


import rpyc
from rpyc.utils.server import ThreadedServer
import time
import threading

from core import database
from config import ( 
    SERVER_HOST, SERVER_PORT, 
    NAME_SERVER_HOST, NAME_SERVER_PORT, SERVICE_NAME
)

from core.color_logger import setup_logger


# ======================================================
# Configuração de Logger
# ======================================================

# Permite rastrear eventos, erros e operações críticas.
logger = setup_logger("CinemaService")


# ======================================================
# Função utilitária para padronizar respostas RPC
# ======================================================

def response(status, message, data=None):
    """
    Formata a resposta para os clientes de forma consistente.
    """
    return {
        "status": status,
        "message": message,
        "data": data
    }


# ======================================================
# Serviço RPC
# ======================================================

class CinemaService(rpyc.Service):
    """
    Define métodos remotos disponíveis aos clientes (Serviço RPC).
    Cada método representa uma operação da lógica de negócios.
    """
    
    # Lock para garantir exclusão mútua
    lock = threading.Lock()
    
    
    def on_connect(self, conn):
        conn._config["allow_pickle"] = False
    
    
    def exposed_list_movies(self):
        """
        Retorna lista de todos os filmes cadastrados.
        """
        
        try:
            # Garantir que apenas uma thread acesse o banco de dados por vez            
            movies = database.list_movies()            
            logger.info("Filmes listados com sucesso.")            
            return response("success", "Filmes listados com sucesso.", movies)
        
        except Exception as e:
            # Logar o erro para análise posterior            
            logger.error(f"Erro ao listar filmes: {e}")            
            return response("error", "Erro interno ao listar filmes.")
    
    
    def exposed_list_screenings_for_movie(self, movie_id):
        """
        Retorna lista de sessões disponíveis para um filme específico.
        """
        
        if not isinstance(movie_id, int):
            # Logar o erro de entrada inválida
            return response("error", "ID do filme inválido.")
        
        try:
            # Garantir que apenas uma thread acesse o banco de dados por vez            
            screenings = database.list_screenings_for_movie(movie_id)            
            logger.info(f"Sessões listadas para filme_id={movie_id}.")
            return response("success", "Sessões listadas com sucesso.", screenings)
        
        except Exception as e:
            # Logar o erro para análise posterior            
            logger.error(f"Erro ao listar sessões: {e}")            
            return response("error", "Erro interno ao listar sessões.")
            
    
    def exposed_buy_tickets(self, name, email, screening_id, quantity):
        """
        Processa a compra de ingressos para uma sessão específica.
        """
        
        if not isinstance(name, str) or not name.strip():
            return response("error", "Nome do cliente inválido.")
        
        if not isinstance(email, str) or not email.strip():
            return response("error", "E-mail do cliente inválido.")
        
        if not isinstance(screening_id, int):
            return response("error", "ID da sessão inválida.")
        
        if not isinstance(quantity, int) or quantity <= 0:
            return response("error", "Quantidade de ingressos inválida.")
        
        try:
            # Garantir que apenas uma thread acesse o banco de dados por vez
            
            with CinemaService.lock:
                # Verificar disponibilidade de ingressos antes de processar a compra
                
                resultado = database.buy_tickets(name, email, screening_id, quantity)
                
                # Se resultado já for dict padronizado (ideal)
                if isinstance(resultado, dict):
                    return resultado

                # Se banco ainda retornar string (compatibilidade)
                return response("success", resultado)

        except Exception as e:
            logger.error(f"Erro ao comprar ingresso: {e}")

            return response(
                "error",
                "Erro interno ao realizar compra."
            )
            

# ======================================================
# Registro no Name Server
# ======================================================

def register_in_name_server():
    """
    Registrar o serviço no Name Server para descoberta pelos clientes.
    Implementa mecanismo de retry e garante
    que a conexão seja encerrada corretamente, mesmo em caso de falhas.
    """
    
    max_retries = 5
    delay = 1
    
    for attempt in range(1, max_retries + 1):
        
        conn = None # Garantir que a conexão seja definida mesmo em caso de falha
        
        try:
            # Registrar o serviço no Name Server para descoberta pelos clientes
            
            # Conectar ao Name Server e registrar o serviço        
            conn = rpyc.connect(NAME_SERVER_HOST, NAME_SERVER_PORT)
            
            # Registrar o serviço com nome, host e porta do servidor principal
            conn.root.register(SERVICE_NAME, SERVER_HOST, SERVER_PORT)            
            
            logger.info("Servidor registrado no Name Server com sucesso.")
            return True
            
        except Exception as e:
            # Logar o erro para análise posterior
            logger.warning(f"Tentativa {attempt} de registro falhou. Erro: {e}")
            time.sleep(delay)
            
        finally:
            # Garantir que a conexão seja fechada corretamente
            if conn:
                try:
                    conn.close()
                except Exception:
                    pass
            
    logger.error(f"Erro ao registrar no Name Server.")
    return False
        
        
# ======================================================
# Inicialização do Servidor
# ======================================================

if __name__ == "__main__":
    """
    Inicializa o banco de dados, 
    registra o serviço no Name Server e inicia o servidor RPC.    
    """
    
    logger.info("===================================")
    logger.info("Iniciando Servidor do Cinema...")
    logger.info("===================================")
    
    try:
        # Inicializar o banco de dados (criar tabelas e inserir dados iniciais)
        
        database.start_db()
        logger.info("Banco de dados inicializado com sucesso.")
        
        # Registrar o serviço no Name Server para descoberta pelos clientes
        if not register_in_name_server():
            raise Exception("Falha ao registrar no Name Server. Verifique os logs para detalhes.")
        
        # Iniciar o servidor RPC para atender às requisições dos clientes
        server = ThreadedServer(
            CinemaService, 
            hostname=SERVER_HOST,
            port=SERVER_PORT, 
            reuse_addr=True,
            protocol_config={
                "allow_public_attrs": True,
                "allow_pickle": False,
                "sync_request_timeout": None
            }
        )
        
        logger.info("Servidor aguardando conexões...")
        server.start()
        
    except KeyboardInterrupt:
        # Logar a interrupção do servidor pelo usuário
        logger.info("Servidor interrompido pelo usuário.")
        
    except Exception as e:
        # Logar o erro para análise posterior
        logger.error(f"Falha ao iniciar o servidor: {e}")