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
    
    def test_listar_filmes(self):
        resposta = self.core.listar_filmes()
        self.assertEqual(resposta["status"], "success")
        
    def test_comprar_ingresso(self):
        resposta = self.core.comprar_ingresso("Teste", "teste@email.com", 1, 1)
        self.assertIn(resposta["status"], ["success", "error"])
        
    def test_retry_com_servidor_off(self):
        
        # Desligar servidor
        self.server.terminate()
        time.sleep(1)
        
        # Tentar listar filmes (deve falhar)
        resposta = self.core.listar_filmes()
        
        self.assertEqual(resposta["status"], "error")
        
        
if __name__ == "__main__":
    unittest.main()