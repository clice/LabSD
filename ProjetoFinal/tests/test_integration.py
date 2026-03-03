"""
test_integration.py

Testes de integração.

Valida se:
- Cliente consegue conectar
- Listagem de filmes funciona
- Compra de ingressos funciona
- Retornos estão no formato esperado
"""

from client.client_core import ClientCore


def test_list_movies():
    """
    Testa listagem de filmes via RPC.
    """
    
    core = ClientCore()
    assert core.connect()
    
    result = core.list_movies()
    
    assert result["status"] == "success"
    assert isinstance(result["data"], list)
    assert len(result["data"]) > 0
    
    core.close()
    

def test_buy_tickets_success():
    """
    Testa compra de ingresso válida.
    """
    
    core = ClientCore()
    assert core.connect()
    
    result = core.buy_tickets(
        "Teste",
        "teste@email.com",
        1,
        1
    )

    assert result["status"] == "success"
    assert "available_tickets" in result["data"]

    core.close()