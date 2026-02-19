import rpyc
from config import (
    NAME_SERVER_HOST,
    NAME_SERVER_PORT,
    SERVICE_NAME
)


class ClientCore:

    def __init__(self):
        self.conn = None

    def conectar(self):

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

    def listar_filmes(self):
        return self.conn.root.listar_filmes()

    def listar_sessoes(self, filme_id):
        return self.conn.root.listar_sessoes(filme_id)

    def comprar_ingresso(self, nome, email, sessao_id, quantidade):
        return self.conn.root.comprar_ingresso(
            nome, email, sessao_id, quantidade
        )
