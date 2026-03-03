from client.client_core import ClientCore


def test_list_movies():
    core = ClientCore()
    assert core.connect()
    
    result = core.list_movies()
    
    assert result["status"] == "success"
    assert isinstance(result["data"], list)
    assert len(result["data"]) > 0
    
    core.close()
    

def test_buy_tickets_success():
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