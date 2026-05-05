import pytest
from src.schemas import Schemas
from src.utils.helpers import extract_ids

class TestAlbumsAPI:
    """Test suite for Albums API."""
    
    @pytest.mark.smoke
    def test_get_all_albums_status_code(self, albums_api):
        """Test GET /albums returns 200 status code."""
        response = albums_api.get_all_albums()
        assert response.status_code == 200
    
    @pytest.mark.regression
    def test_get_all_albums_returns_list(self, all_albums):
        """Test GET /albums returns a list."""
        assert isinstance(all_albums, list)
        assert len(all_albums) > 0
    
    @pytest.mark.schema
    def test_albums_schema_validation(self, all_albums):
        """Test all albums match the expected schema."""
        assert Schemas.validate_list_schema(all_albums, Schemas.ALBUM_SCHEMA)
    
    @pytest.mark.regression
    def test_albums_belong_to_valid_users(self, all_albums, all_users):
        """Test all albums belong to valßid users."""
        user_ids = extract_ids(all_users, "id")
        for album in all_albums:
            assert album["userId"] in user_ids, f"Album {album['id']} has invalid userId"
    
    @pytest.mark.parametrize("user_id", [1, 5, 10])
    @pytest.mark.regression
    def test_get_albums_by_user(self, albums_api, user_id):
        """Test GET /albums?userId={id}."""
        response = albums_api.get_albums_by_user(user_id)
        assert response.status_code == 200
        albums = response.json()
        for album in albums:
            assert album["userId"] == user_id
