import requests
from src.api.base_client import BaseAPIClient

class TodosAPI(BaseAPIClient):
    """API client for Todos endpoints."""
    
    ENDPOINT = "/todos"
    
    def get_all_todos(self) -> requests.Response:
        """Get all todos."""
        return self.get(self.ENDPOINT)
    
    def get_todos_by_user(self, user_id: int) -> requests.Response:
        """Get todos by user ID."""
        return self.get(self.ENDPOINT, params={"userId": user_id})
