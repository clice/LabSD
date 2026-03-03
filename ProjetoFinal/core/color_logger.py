import logging


class ColorFormatter(logging.Formatter):
    """
    Formatter customizado que adiciona cores aos logs para facilitar a 
    identificação de erros e mensagens importantes.
    """
    
    COLORS = {
        logging.DEBUG: "\033[94m",     # Azul
        logging.INFO: "\033[92m",      # Verde
        logging.WARNING: "\033[93m",   # Amarelo
        logging.ERROR: "\033[91m",     # Vermelho
        logging.CRITICAL: "\033[95m",  # Magenta
    }
    
    RESET = "\033[0m"
    
    def format(self, record):
        color = self.COLORS.get(record.levelno, self.RESET)
        message = super().format(record)
        return f"{color}{message}{self.RESET}"


def setup_logger(name: str):
    """
    Configura um logger com formatação colorida.
    """
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)  # Loga todos os níveis
    
    # Criar console handler com formatação colorida
    console_handler = logging.StreamHandler()
    formatter = ColorFormatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger