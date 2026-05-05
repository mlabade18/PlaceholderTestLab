import pytest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api import UsersAPI, PostsAPI, CommentsAPI, AlbumsAPI, TodosAPI
from src.database import DatabaseManager
from src.utils.logger import Logger

# Session-scoped fixtures
@pytest.fixture(scope="session")
def logger():
    """Session-scoped logger."""
    return Logger()

@pytest.fixture(scope="session")
def db():
    """Session-scoped database manager."""
    return DatabaseManager()

@pytest.fixture(scope="session")
def users_api():
    """Session-scoped Users API client."""
    return UsersAPI()

@pytest.fixture(scope="session")
def posts_api():
    """Session-scoped Posts API client."""
    return PostsAPI()

@pytest.fixture(scope="session")
def comments_api():
    """Session-scoped Comments API client."""
    return CommentsAPI()

@pytest.fixture(scope="session")
def albums_api():
    """Session-scoped Albums API client."""
    return AlbumsAPI()

@pytest.fixture(scope="session")
def todos_api():
    """Session-scoped Todos API client."""
    return TodosAPI()

# Data fixtures
@pytest.fixture(scope="session")
def all_users(users_api, db):
    """Fetch and store all users."""
    response = users_api.get_all_users()
    users = response.json()
    db.insert_users(users)
    return users

@pytest.fixture(scope="session")
def all_posts(posts_api, db, all_users):
    """Fetch and store all posts."""
    response = posts_api.get_all_posts()
    posts = response.json()
    db.insert_posts(posts)
    return posts

@pytest.fixture(scope="session")
def all_comments(comments_api, db, all_posts):
    """Fetch and store all comments."""
    response = comments_api.get_all_comments()
    comments = response.json()
    db.insert_comments(comments)
    return comments

@pytest.fixture(scope="session")
def all_albums(albums_api, db, all_users):
    """Fetch and store all albums."""
    response = albums_api.get_all_albums()
    albums = response.json()
    db.insert_albums(albums)
    return albums

@pytest.fixture(scope="session")
def all_todos(todos_api, db, all_users):
    """Fetch and store all todos."""
    response = todos_api.get_all_todos()
    todos = response.json()
    db.insert_todos(todos)
    return todos

# Pytest hooks
def pytest_configure(config):
    """Configure custom markers."""
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "regression: mark test as regression test")
    config.addinivalue_line("markers", "negative: mark test as negative test")
    config.addinivalue_line("markers", "schema: mark test as schema validation test")
    config.addinivalue_line("markers", "database: mark test as database validation test")
