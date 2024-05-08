from bcra.config import ConfigClient
from .variables import Variables


class Statistics:
    """
        Clase de orden jerárquico para agrugar todos los endpoint de api.bcra.gob.ar/estadisticas/*
    """
    def __init__(self, config: ConfigClient) -> None:
        self.variables = Variables(config).variables
