from bcra.base import BaseClient
from bcra.config import ConfigClient
from bcra.exceptions import PathIncomplete

PATH_ROOT = "estadisticas/v1/"


class Variables(BaseClient):
    """
        Clase para contener las variables principales del BCRA
    """

    def __init__(self, config: ConfigClient) -> None:
        self.path = PATH_ROOT
        super().__init__(config)

    def variables(self, id_variable: int = None,
                  from_: str = None,
                  to: str = None) -> list:
        """
        "Constructor" de la clase para llamar a los métodos correspondientes dependiendo de los parametros ingresados, si no se ingresa parametros
        devolvera la lista de variables completas, caso contrario se filtrará una variable en el rango fecha solicitada

        :param id_variable: ID de la variable deseada, la misma se puede consultar por el endpoint “Obtener principales variables
        :param from_: Corresponde a la fecha de inicio del rango a consultar, la misma deberá tener el formato yyyy-mm-dd
        :param to: Corresponde a la fecha de fin del rango a consultar, la misma deberá tener el formato yyyy-mm-dd

        :return: Retorna una lista de los valores de las principales variables o de la variable solicitada dentro de un rango de fecha
        """

        if id_variable is None and from_ is None and to is None:
            return self.get()
        else:
            return self.filter(id_variable, from_, to)

    def get(self) -> list:
        """
        Método para obtener la lista de todas las variables publicadas por el BCRA

        :return: Lista de valores
        """
        path = self.path + "principalesvariables"

        response = self._get(path=path)
        return response['results']

    def filter(self,
               id_variable: int = None,
               from_: str = None,
               to: str = None) -> list:
        """
        Método para obtener los valores para la variable y el rango de fechas indicadas

        :param id_variable: ID de la variable deseada, la misma se puede consultar por el endpoint “Obtener principales variables
        :param from_: Corresponde a la fecha de inicio del rango a consultar, la misma deberá tener el formato yyyy-mm-dd
        :param to: Corresponde a la fecha de fin del rango a consultar, la misma deberá tener el formato yyyy-mm-dd

        :return: Lista de valores de la variable deseada dentro del rango de fecha seleccionado
        """

        if id_variable is None:
            raise PathIncomplete(
                f"id_variable no puede estar vacio"
            )

        if from_ is None or len(from_) == 0:
            raise PathIncomplete(
                f"fecha desde no puede estar vacio"
            )

        if to is None or len(from_) == 0:
            raise PathIncomplete(
                f"fecha hasta no puede estar vacio"
            )

        # TODO - Validacion de formato fechas

        self.path = f"{self.path}datosvariable/{id_variable}/{from_}/{to}"
        print(self.path)

        response = self._get(path=self.path)
        return response['results']
