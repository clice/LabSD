"""
circuit_breaker.py

Implementação do padrão Circuit Breaker para tolerância a falhas.

Protege chamadas remotas evitando sobrecarga quando
o servidor está indisponível.
"""

import time


class CircuitBreaker:
    """
    Implementação simples do padrão Circuit Breaker.

    Estados:
    - CLOSED: funcionamento normal
    - OPEN: bloqueia chamadas após muitas falhas
    - HALF-OPEN: testa se o servidor voltou
    """

    def __init__(self, failure_threshold=3, recovery_timeout=5):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout

        self.failure_count = 0
        self.state = "CLOSED"
        self.last_failure_time = None

    def call(self, func, *args):

        # ==========================
        # Estado OPEN
        # ==========================
        if self.state == "OPEN":

            if time.time() - self.last_failure_time > self.recovery_timeout:
                print("Mudando para HALF-OPEN...")
                self.state = "HALF-OPEN"
            else:
                return "Circuito aberto. Servidor temporariamente indisponível."

        try:
            result = func(*args)

            # Se estava HALF-OPEN e funcionou
            if self.state == "HALF-OPEN":
                print("Servidor recuperado. Fechando circuito.")
                self.state = "CLOSED"
                self.failure_count = 0

            return result

        except Exception as e:

            self.failure_count += 1
            self.last_failure_time = time.time()

            print("Erro detectado:", e)

            if self.failure_count >= self.failure_threshold:
                print("Limite de falhas atingido. Abrindo circuito.")
                self.state = "OPEN"

            return "Erro na comunicação com o servidor."
