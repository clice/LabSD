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


4. COMO SUBIR NO GITHUB (SIMPLIFICADO)
	1.	Crie uma pasta:

mkdir socket-projeto
cd socket-projeto

	2.	Coloque os arquivos:

server.py
client.py

	3.	Inicie o repositório:

git init
git add .
git commit -m "Projeto cliente/servidor socket"

	4.	Crie um repositório no GitHub e depois:

git remote add origin https://github.com/SEU_USUARIO/socket-projeto.git
git push -u origin main