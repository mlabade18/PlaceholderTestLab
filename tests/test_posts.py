import pytest
from src.schemas import Schemas
from src.utils.helpers import extract_ids, find_orphan_records

class TestPostsAPI:
    """Test suite for Posts API."""
    
    @pytest.mark.smoke
    def test_get_all_posts_status_code(self, posts_api):
        """Test GET /posts returns 200 status code."""
        response = posts_api.get_all_posts()
        assert response.status_code == 200
    
    @pytest.mark.regression
    def test_get_all_posts_returns_list(self, all_posts):
        """Test GET /posts returns a list."""
        assert isinstance(all_posts, list)
        assert len(all_posts) > 0
    
    @pytest.mark.schema
    def test_posts_schema_validation(self, all_posts):
        """Test all posts match the expected schema."""
        assert Schemas.validate_list_schema(all_posts, Schemas.POST_SCHEMA)
    
    @pytest.mark.regression
    def test_posts_mandatory_fields(self, all_posts):
        """Test all posts have mandatory fields."""
        mandatory_fields = ["id", "userId", "title", "body"]
        for post in all_posts:
            for field in mandatory_fields:
                assert field in post, f"Missing field: {field}"
    
    @pytest.mark.parametrize("post_id", [1, 50, 100])
    @pytest.mark.regression
    def test_get_post_by_valid_id(self, posts_api, post_id):
        """Test GET /posts/{id} with valid IDs."""
        response = posts_api.get_post_by_id(post_id)
        assert response.status_code == 200
        post = response.json()
        assert post["id"] == post_id
    
    @pytest.mark.regression
    def test_posts_belong_to_valid_users(self, all_posts, all_users):
        """Test all posts belong to valid users."""
        user_ids = extract_ids(all_users, "id")
        for post in all_posts:
            assert post["userId"] in user_ids, f"Post {post['id']} has invalid userId"
    
    @pytest.mark.regression
    def test_no_orphan_posts(self, all_posts, all_users):
        """Test no posts reference non-existent users."""
        user_ids = extract_ids(all_users, "id")
        orphans = find_orphan_records(all_posts, user_ids, "userId")
        assert len(orphans) == 0, f"Found {len(orphans)} orphan posts"
    
    @pytest.mark.parametrize("user_id", [1, 2, 3])
    @pytest.mark.regression
    def test_get_posts_by_user(self, posts_api, user_id):
        """Test GET /posts?userId={id}."""
        response = posts_api.get_posts_by_user(user_id)
        assert response.status_code == 200
        posts = response.json()
        for post in posts:
            assert post["userId"] == user_id
    
    @pytest.mark.database
    def test_post_count_per_user_in_db(self, all_posts, all_users, db):
        """Test post count per user matches database."""
        for user in all_users:
            api_count = len([p for p in all_posts if p["userId"] == user["id"]])
            db_count = db.get_post_count_by_user(user["id"])
            assert api_count == db_count, f"User {user['id']}: API={api_count}, DB={db_count}"
