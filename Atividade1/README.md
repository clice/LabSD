# 🧮 Atividade 1 - Modelo Cliente/Servidor com Sockets em Python

- O servidor deve atender um único pedido do cliente: Retornar o horário do momento
solicitado. O cliente deve solicitar o horário ao servidor e encerrar. O servidor deve
ser multithread.
- O servidor deve escutar em uma porta específica (ex: 8000). Quando recebe uma
string, ele a reverte e a envia de volta. O cliente que se conecta ao servidor, envia
uma string ("Olá Mundo Distribuído") e espera a resposta.

---

## 📁 Estrutura

Atividade1/

	├── Atividade de Laboratório 1.pdf
	├── client.py
	├── README.md
	└── server.py

---

## ▶️ Como executar

```bash
python3 server.py  # Executar o código do servidor
python3 client.py  # Ao mesmo tempo também executar o do cliente
```