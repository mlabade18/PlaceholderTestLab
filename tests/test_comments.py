import pytest
from src.schemas import Schemas
from src.utils.helpers import validate_email, extract_ids, find_orphan_records

class TestCommentsAPI:
    """Test suite for Comments API."""
    
    @pytest.mark.smoke
    def test_get_all_comments_status_code(self, comments_api):
        """Test GET /comments returns 200 status code."""
        response = comments_api.get_all_comments()
        assert response.status_code == 200
    
    @pytest.mark.regression
    def test_get_all_comments_returns_list(self, all_comments):
        """Test GET /comments returns a list."""
        assert isinstance(all_comments, list)
        assert len(all_comments) > 0
    
    @pytest.mark.schema
    def test_comments_schema_validation(self, all_comments):
        """Test all comments match the expected schema."""
        assert Schemas.validate_list_schema(all_comments, Schemas.COMMENT_SCHEMA)
    
    @pytest.mark.regression
    def test_comments_email_format(self, all_comments):
        """Test all comments have valid email format."""
        for comment in all_comments:
            assert validate_email(comment["email"]), f"Invalid email: {comment['email']}"
    
    @pytest.mark.regression
    def test_comments_belong_to_valid_posts(self, all_comments, all_posts):
        """Test all comments belong to valid posts."""
        post_ids = extract_ids(all_posts, "id")
        for comment in all_comments:
            assert comment["postId"] in post_ids, f"Comment {comment['id']} has invalid postId"
    
    @pytest.mark.regression
    def test_no_orphan_comments(self, all_comments, all_posts):
        """Test no comments reference non-existent posts."""
        post_ids = extract_ids(all_posts, "id")
        orphans = find_orphan_records(all_comments, post_ids, "postId")
        assert len(orphans) == 0, f"Found {len(orphans)} orphan comments"
    
    @pytest.mark.parametrize("post_id", [1, 10, 50])
    @pytest.mark.regression
    def test_get_comments_by_post(self, comments_api, post_id):
        """Test GET /comments?postId={id}."""
        response = comments_api.get_comments_by_post(post_id)
        assert response.status_code == 200
        comments = response.json()
        for comment in comments:
            assert comment["postId"] == post_id
    
    @pytest.mark.database
    def test_comments_stored_in_db(self, all_comments, db):
        """Test comments are properly stored in database."""
        post_ids = db.get_all_post_ids()
        for comment in all_comments:
            assert comment["postId"] in post_ids
