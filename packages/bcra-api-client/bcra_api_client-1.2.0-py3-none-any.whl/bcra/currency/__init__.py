from bcra.config import ConfigClient
from .dollar import Dollar


class Currency:
    """
        Clase para agrugar funciones relacionadas al tipo de cambio
    """
    def __init__(self, config: ConfigClient):
        self.USD = Dollar(config).dollar
