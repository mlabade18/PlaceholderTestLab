import requests
from src.api.base_client import BaseAPIClient

class CommentsAPI(BaseAPIClient):
    """API client for Comments endpoints."""
    
    ENDPOINT = "/comments"
    
    def get_all_comments(self) -> requests.Response:
        """Get all comments."""
        return self.get(self.ENDPOINT)
    
    def get_comments_by_post(self, post_id: int) -> requests.Response:
        """Get comments by post ID."""
        return self.get(self.ENDPOINT, params={"postId": post_id})
