import requests
from requests.exceptions import RequestException
from .authentication import Authentication


class BaseAPI:
    def __init__(self, auth: Authentication, base_url: str = "https://api.partnero.com/v1/"):
        self.auth = auth
        self.base_url = base_url

    def send_request(self, method: str, endpoint: str, data=None, params=None) -> dict:
        url = f"{self.base_url}{endpoint}"
        headers = self.auth.get_headers()
        try:
            response = requests.request(method, url, headers=headers, json=data, params=params)
            return self.handle_api_response(response)
        except RequestException as e:
            raise Exception(f"Network-related error occurred: {str(e)}")

    @staticmethod
    def handle_api_response(response: requests.Response) -> dict:
        if response.status_code not in [200, 201]:
            try:
                error_details = response.json()
                error_message = error_details.get('message', 'An unknown error occurred')
            except ValueError:
                error_message = response.text
            raise Exception(f"API Error {response.status_code}: {error_message}")
        try:
            return response.json()
        except ValueError:
            raise Exception("Failed to decode JSON response")
