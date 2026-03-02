"""
test_integration.py

Testes automatizados de integração 
para o Sistema Distribuído de Cinema

Testar:
- Conexão
- Listagem
- Compra
- Tratamento de erro
"""

import unittest
import time
from client.client_core import ClientCore


class TestCinemaSystem(unittest.TestCase):


	@classmethod
	def setUpClass(cls):
		"""
		Executado uma vez antes dos testes.
		"""

		cls.core = ClientCore()

		connected = cls.core.connect()

		if not connected:
			raise Exception("Servidor não está rodando.")


	@classmethod
	def tearDownClass(cls):
		"""
		Executado após todos os testes.
		"""

		cls.core.close()
	
	
	# ---------------------------------------
    # Teste de Conexão
    # ---------------------------------------
    
    def test_connection(self):
        self.assertIsNotNone(self.core.conn)


    # ---------------------------------------
    # Teste Listar Filmes
    # ---------------------------------------

    def test_listar_filmes(self):
    	resposta = self.core.listar_filmes()
    	self.assertEqual(resposta["status"], "success")
    	self.assertTrue(len(resposta["data"]) > 0)


    # ---------------------------------------
    # Teste Listar Sessões
    # ---------------------------------------

    def test_listar_sessoes_por_filme(self):
    	resposta = self.core.listar_sessoes_por_filme(1)
    	self.assertEqual(resposta["status"], "success")
    	self.assertTrue(len(resposta["data"]) > 0)


    # ---------------------------------------
    # Teste Compra Válida
    # ---------------------------------------

    def test_compra_valida(self):
    	resposta = self.core.comprar_ingresso("Teste", "teste@email.com", 1, 1)
    	self.assertIn(resposta["status"], ["success", "error"])


    # ---------------------------------------
    # Teste Compra Inválida
    # ---------------------------------------

    def test_compra_invalida(self):
    	resposta = self.core.comprar_ingresso("Teste", "teste@email.com", 9999, 1)
    	self.assertEqual(resposta["status"], "error")


if __name__ == "__main__":
	unittest.main()