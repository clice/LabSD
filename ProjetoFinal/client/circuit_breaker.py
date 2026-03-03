"""
circuit_breaker.py

Implementação do padrão Circuit Breaker.

O Circuit Breaker é um padrão de tolerância a falhas utilizado
em sistemas distribuídos para evitar:
- Chamadas repetidas a serviços indisponíveis
- Sobrecarga desnecessária
- Efeito cascata de falhas
- Aumento de latência devido a múltiplos retries

Estados possíveis:
CLOSED     -> Operação normal
OPEN       -> Chamadas bloqueadas temporariamente
HALF_OPEN  -> Teste para verificar se serviço se recuperou
"""

import time


class CircuitBreaker:
    """
    Implementação simplificada de padrão de tolerância a falhas
    """
    
    def __init__(self, failure_threshold=3, recovery_timeout=5):
        """
        failure_threshold:
            Número de falhas consecutivas necessárias
            para abrir o circuito.

        recovery_timeout:
            Tempo (em segundos) que o circuito permanece
            aberto antes de permitir nova tentativa.
        """
        
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        
        # Estado iniical do circuito
        self.state = "CLOSED"
        
        # Contador de falhas consecutivas
        self.failure_count = 0
        
        # Momento da última falha crítica
        self.last_failure_time = None
        
    
    # ==========================================================
    # Controle antes da chamada
    # ==========================================================
    
    def before_call(self):
        """
        Deve ser chamado antes de qualquer operação remota.
        Verifica se o circuito permite execução.
        """
        
        if self.state == "OPEN":
            # Verifica se já passou o tempo de recuperação
            elapsed_time = time.time() - self.last_failure_time
            
            if elapsed_time >= self.recovery_timeout:
                # Permite tentativa de teste
                self.state = "HALF_OPEN"
            else:
                # Bloqueia chamada
                raise Exception("Circuito aberto. Serviço temporariamente indisponível.")
            
    
    # ==========================================================
    # Evento de sucesso
    # ==========================================================
    
    def on_success(self):
        """
        Deve ser chamado quando uma chamada remota
        é executada com sucesso.
        Reseta completamente o circuito.
        """
        
        self.state = "CLOSED"
        self.failure_count = 0
        self.last_failure_time = None
        
    
    # ==========================================================
    # Evento de falha
    # ==========================================================

    def on_failure(self):
        """
        Deve ser chamado quando ocorre falha definitiva.
        Incrementa contador e abre circuito se necessário.
        """
        
        self.failure_count += 1
        
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            self.last_failure_time = time.time()