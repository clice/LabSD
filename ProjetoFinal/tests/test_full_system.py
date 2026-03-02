import unittest
import subprocess
import time
import sys
from client.client_core import ClientCore


class TestFullSystem(unittest.TestCase):
    
    
    @classmethod
    def setUpClass(cls):
        
        python_exec = sys.executable
        
        # Iniciar Name Server
        cls.name_server = subprocess.Popen(
            [python_exec, "-m", "core.name_server"]
        )
        
        time.sleep(2)
        
        # Iniciar servidor
        cls.server = subprocess.Popen(
            [python_exec, "-m", "core.server"]
        )
        
        time.sleep(2)
        
        # Criar cliente
        cls.core = ClientCore()
        
        if not cls.core.connect():
            raise Exception("Falha ao conectar ao sistema.")
        
    @classmethod
    def tearDownClass(cls):
        
        cls.core.close()
        
        cls.server.terminate()
        cls.name_server.terminate()
        
    # ---------------------------------------
    # Testes reais de sistema
    # ---------------------------------------
    
    def test_list_movies(self):
        result = self.core.list_movies()
        self.assertEqual(result["status"], "success")
        
    def test_buy_tickets(self):
        result = self.core.buy_tickets("Teste", "teste@email.com", 1, 1)
        self.assertIn(result["status"], ["success", "error"])
        
    def test_retry_with_server_down(self):
        
        # Desligar servidor
        self.server.terminate()
        time.sleep(1)
        
        # Tentar listar filmes (deve falhar)
        result = self.core.list_movies()
        
        self.assertEqual(result["status"], "error")
        
        
if __name__ == "__main__":
    unittest.main()