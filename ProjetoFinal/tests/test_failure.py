"""
test_failure.py

Testes de falha e validação de entrada.

Valida se o servidor trata entradas inválidas corretamente.
"""

from client.client_core import ClientCore


def test_invalid_movie_id():
    """
    Envia ID inválido (string) para método que exige inteiro.
    """
    
    core = ClientCore()
    core.connect()

    result = core.list_screenings_by_movie("abc")

    assert result["status"] == "error"

    core.close()