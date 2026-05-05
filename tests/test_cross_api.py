import pytest
from src.utils.helpers import extract_ids

class TestCrossAPIValidation:
    """Test suite for cross-API data validation."""
    
    @pytest.mark.regression
    def test_all_posts_have_valid_user_references(self, all_users, all_posts):
        """Validate post.userId exists in users data."""
        user_ids = extract_ids(all_users, "id")
        invalid_posts = [p for p in all_posts if p["userId"] not in user_ids]
        assert len(invalid_posts) == 0, f"Posts with invalid user references: {invalid_posts}"
    
    @pytest.mark.regression
    def test_all_comments_have_valid_post_references(self, all_posts, all_comments):
        """Validate comment.postId exists in posts data."""
        post_ids = extract_ids(all_posts, "id")
        invalid_comments = [c for c in all_comments if c["postId"] not in post_ids]
        assert len(invalid_comments) == 0, f"Comments with invalid post references: {invalid_comments}"
    
    @pytest.mark.regression
    def test_user_post_comment_chain(self, all_users, all_posts, all_comments):
        """Validate the complete user -> post -> comment relationship chain."""
        user_ids = extract_ids(all_users, "id")
        
        for post in all_posts:
            assert post["userId"] in user_ids, f"Post {post['id']} has invalid user"
            
            post_comments = [c for c in all_comments if c["postId"] == post["id"]]
            for comment in post_comments:
                assert comment["postId"] == post["id"]
    
    @pytest.mark.regression
    def test_all_albums_have_valid_user_references(self, all_users, all_albums):
        """Validate album.userId exists in users data."""
        user_ids = extract_ids(all_users, "id")
        invalid_albums = [a for a in all_albums if a["userId"] not in user_ids]
        assert len(invalid_albums) == 0, f"Albums with invalid user references: {invalid_albums}"
    
    @pytest.mark.regression
    def test_all_todos_have_valid_user_references(self, all_users, all_todos):
        """Validate todo.userId exists in users data."""
        user_ids = extract_ids(all_users, "id")
        invalid_todos = [t for t in all_todos if t["userId"] not in user_ids]
        assert len(invalid_todos) == 0, f"Todos with invalid user references: {invalid_todos}"
    
    @pytest.mark.database
    def test_api_data_consistency_with_db(self, all_users, all_posts, db):
        """Test API data is consistent with database."""
        api_user_ids = extract_ids(all_users, "id")
        db_user_ids = db.get_all_user_ids()
        
        assert api_user_ids == db_user_ids, "User IDs mismatch between API and DB"
        
        api_post_ids = extract_ids(all_posts, "id")
        db_post_ids = db.get_all_post_ids()
        
        assert api_post_ids == db_post_ids, "Post IDs mismatch between API and DB"
    
    @pytest.mark.regression
    def test_data_integrity_summary(self, all_users, all_posts, all_comments, all_albums, all_todos):
        """Summary test for overall data integrity."""
        user_ids = extract_ids(all_users, "id")
        post_ids = extract_ids(all_posts, "id")
        
        # Validate counts
        assert len(all_users) == 10, f"Expected 10 users, got {len(all_users)}"
        assert len(all_posts) == 100, f"Expected 100 posts, got {len(all_posts)}"
        assert len(all_comments) == 500, f"Expected 500 comments, got {len(all_comments)}"
        
        # Validate relationships
        posts_valid = all(p["userId"] in user_ids for p in all_posts)
        comments_valid = all(c["postId"] in post_ids for c in all_comments)
        albums_valid = all(a["userId"] in user_ids for a in all_albums)
        todos_valid = all(t["userId"] in user_ids for t in all_todos)
        
        assert posts_valid, "Invalid post-user relationships"
        assert comments_valid, "Invalid comment-post relationships"
        assert albums_valid, "Invalid album-user relationships"
        assert todos_valid, "Invalid todo-user relationships"
