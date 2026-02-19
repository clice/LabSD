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
import logging
from config import NAME_SERVER_PORT, LOG_FORMAT


# ======================================================
# Configuração de Logging
# ======================================================

# Permite monitorar registro e consultas de serviços.
# Fundamental para depuração e observabilidade do sistema.
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


class NameService(rpyc.Service):
    """
    Classe que implementa o serviço de registro e descoberta.
    """
    
    # Registro de serviços
    registry = {}
    
    
    def exposed_register(self, service_name, host, port):
        """
        Permite que um servidor registre seu endereço.
        """

        NameService.registry[service_name] = (host, port)

        # Logar o registro para monitoramento
        logging.info(f"Serviço '{service_name}' registrado em {host}:{port}")

        return {
			"status": "success",
			"message": "Registro bem-sucedido"
		}


    def exposed_lookup(self, service_name):
        """
        Permite que o cliente descubra o endereco de servico.
        """
        
        if service_name in NameService.registry:
            # Logar a consulta para monitoramento
            logging.info(f"Consulta ao serviço '{service_name}'.")            
            return NameService.registry[service_name]
        
        # Logar o registro para monitoramento
        logging.warning(f"Serviço '{service_name}' não encontrado.")
        
        return None


# ======================================================
# Inicialização do Name Server
# ======================================================

if __name__ == "__main__":

	logging.info("==================================")
	logging.info("Name Server iniciado...")
	logging.info("==================================")

    # Iniciar o servidor de nomes
	server = ThreadedServer(NameService, port=NAME_SERVER_PORT)

	server.start()