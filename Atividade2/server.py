import rpyc
from rpyc.utils.server import ThreadedServer
from datetime import datetime

# Classe de serviço que define os métodos remotos que o cliente pode chamar, usando RPC
class ServicoHorario(rpyc.Service):

    def exposed_get_horario(self): # Métodos que começam com "exposed_" são expostos como métodos remotos que o cliente pode chamar.
        """
        Método remoto que será chamado pelo cliente.
        """
        agora = datetime.now()
        return agora.strftime("%d/%m/%Y %H:%M:%S")


if __name__ == "__main__":
    print("Servidor RPC iniciado...")
    servidor = ThreadedServer(ServicoHorario, port=18861) # Permite que o servidor atenda a múltiplas conexões simultâneas usando threads.
    servidor.start()
