"""
server.py

Servidor da aplicação distribuída de reservas de ingressos.

Este servidor implementa:
- Comunicação via RPC utilizando RPyC (middleware)
- Arquitetura N-Camadas (Camada de Negócio)
- Concorrência (ThreadedServer)
- Estado compartilhado
- Exclusão mútua para evitar condição de corrida

O servidor expõe métodos que podem ser chamados remotamente
pelos clientes como se fossem funções locais.
"""

import rpyc
from rpyc.utils.server import ThreadedServer
import threading
from datetime import datetime

class TicketService(rpyc.Service):
    # Classe que define os métodos remotos disponíveis aos clientes.
    # Esta classe representa a Camada de Lógica de Negócio
    # dentro da arquitetura em N-Camadas.

    # Quantidade inicial de ingressos disponíveis
    ingressos_disponiveis = 10

    # Lock para garantir exclusão mútua
    lock = threading.Lock()


    def exposed_consultar_ingressos(self):
        # Consultar ingressos disponíveis
        # Retorna a quantidade de ingressos disponíveis.
        # O prefixo 'exposed_' indica que o método pode
        # ser chamado remotamente via RPC.
        # Transparência de acesso e estado compartilhado
        
        return TicketService.ingressos_disponiveis
    

    def exposed_reservar_ingresso(self, nome_cliente, quantidade):
        # Reservar ingresso
        # Para evitar condição de corrida (race condition),
        # utilizamos exclusão mútua com Lock.
        # Concorrência, exclusão mútua e gerenciamento de recurso compartilhado
        
        with TicketService.lock:
            
            if TicketService.ingressos_disponiveis >= quantidade:
                TicketService.ingressos_disponiveis -= quantidade

                return (
                    f"Reserva confirmada para {nome_cliente}. "
                    f"{quantidade} ingresso(s) reservado(s)."
                )

            else:
                return "Ingressos insuficientes."


    def exposed_status_servidor(self):
        # Status do Servidor
        # Retorna informações sobre o estado atual do servidor.
        # Compartilhamento de estado e capacidade de monitoramento
        
        return {
            "horario": str(datetime.now()),
            "ingressos_restantes":
                TicketService.ingressos_disponiveis
        }
        

if __name__ == "__main__":
    # Inicialização do Servidor
    # Ponto de entrada do servidor.
    # Utiliza ThreadedServer para permitir múltiplos clientes
    # simultaneamente (modelo multithread).
    # Concorrência no servidor e capacidade de atender múltiplos nós
    
    print("Servidor de Ingressos iniciado...")
    print("Aguardando conexões...")

    # ThreadedServer permite múltiplas conexões simultâneas
    server = ThreadedServer(
        TicketService,
        port=18861
    )

    server.start()
