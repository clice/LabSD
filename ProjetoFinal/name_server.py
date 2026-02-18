"""
name_server.py

Nó de Nomes (Service Discovery) da aplicação distribuída.

- Registrar serviços disponíveis
- Permitir que clientes descubram dinamicamente os serviços
- Implementar transparência de localização

Este componente é um nó independente do sistema distribuído.
Ele funciona como um "registro central" de serviços.
"""


import rpyc
from rpyc.utils.server import ThreadedServer
import logging


# Configuração de logging para monitoramento e depuração
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


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
        logging.info(
            f"Serviço '{service_name}' registrado "
            f"em {host}:{port}"
        )

        return "Serviço registrado com sucesso."
    

    def exposed_lookup(self, service_name):
        """
        Permite que cliente descubra o endereço do serviço.
        """

        if service_name in NameService.registry:
            
            # Logar a consulta para monitoramento
            logging.info(
                f"Consulta ao serviço '{service_name}'."
            )

            return NameService.registry[service_name]

        logging.warning(
            f"Serviço '{service_name}' não encontrado."
        )

        return None
        

if __name__ == "__main__":

    logging.info("===================================")
    logging.info("Name Server iniciado")
    logging.info("===================================")

    server = ThreadedServer(
        NameService,
        port=18862
    )

    server.start()