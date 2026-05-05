from typing import Optional
import requests
from src.api.base_client import BaseAPIClient

class PostsAPI(BaseAPIClient):
    """API client for Posts endpoints."""
    
    ENDPOINT = "/posts"
    
    def get_all_posts(self) -> requests.Response:
        """Get all posts."""
        return self.get(self.ENDPOINT)
    
    def get_post_by_id(self, post_id: int) -> requests.Response:
        """Get post by ID."""
        return self.get(f"{self.ENDPOINT}/{post_id}")
    
    def get_posts_by_user(self, user_id: int) -> requests.Response:
        """Get posts by user ID."""
        return self.get(self.ENDPOINT, params={"userId": user_id})
