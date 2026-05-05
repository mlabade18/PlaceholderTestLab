from typing import Optional
import requests
from src.api.base_client import BaseAPIClient

class UsersAPI(BaseAPIClient):
    """API client for Users endpoints."""
    
    ENDPOINT = "/users"
    
    def get_all_users(self) -> requests.Response:
        """Get all users."""
        return self.get(self.ENDPOINT)
    
    def get_user_by_id(self, user_id: int) -> requests.Response:
        """Get user by ID."""
        return self.get(f"{self.ENDPOINT}/{user_id}")
    
    def get_user_by_invalid_id(self, user_id: str) -> requests.Response:
        """Get user by invalid ID (for negative testing)."""
        return self.get(f"{self.ENDPOINT}/{user_id}")
    