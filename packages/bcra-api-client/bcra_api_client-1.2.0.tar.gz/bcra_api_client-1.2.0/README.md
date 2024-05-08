# BCRA Client Python

![pypi version](https://img.shields.io/pypi/v/bcra-api-client?style=flat&label=pypi%20package&color=green)

Consumo de datos de la API del Banco Central de la República Argentina (BCRA)

Esta librería está construida con base en la documentación presentada por la misma entidad en el siguiente [link](https://www.bcra.gob.ar/BCRAyVos/catalogo-de-APIs-banco-central.asp).

## Instalar

Debe usar pip para instalar o actualizar a la última versión estable.
```
pip install -U bcra-api-client
```

## Como usar
Su uso es simple, se debe crear primero un cliente a la API.

**Nota**: Hasta ahora la API tiene dos endpoints de estadísticas.

## Cliente API
```python
from bcra import Client

client = Client()
```

## Configurar el Cliente
Se pueden cambiar las configuraciones de un cliente de la siguiente manera: 
```python
from bcra import ConfigClient, Client

config = ConfigClient(language='es')

client = Client(config)
```

### Referencias

- #### language: 
Los idiomas configurados actualmente “es-AR” y “en-US”. De no informar dicho
parámetro, la respuesta se realizará por defecto en “es-AR”.

Los valores admitidos son “es” referenciando a “es-AR” o “en” a “en-US”.


## Principales variables
Para obtener la lista de todas las variables publicadas por el BCRA.
```python
statistics = client.statistics
print(statistics.variables())
```

## Datos de Variable
Para obtener los valores para la variable y el rango de fechas indicadas.

Se debe llamar al mismo método con los siguientes parámetros (id_variable, from_, to)

Donde: 

- **id_variable**: (Int) Se obtiene de consultar a la lista de todas las variables
- **from_**: (String) Corresponde a la fecha de inicio del rango a consultar, la misma deberá tener el formato yyyy-mm-dd
- **to**: (String) Corresponde a la fecha de fin del rango a consultar, la misma deberá tener el formato yyyy-mm-dd

```python
statistics = client.statistics
print(statistics.variables(5, '2024-01-01', '2024-05-01'))
```

