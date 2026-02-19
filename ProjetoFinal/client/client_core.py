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
"""


import rpyc
from config import (
    NAME_SERVER_HOST,
    NAME_SERVER_PORT,
    SERVICE_NAME
)


class ClientCore:

    def __init__(self):
        self.conn = None
        
        
    def connect(self):
        """
        Conecta ao servidor via RPyC usando o Name Server para descoberta.
        """

        try:
            ns_conn = rpyc.connect(NAME_SERVER_HOST, NAME_SERVER_PORT)

            endereco = ns_conn.root.lookup(SERVICE_NAME)
            ns_conn.close()

            if not endereco:
                return False

            host, port = endereco
            self.conn = rpyc.connect(host, port)
            return True

        except Exception:
            return False
        
        
    def close(self):
        """
        Fecha conexão RPC.
        """
        
        if self.conn:
            self.conn.close()
            
            
    def listar_filmes(self):
        return self.conn.root.listar_filmes()
    

    def listar_sessoes_por_filme(self, filme_id):
        return self.conn.root.listar_sessoes_por_filme(filme_id)
    

    def comprar_ingresso(self, nome, email, sessao_id, quantidade):
        return self.conn.root.comprar_ingresso(nome, email, sessao_id, quantidade)
