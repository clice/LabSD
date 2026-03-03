import threading
from client.client_core import ClientCore


def buy_ticket_thread(results, index):
    core = ClientCore()
    core.connect()

    result = core.buy_tickets(
        f"User{index}",
        f"user{index}@mail.com",
        1,
        1
    )

    results.append(result)
    core.close()


def test_concurrent_buy():
    threads = []
    results = []

    for i in range(5):
        t = threading.Thread(
            target=buy_ticket_thread,
            args=(results, i)
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    success_count = sum(
        1 for r in results if r["status"] == "success"
    )

    assert success_count > 0