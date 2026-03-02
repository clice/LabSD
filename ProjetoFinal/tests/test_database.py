import unittest
from core import database


class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        database.start_db()

    def test_list_movies(self):
        movies = database.list_movies()
        self.assertTrue(len(movies) > 0)

    def test_buy_invalid(self):
        result = database.buy_tickets(
            "Teste",
            "teste@email.com",
            9999,
            1
        )
        self.assertEqual(result["status"], "error")


if __name__ == "__main__":
    unittest.main()