from typing import Dict


class Authentication:
    def __init__(self, api_token: str):
        self.api_token = api_token

    def get_headers(self) -> Dict[str, str]:
        return {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }
