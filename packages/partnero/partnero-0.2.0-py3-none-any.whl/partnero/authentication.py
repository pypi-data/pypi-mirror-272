from typing import Dict


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Authentication(metaclass=SingletonMeta):
    api_token = None

    @classmethod
    def configure(cls, api_token):
        cls.api_token = api_token

    def get_headers(self) -> Dict[str, str]:
        if not self.api_token:
            raise ValueError("API token has not been set.")
        return {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }
