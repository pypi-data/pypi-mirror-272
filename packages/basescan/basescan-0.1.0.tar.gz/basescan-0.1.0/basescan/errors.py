"""
Errors module for the API Exceptions.
"""
class APIError(Exception):
    def __init__(self, message: str, status_code: str = "NOTOK"):
        super().__init__(f"{message} [{status_code}]")
        self.status_code = status_code
    

class InvalidAPIKey(APIError):
    def __init__(self, msg: str, api_key: str):
        super().__init__(f"Invalid API Key! {msg}: {api_key!r}")