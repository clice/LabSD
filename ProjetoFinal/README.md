# 🎟️ Sistema Distribuído de Compras de Ingressos

Projeto desenvolvido para a disciplina de **Sistemas Distribuídos**.

## 📖 Objetivo


Implementa uma aplicação distribuída para compra de ingressos de cinema, utilizando RPC, arquitetura em camadas, persistência durável e mecanismos de tolerância a falhas. Demonstrando:

- Comunicação entre múltiplos nós
- Gerenciamento de estado compartilhado
- Aplicação de transparências (acesso, localização e falhas)
- Concorrência no servidor
- Uso de RPC como middleware

---

## 🏗️ Arquitetura do Sistema

A aplicação segue o modelo **N-Camadas**:

O sistema é dividido em componentes independentes:

    Cliente (client_test)  
                ⬇  
    ClientCore (abstração RPC + Retry)  
                ⬇  
    Name Server (Descoberta de Serviço)  
                ⬇  
    Servidor RPC (Lógica de Negócio)  
                ⬇  
    SQLite (Persistência)

### 🔹 Camada de Apresentação (Cliente)
- Interface em terminal
- Não gerencia sockets diretamente
- Comunicação via RPC (RPyC)

### 🔹 Camada de Negócio (Servidor)
- Processa reservas
- Controla concorrência
- Gerencia estado compartilhado

### 🔹 Camada de Persistência
- Estado mantido em memória (quantidade de ingressos disponíveis)

---

## 📡 Comunicação e Middleware

O sistema utiliza **RPC (Remote Procedure Call)** por meio da biblioteca:

👉 `RPyC (Remote Python Call)`

O cliente realiza chamadas remotas como se fossem funções locais:

```python
conn.root.reservar_ingresso("Cliente", 2)
```

Sem necessidade de manipular sockets diretamente.

---

## 🔐 Concorrência e Sincronização

O servidor é multithreaded, permitindo múltiplos clientes simultaneamente.

Para evitar condições de corrida no recurso compartilhado (ingressos), foi utilizada:

```python
threading.Lock()
```

Isso garante exclusão mútua durante as operações de reserva.

---

## 🌍 Transparências Implementadas

✔ Transparência de Acesso

O cliente chama métodos remotos como se fossem locais.

✔ Transparência de Localização (quando implementado o Nó de Nomes)

O cliente descobre dinamicamente o servidor.

✔ Transparência de Falhas (quando implementado retry/circuit breaker)

O cliente trata falhas automaticamente.

---

## ⚙️ Requisitos

 - Python 3.8+
 - RPyC

---

## 📦 Instalação

### 🔹 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/nome-do-repo.git
cd nome-do-repo
```

### 🔹 2. Criar ambiente virtual (Recomendado)

Linux/Mac:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 🔹 3. Instalar dependências

```bash
pip install rpyc
```

---

## ▶️ Como Executar

### 🔹 1. Iniciar o Servidor

```bash
python server.py
```

Saída esperada:

```bash
Servidor de Ingressos iniciado...
```

### 🔹 2. Executar o Cliente

```bash
python client.py
```

---

## 🧪 Testes

 - Execute múltiplos clientes simultaneamente.
 - Tente reservar mais ingressos do que o disponível.
 - Observe o comportamento concorrente.
 - Teste falhas interrompendo o servidor.

---

## 📂 Estrutura do Projeto

    ProjetoFinal/
    ├── server.py
    ├── database.py
    ├── name_server.py
    ├── client_core.py
    ├── circuit_breaker.py
    ├── gui.py
    ├── tickets.db (gerado automaticamente)
    ├── README.md
    └── slides.pptx

---

## 🚀 Funcionalidades

 - Consultar ingressos disponíveis
 - Reservar ingressos
 - Ver status do servidor
 - Controle de concorrência
 - Comunicação RPC

---

## 🎓 Conceitos de Sistemas Distribuídos Aplicados

 - RPC / Middleware
 - Arquitetura em N-Camadas
 - Concorrência
 - Exclusão Mútua
 - Estado Compartilhado
 - Transparência de Acesso
 - Transparência de Falhas
 - Descoberta de Serviço (opcional)