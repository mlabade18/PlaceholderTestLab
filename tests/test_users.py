import pytest
from src.schemas import Schemas
from src.utils.helpers import validate_email, validate_response_time

class TestUsersAPI:
    """Test suite for Users API."""
    
    @pytest.mark.smoke
    def test_get_all_users_status_code(self, users_api):
        """Test GET /users returns 200 status code."""
        response = users_api.get_all_users()
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    @pytest.mark.smoke
    def test_get_all_users_response_time(self, users_api):
        """Test GET /users response time is within threshold."""
        response = users_api.get_all_users()
        assert validate_response_time(response.elapsed.total_seconds())
    
    @pytest.mark.regression
    def test_get_all_users_returns_list(self, all_users):
        """Test GET /users returns a list."""
        assert isinstance(all_users, list)
        assert len(all_users) > 0
    
    @pytest.mark.schema
    def test_users_schema_validation(self, all_users):
        """Test all users match the expected schema."""
        assert Schemas.validate_list_schema(all_users, Schemas.USER_SCHEMA)
    
    @pytest.mark.regression
    def test_users_mandatory_fields(self, all_users):
        """Test all users have mandatory fields."""
        mandatory_fields = ["id", "name", "username", "email"]
        for user in all_users:
            for field in mandatory_fields:
                assert field in user, f"Missing field: {field}"
    
    @pytest.mark.regression
    def test_users_email_format(self, all_users):
        """Test all users have valid email format."""
        for user in all_users:
            assert validate_email(user["email"]), f"Invalid email: {user['email']}"
    
    @pytest.mark.regression
    def test_users_unique_ids(self, all_users):
        """Test all user IDs are unique."""
        user_ids = [user["id"] for user in all_users]
        assert len(user_ids) == len(set(user_ids)), "Duplicate user IDs found"
    
    @pytest.mark.parametrize("user_id", [1, 2, 3, 5, 10])
    @pytest.mark.regression
    def test_get_user_by_valid_id(self, users_api, user_id):
        """Test GET /users/{id} with valid IDs."""
        response = users_api.get_user_by_id(user_id)
        assert response.status_code == 200
        user = response.json()
        assert user["id"] == user_id
    
    @pytest.mark.negative
    def test_get_user_invalid_id(self, users_api):
        """Test GET /users/{id} with non-existent ID."""
        response = users_api.get_user_by_id(9999)
        assert response.status_code == 404
    
    @pytest.mark.negative
    def test_get_user_non_numeric_id(self, users_api):
        """Test GET /users/{id} with non-numeric ID."""
        response = users_api.get_user_by_invalid_id("abc")
        assert response.status_code == 404
    
    @pytest.mark.database
    def test_users_count_in_db(self, all_users, db):
        """Test user count in API matches database."""
        db_count = db.get_user_count()
        assert len(all_users) == db_count, f"API: {len(all_users)}, DB: {db_count}"
    
    @pytest.mark.database
    def test_user_data_matches_db(self, all_users, db):
        """Test API user data matches database data."""
        db_users = db.get_all_users()
        api_user_ids = {user["id"] for user in all_users}
        db_user_ids = {user["id"] for user in db_users}
        assert api_user_ids == db_user_ids
