"""
name_server.py

Nó de Nomes (Service Discovery) da aplicação distribuída.

Responsável por:
✔ Registrar serviços disponíveis
✔ Permitir que clientes descubram dinamicamente os serviços
✔ Implementar transparência de localização

Este componente é um nó independente do sistema distribuído.
Ele funciona como um "registro central" de serviços.
"""

import rpyc
from rpyc.utils.server import ThreadedServer


class NameService(rpyc.Service):
    """
    Classe que implementa o serviço de registro e descoberta.

    Atua como um diretório central de serviços.

    Estrutura de registro:
        {
            "nome_servico": (host, porta)
        }

    Demonstra:
    ✔ Descoberta de Serviço
    ✔ Transparência de Localização
    ✔ Arquitetura distribuída com múltiplos nós
    """

    # ==========================================
    # Estrutura de armazenamento dos serviços
    # ==========================================

    registry = {}

    # ==================================================
    # Método Remoto: Registrar Serviço
    # ==================================================

    def exposed_register(self, service_name, host, port):
        """
        Permite que um servidor registre seu serviço.

        Parâmetros:
        - service_name: Nome lógico do serviço
        - host: Endereço IP ou hostname
        - port: Porta onde o serviço está rodando

        Este método é chamado pelo servidor de reservas
        durante sua inicialização.

        Demonstra:
        ✔ Registro dinâmico de serviços
        ✔ Interação entre múltiplos nós
        """

        NameService.registry[service_name] = (host, port)

        print(f"[REGISTRO] Serviço '{service_name}' "
              f"registrado em {host}:{port}")

        return "Serviço registrado com sucesso."

    # ==================================================
    # Método Remoto: Descobrir Serviço
    # ==================================================

    def exposed_lookup(self, service_name):
        """
        Permite que clientes descubram a localização de um serviço.

        Parâmetro:
        - service_name: Nome lógico do serviço

        Retorna:
        - (host, port) se encontrado
        - None se não existir

        Demonstra:
        ✔ Transparência de localização
        ✔ Desacoplamento entre cliente e servidor
        """

        if service_name in NameService.registry:

            print(f"[CONSULTA] Cliente consultou "
                  f"o serviço '{service_name}'")

            return NameService.registry[service_name]

        else:
            print(f"[ERRO] Serviço '{service_name}' não encontrado.")
            return None


# ======================================================
# Inicialização do Name Server
# ======================================================

if __name__ == "__main__":
    """
    Ponto de entrada do Nó de Nomes.

    Utiliza ThreadedServer para permitir múltiplas
    consultas simultâneas.

    Deve ser iniciado antes do servidor principal.
    """

    print("===================================")
    print(" Nó de Nomes iniciado")
    print(" Aguardando registros e consultas...")
    print("===================================")

    server = ThreadedServer(
        NameService,
        port=18862
    )

    server.start()
