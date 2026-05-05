import pytest
from src.schemas import Schemas
from src.utils.helpers import extract_ids

class TestTodosAPI:
    """Test suite for Todos API."""
    
    @pytest.mark.smoke
    def test_get_all_todos_status_code(self, todos_api):
        """Test GET /todos returns 200 status code."""
        response = todos_api.get_all_todos()
        assert response.status_code == 200
    
    @pytest.mark.regression
    def test_get_all_todos_returns_list(self, all_todos):
        """Test GET /todos returns a list."""
        assert isinstance(all_todos, list)
        assert len(all_todos) > 0
    
    @pytest.mark.schema
    def test_todos_schema_validation(self, all_todos):
        """Test all todos match the expected schema."""
        assert Schemas.validate_list_schema(all_todos, Schemas.TODO_SCHEMA)
    
    @pytest.mark.regression
    def test_todos_completed_field_is_boolean(self, all_todos):
        """Test completed field is boolean."""
        for todo in all_todos:
            assert isinstance(todo["completed"], bool), f"Todo {todo['id']} completed is not boolean"
    
    @pytest.mark.regression
    def test_todos_belong_to_valid_users(self, all_todos, all_users):
        """Test all todos belong to valid users."""
        user_ids = extract_ids(all_users, "id")
        for todo in all_todos:
            assert todo["userId"] in user_ids, f"Todo {todo['id']} has invalid userId"
    
    @pytest.mark.parametrize("user_id", [1, 5, 10])
    @pytest.mark.regression
    def test_get_todos_by_user(self, todos_api, user_id):
        """Test GET /todos?userId={id}."""
        response = todos_api.get_todos_by_user(user_id)
        assert response.status_code == 200
        todos = response.json()
        for todo in todos:
            assert todo["userId"] == user_id
    
    @pytest.mark.regression
    def test_todos_completed_vs_pending_analysis(self, all_todos):
        """Test completed vs pending todos analysis."""
        completed = [t for t in all_todos if t["completed"]]
        pending = [t for t in all_todos if not t["completed"]]
        
        assert len(completed) + len(pending) == len(all_todos)
        assert len(completed) > 0, "No completed todos found"
        assert len(pending) > 0, "No pending todos found"
    
    @pytest.mark.database
    def test_todos_completion_status_in_db(self, all_todos, all_users, db):
        """Test todos completion status in database."""
        for user in all_users[:3]:  # Check first 3 users
            user_todos = [t for t in all_todos if t["userId"] == user["id"]]
            api_completed = len([t for t in user_todos if t["completed"]])
            api_pending = len([t for t in user_todos if not t["completed"]])
            
            db_completed = db.get_completed_todos_count(user["id"])
            db_pending = db.get_pending_todos_count(user["id"])
            
            assert api_completed == db_completed
            assert api_pending == db_pending
