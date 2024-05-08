from bcra.config import ConfigClient
from bcra.statistics import Variables


class Dollar(Variables):
    """
        Clase para contener los métodos referentes al tipo de cambio Dólar
    """
    def __init__(self, config: ConfigClient):
        super().__init__(config)

    def dollar(self) -> list:
        """
        Método para traer las variables de dólar minorista y dólar mayorista con la ultima cotización
        :return: lista de valores de variables con id 4 y 5
        """

        response = super().get()
        dollar = []
        dollar_filter = filter(lambda data: data['idVariable'] in (4, 5), response)

        for d in dollar_filter:
            dollar.append(d)

        return dollar
