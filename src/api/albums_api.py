import requests
from src.api.base_client import BaseAPIClient

class AlbumsAPI(BaseAPIClient):
    """API client for Albums endpoints."""
    
    ENDPOINT = "/albums"
    
    def get_all_albums(self) -> requests.Response:
        """Get all albums."""
        return self.get(self.ENDPOINT)
    
    def get_albums_by_user(self, user_id: int) -> requests.Response:
        """Get albums by user ID."""
        return self.get(self.ENDPOINT, params={"userId": user_id})
