"""
client_core.py

Camada intermediária entre interface (GUI ou terminal)
e servidor RPC.

Esta classe encapsula toda a comunicação RPC,
garantindo que a interface NÃO precise conhecer:

- Gerencia conexão com o servidor
- Fornece métodos para operações de listagem e compra
- Abstrai detalhes de comunicação RPC do cliente
- Encapsular chamadas remotas
- Implementação de Retry automático (Tolerância a Falhas)
"""


import rpyc
import time
from config import NAME_SERVER_HOST, NAME_SERVER_PORT, SERVICE_NAME
from client.circuit_breaker import CircuitBreaker


class ClientCore:

    def __init__(self):
        """
        Inicializa o cliente sem conexão ativa.
        """
        self.conn = None

        # Configurações de Retry
        self.max_retries = 3
        self.retry_delay = 1  # segundos
        
        # 
        self.breaker = CircuitBreaker(
            failure_threshold=3,
            recovery_timeout=5
        )
        
    
    # ==================================================
    # Controles de conexão via Name Server
    # ==================================================    
        
    def connect(self):
        """
        Conecta ao servidor via RPyC usando o Name Server para descoberta.
        """

        try:
            # Fecha conexão anterior se existir
            if self.conn:
                self.conn.close()
                self.conn = None

            # Conectar ao Name Server
            ns_conn = rpyc.connect(NAME_SERVER_HOST, NAME_SERVER_PORT)
            address = ns_conn.root.lookup(SERVICE_NAME)
            
            if not address:
                return False

            # Conectar ao servidor real
            host, port = address
            self.conn = rpyc.connect(host, port)
            return True

        except Exception as e:
            print(f"Erro ao conectar: {e}")
            self.conn = None
            return False
        
        finally:
            # Garantir que a conexão com o Name Server seja fechada
            if ns_conn:
                try:
                    ns_conn.close()
                except Exception:
                    pass
        
        
    def close(self):
        """
        Fecha conexão RPC ativa.
        """
        
        if self.conn:
            try:
                self.conn.close()
            except Exception:
                pass
            finally:
                self.conn = None           

    
    # ==================================================
    # Método Interno com Retry
    # ==================================================

    def _retry_call(self, method_name, *args):
        """
        Executa chamada RPC combinando retry automático e Circuit Breaker,
        implementando tolerância a falhas, verificando o estado do circuito,
        executando chamadas com retry e depois atualizando o estado do circuito.
        """
        
        # Verifica o estado do circuito
        try:
            # Verifica se o circuito permite chamada
            self.breaker.before_call()
            
        except Exception as e:
            # Circuito aberto -> bloqueia imediatamente
            return {
                "status": "erro",
                "message": str(e),
                "data": None
            }

        # Executa retry apenas se circuito permitir
        for retry in range(1, self.max_retries + 1):

            try:
                # Se a conexão não existir, tenta conectar
                if not self.conn:
                    if not self.connect():
                        raise Exception("Falha ao conectar ao servidor")

                # Recuperar método dinamicamente
                method = getattr(self.conn.root, method_name)
                result = method(*args)
                
                # Se chegou aqui, circuito foi bem sucedido
                self.breaker.on_success()

                # Forçar materialização simples sem pickle
                if isinstance(result, dict):
                    return {k: v for k, v in result.items()}

                return result

            except Exception as e:
                print(f"Falha na tentativa {retry}. Erro: {e}")

                # Fecha conexão antiga
                if self.conn:
                    try:
                        self.conn.close()
                    except Exception:
                        pass
                    finally:
                        self.conn = None

                # Realiza as tentativas de conexão com o servidor
                if retry < self.max_retries:
                    # Aguarda antes de nova tentativa
                    time.sleep(self.retry_delay)
                else:
                    # Falha definitiva, registra falha
                    self.breaker.on_failure()
                    
                    return {
                        "status": "error",
                        "message": "Servidor indisponível após múltiplas tentativas.",
                        "data": None
                    }


    # ==================================================
    # Operações Remotas
    # ==================================================            
            
    def list_movies(self):
        return self._retry_call("list_movies")
    

    def list_screenings_by_movie(self, movie_id):
        return self._retry_call("list_screenings_by_movie", movie_id)
    

    def buy_tickets(self, nome, email, screening_id, quantity):
        return self._retry_call("buy_tickets", nome, email, screening_id, quantity)
