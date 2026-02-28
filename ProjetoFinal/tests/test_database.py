import unittest
from core import database


class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        database.inicializar_banco()

    def test_listar_filmes(self):
        filmes = database.listar_filmes()
        self.assertTrue(len(filmes) > 0)

    def test_compra_invalida(self):
        resposta = database.comprar_ingresso(
            "Teste",
            "teste@email.com",
            9999,
            1
        )
        self.assertEqual(resposta["status"], "error")


if __name__ == "__main__":
    unittest.main()