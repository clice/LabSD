import rpyc
from rpyc.utils.server import ThreadedServer
import threading
from datetime import datetime

class TicketService(rpyc.Service):

    # Estado compartilhado entre todos os clientes
    ingressos_disponiveis = 10
    lock = threading.Lock()

    def exposed_consultar_ingressos(self):
        return TicketService.ingressos_disponiveis

    def exposed_reservar_ingresso(self, nome_cliente, quantidade):
        with TicketService.lock:  # Exclusão mútua
            if TicketService.ingressos_disponiveis >= quantidade:
                TicketService.ingressos_disponiveis -= quantidade
                return f"Reserva confirmada para {nome_cliente}. {quantidade} ingresso(s) reservado(s)."
            else:
                return "Ingressos insuficientes."

    def exposed_status_servidor(self):
        return {
            "horario": str(datetime.now()),
            "ingressos_restantes": TicketService.ingressos_disponiveis
        }

if __name__ == "__main__":
    print("Servidor de Ingressos iniciado...")
    server = ThreadedServer(TicketService, port=18861)
    server.start()
