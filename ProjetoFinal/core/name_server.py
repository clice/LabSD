"""
name_server.py

Nó de Nomes (Name Server) da aplicação distribuída.

Este componente implementa o mecanismo de Service Discovery,
permitindo que:

- Servidores registrem seus serviços dinamicamente
- Clientes descubram serviços sem conhecer endereço fixo
- Seja implementada transparência de localização

Em um Sistema Distribuído, o Name Server desacopla cliente e servidor,
evitando que o cliente precise saber previamente onde o serviço está
rodando (IP/porta). É um nó independente do sistema distribuído.
Ele funciona como um "registro central" de serviços.
"""


import rpyc
from rpyc.utils.server import ThreadedServer
import threading
from config import NAME_SERVER_PORT
from core.color_logger import setup_logger


# ======================================================
# Configuração de Logger
# ======================================================

# Permite monitorar registro e consultas de serviços.
# Fundamental para depuração e observabilidade do sistema.
logger = setup_logger("NameServer")


class NameService(rpyc.Service):
    """
    Classe que implementa o serviço de registro e descoberta.
    """
    
    # Registro de serviços
    registry = {}
    lock = threading.Lock()  # Para proteger acesso concorrente ao registro
    
    def exposed_register(self, service_name, host, port):
        """
        Permite que um servidor registre seu endereço.
        """

        with NameService.lock:
            NameService.registry[service_name] = (host, port)

        # Logar o registro para monitoramento
        logger.info(f"Serviço '{service_name}' registrado em {host}:{port}")

        return {
			"status": "success",
			"message": "Registro bem-sucedido"
		}


    def exposed_lookup(self, service_name):
        """
        Permite que o cliente descubra o endereco de servico.
        """
        
        with NameService.lock:
            address = NameService.registry.get(service_name)
        
        if address:
            # Logar a consulta para monitoramento
            logger.info(f"Consulta ao serviço '{service_name}'.")            
            return address
        
        # Logar o registro para monitoramento
        logger.warning(f"Serviço '{service_name}' não encontrado.")
        
        return None


# ======================================================
# Inicialização do Name Server
# ======================================================

if __name__ == "__main__":
    
    logger.info("==================================")
    logger.info("Name Server iniciando...")
    logger.info("==================================")
    
    # Iniciar o servidor de nomes para atender às requisições de registro e consulta
    server = ThreadedServer(
        NameService,
        hostname="0.0.0.0",
        port=NAME_SERVER_PORT,
        reuse_addr=True
    )
    
    server.start()