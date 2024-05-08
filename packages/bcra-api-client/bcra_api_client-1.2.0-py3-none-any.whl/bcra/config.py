import os

BASE = "https://api.bcra.gob.ar/"
ENV_KEY = "BCRA_API_KEY"


class ConfigClient:
    def __init__(self,
                 api_key: str = os.getenv(ENV_KEY),
                 connect_timeout: int = 400,
                 language: str = 'es') -> None:
        self.base_url = BASE
        self.api_key = api_key
        self.connect_timeout = connect_timeout
        self.language = None

        self.set_language(language)

    def set_language(self, lang):
        if lang == 'es':
            self.language = 'es-AR'
        elif lang == 'en':
            self.language = 'en-US'
        else:
            self.language = 'es-AR'
