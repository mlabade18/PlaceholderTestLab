import requests
from typing import Optional, Any
from config.config import Config
from src.utils.decorators import retry, log_api_call
from src.utils.logger import Logger

class BaseAPIClient:
    """Base API client with common HTTP methods."""
    
    def __init__(self):
        self.base_url = Config.BASE_URL
        self.timeout = Config.TIMEOUT
        self.session = requests.Session()
        self.logger = Logger()
    
    @retry(max_attempts=3, delay=1.0)
    @log_api_call
    def get(self, endpoint: str, params: Optional[dict] = None) -> requests.Response:
        """Perform GET request."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, params=params, timeout=self.timeout)
        return response
    
    @retry(max_attempts=3, delay=1.0)
    @log_api_call
    def post(self, endpoint: str, data: dict) -> requests.Response:
        """Perform POST request."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url, json=data, timeout=self.timeout)
        return response
    
    @retry(max_attempts=3, delay=1.0)
    @log_api_call
    def put(self, endpoint: str, data: dict) -> requests.Response:
        """Perform PUT request."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.put(url, json=data, timeout=self.timeout)
        return response
    
    @retry(max_attempts=3, delay=1.0)
    @log_api_call
    def delete(self, endpoint: str) -> requests.Response:
        """Perform DELETE request."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.delete(url, timeout=self.timeout)
        return response
