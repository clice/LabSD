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
from config import (
    NAME_SERVER_HOST,
    NAME_SERVER_PORT,
    SERVICE_NAME
)


class ClientCore:

    def __init__(self):
        """
        Inicializa o cliente sem conexão ativa.
        """
        self.conn = None

        # Configurações de Retry
        self.max_retries = 3
        self.retry_delay = 1  # segundos
        
    
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
            endereco = ns_conn.root.lookup(SERVICE_NAME)
            ns_conn.close()

            if not endereco:
                return False

            # Conectar ao servidor real
            host, port = endereco
            self.conn = rpyc.connect(host, port)
            return True

        except Exception:
            self.conn = None
            return False
        
        
    def close(self):
        """
        Fecha conexão RPC.
        """
        
        if self.conn:
            self.conn.close()
            self.conn = None

    
    # ==================================================
    # Método Interno de Retry
    # ==================================================

    def _retry_call(self, method_name, *args):
        """
        Executa chamada RPC com mecanismo de retry,
        implementando tolerância a falhas.
        """

        for tentativa in range(1, self.max_retries + 1):

            try:
                # Se a conexão não existir, tenta conectar
                if not self.conn:
                    if not self.connect():
                        raise Exception("Falha ao conectar")

                # Recuperar método dinamicamente
                method = getattr(self.conn.root, method_name)

                return method(*args)

            except Exception:

                # Fecha conexão antiga
                if self.conn:
                    try:
                        self.conn.close()
                    except:
                        pass

                    self.conn = None

                # Realiza as tentativas de conexão com o servidor
                if tentativa < self.max_retries:
                    print(
                        f"Falha na tentativa {tentativa}. "
                        f"Tentando novamente..."
                    )
                    time.sleep(self.retry_delay)

                else:
                    return {
                        "status": "error",
                        "message": "Servidor indisponível após múltiplas tentativas.",
                        "data": None
                    }


    # ==================================================
    # Operações Remotas
    # ==================================================            
            
    def listar_filmes(self):
        return self._retry_call("listar_filmes")
    

    def listar_sessoes_por_filme(self, filme_id):
        return self._retry_call("listar_sessoes_por_filme", filme_id)
    

    def comprar_ingresso(self, nome, email, sessao_id, quantidade):
        return self._retry_call("comprar_ingresso", nome, email, sessao_id, quantidade)
