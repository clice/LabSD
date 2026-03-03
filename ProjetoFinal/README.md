# Sistema Distribuído de Compras de Ingressos

Projeto final desenvolvido para a disciplina de **Sistemas Distribuídos**.

## Descrição do Projeto


Este projeto implementa um sistema distribuído cliente-servidor para simulação de compra de ingressos de cinema.

O sistema permite que múltiplos clientes consultem filmes disponíveis e realizem compras simultaneamente, garantindo:

- Comunicação remota via RPC
- Descoberta de serviços via Name Server
- Controle de concorrência
- Tolerância a falhas
- Testes automatizados
- Interface CLI e GUI

O objetivo é aplicar conceitos fundamentais de Sistemas Distribuídos, como:

- Comunicação remota
- Descoberta de serviços
- Sincronização
- Resiliência
- Tratamento de falhas

---

## Estrutura do Projeto

    ProjetoFinal/
    │
    ├── client/
    │   ├── client_core.py
    │   ├── circuit_breaker.py
    │   └── cli.py
    │
    ├── core/
    │   ├── server.py
    │   ├── name_server.py
    │   └── database.py
    │
    ├── data/
    │   └── ...
    │
    ├── docs/
    │   └── ...
    │
    ├── gui/
    │   └── ...
    │
    ├── scripts/
    │   ├── run.py
    │   ├── run_gui.py
    │   └── run_tests.py
    │
    ├── tests/
    │   ├── conftest.py
    │   ├── test_concurrency.py
    │   ├── test_failure.py
    │   └── test_integration.py
    │
    ├── config.py
    └── requirements.txt

---

## Como Executar o Projeto

### Instalar dependências

* Linux/Mac:

```bash
python3 -m venv venv
source .venv/bin/activate
pip install -r requirements.txt
```

* Windows:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Executar projeto

Existem duas formar de executar o projeto:

- Executar via CLI

```bash
# Linux/Mac:
python3 scripts/run.py

# Windows
python scripts/run.py
```

- Executar via GUI

```bash
# Linux/Mac:
python3 scripts/run_gui.py

# Windows
python scripts/run_gui.py
```

---

## Tecnologias Utilizadas

- Python 3.x
- RPyC
- Pytest
- Threading
- Tkinter (GUI)

---

## Arquitetura do Sistema

O sistema é composto pelos seguintes componentes:

### Name Server

Responsável por registrar e fornecer a localização do servidor para os clientes.

- Permite desacoplamento entre cliente e servidor
- Facilita escalabilidade futura
- Evita dependência de endereço fixo

Arquivo: `core/name_server.py`

### Servidor

Responsável por:

- Gerenciar os filmes disponíveis
- Processar compras
- Controlar concorrência
- Garantir consistência dos dados
- Responder requisições remotas via RPC

Arquivo: `core/server.py`

### Banco de Dados (Em Memória)

Simula um banco de dados para armazenar:

- Lista de filmes
- Quantidade de ingressos disponíveis
- Histórico de compras

Arquivo: `core/database.py`

### Cliente

Responsável por:

- Consultar o Name Server
- Conectar-se ao servidor
- Realizar requisições remotas
- Interagir com o usuário

Componentes:

- CLI: `client/cli.py`
- Núcleo do cliente: `client/client_core.py`
- Interface gráfica: `gui/`

---

## Componentes do Sistema

### Name Server
Responsável por registrar e fornecer a localização dos serviços disponíveis.

Arquivo: `core/name_server.py`

### Servidor
Responsável por:
- Gerenciar filmes
- Processar compras
- Controlar concorrência
- Persistir dados

Arquivo: `core/server.py`

### Banco de Dados
Simulação de banco em memória para armazenar:
- Filmes
- Ingressos disponíveis
- Compras realizadas

Arquivo: `core/database.py`

### Cliente
- Interface CLI (`client/cli.py`)
- Interface gráfica (`gui/`)
- Comunicação com servidor via RPC

### Circuit Breaker
Implementado para tolerância a falhas.
Arquivo: `client/circuit_breaker.py`

---

## Comunicação e Middleware

O sistema utiliza **RPC (Remote Procedure Call)** por meio da biblioteca `RPyC (Remote Python Call)` no Python. O cliente realiza chamadas remotas pelo como se fossem funções locais, sem a necessidade de manipular sockets diretamente e consulta o Name Server antes de se conectar ao servidos.

---

## Concorrência e Sincronização

O servidor é multithreaded, permitindo múltiplos clientes simultaneamente. Para evitar condições de corrida no recurso compartilhado (ingressos). Foi utilizada o lock threading, o que garante exclusão mútua durante as operações de reserva e previne venda duplicada.

---

## Tolerância a Falhas

Para garantir resiliência em ambiente distribuído, foi implementado o padrão Circuit Breaker no cliente.

O Circuit Breaker impede que o cliente continue realizando chamadas remotas quando o servidor apresenta falhas consecutivas, evitando sobrecarga e melhorando a estabilidade do sistema.

O mecanismo opera com três estados:

- **Closed**: funcionamento normal
- **Open**: bloqueio temporário de requisições após número limite de falhas
- **Half-Open**: estado intermediário para testar recuperação do servidor

Essa abordagem permite que o sistema:
- Evite tentativas desnecessárias de conexão
- Reduza impacto de falhas temporárias
- Recupere-se automaticamente quando o servidor voltar ao funcionamento

Os testes de falha estão implementados em `tests/test_failure.py`.
