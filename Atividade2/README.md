# 🖥️ Atividade de Laboratório 2 - Modelo Cliente/Servidor Baseado em RPC (Remote Procedure Call) Usando RPyC

## 📚 Disciplina: Sistemas Distribuídos

Este projeto é a continuação da Atividade 1 (Consulta de Horário com Sockets), agora implementado utilizando o modelo **RPC (Remote Procedure Call)** com a biblioteca **RPyC (Remote Python Call)**.

---

## 🎯 Objetivo

Implementar um sistema cliente/servidor utilizando RPC em Python, onde:

- O servidor disponibiliza um método remoto para retornar o horário atual.
- O cliente solicita o horário ao servidor.
- O cliente exibe o horário recebido.
- A conexão é encerrada após a resposta.

---

## 🧠 Conceito Teórico

### 🔹 O que é RPC?

RPC (Remote Procedure Call) é um modelo de comunicação onde um programa pode chamar uma função que está sendo executada em outro processo ou máquina, como se fosse uma função local.

Nesse modelo:
- O cliente chama um método remoto.
- O servidor executa o método.
- O resultado é retornado ao cliente.

### 🔹 O que é RPyC?

RPyC (Remote Python Call) é uma biblioteca Python que implementa RPC, permitindo chamadas remotas de métodos de forma simples e transparente.

---

## ⚙️ Instalação do RPyC (Linux Ubuntu/Debian)

É necessário ter o Python instalado e a melhor forma é utilizando uma ambiente virtual para instalação das dependências e bibliotecas necessárias. 

```
python3 -m venv venv       # Preparação do ambiente virtual
source venv/bin/activate   # Ativação do ambiente virtual
pip install rpyc           # Instalação da biblioteca RPyC

```

---

## 🏗️ Estrutura do Projeto

    📁 Atividade2/
    │
    ├── venv/
    ├── client.py
    ├── server.py
    ├── Atividade de Laboratório 2.pdf
    └── README.md

---

## 🖥️ Implementação

### 🔹 Servidor (servidor.py)

O servidor define um serviço que expõe o método remoto get_horario().

Esse método:
 - Obtém o horário atual do sistema;
 - Retorna a data e hora formatadas; e
 - O servidor fica aguardando conexões na porta 18861.

### 🔹 Cliente (cliente.py)

O cliente:
 - Conecta ao servidor;
 - Chama o método remoto get_horario();
 - Exibe o horário recebido; e
 - Encerra a conexão.

---

## ▶️ Como Executar

É necessário que dois terminais sejam abertos e ativados, um será onde o servidor (server.py) será executado e outro para a execução do cliente (client.py).

### 1️⃣ Ativar o ambiente virtual

```
source venv/bin/activate
```

### 2️⃣ Iniciar o Servidor

```
python servidor.py
```

#### Saída esperada

```
Servidor RPC iniciado...
```

### 3️⃣ Executar o Cliente

Em outro terminal (também com o venv ativado):

```
source venv/bin/activate
python cliente.py
```

#### Saída esperada:

Exemplo:

```
Conectando ao servidor...
Horário recebido do servidor: 14/02/2026 19:30:45
Conexão encerrada.
```