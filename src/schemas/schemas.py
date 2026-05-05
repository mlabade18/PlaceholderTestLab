from jsonschema import validate, ValidationError
from typing import Any

class Schemas:
    """JSON Schemas for API response validation."""
    
    USER_SCHEMA = {
        "type": "object",
        "required": ["id", "name", "username", "email"],
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "username": {"type": "string"},
            "email": {"type": "string"},
            "phone": {"type": "string"},
            "website": {"type": "string"},
            "address": {
                "type": "object",
                "properties": {
                    "street": {"type": "string"},
                    "suite": {"type": "string"},
                    "city": {"type": "string"},
                    "zipcode": {"type": "string"},
                    "geo": {
                        "type": "object",
                        "properties": {
                            "lat": {"type": "string"},
                            "lng": {"type": "string"}
                        }
                    }
                }
            },
            "company": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "catchPhrase": {"type": "string"},
                    "bs": {"type": "string"}
                }
            }
        }
    }
    
    POST_SCHEMA = {
        "type": "object",
        "required": ["id", "userId", "title", "body"],
        "properties": {
            "id": {"type": "integer"},
            "userId": {"type": "integer"},
            "title": {"type": "string"},
            "body": {"type": "string"}
        }
    }
    
    COMMENT_SCHEMA = {
        "type": "object",
        "required": ["id", "postId", "name", "email", "body"],
        "properties": {
            "id": {"type": "integer"},
            "postId": {"type": "integer"},
            "name": {"type": "string"},
            "email": {"type": "string"},
            "body": {"type": "string"}
        }
    }
    
    ALBUM_SCHEMA = {
        "type": "object",
        "required": ["id", "userId", "title"],
        "properties": {
            "id": {"type": "integer"},
            "userId": {"type": "integer"},
            "title": {"type": "string"}
        }
    }
    
    TODO_SCHEMA = {
        "type": "object",
        "required": ["id", "userId", "title", "completed"],
        "properties": {
            "id": {"type": "integer"},
            "userId": {"type": "integer"},
            "title": {"type": "string"},
            "completed": {"type": "boolean"}
        }
    }
    
    @staticmethod
    def validate_schema(data: Any, schema: dict) -> bool:
        """Validate data against schema."""
        try:
            validate(instance=data, schema=schema)
            return True
        except ValidationError:
            return False
    
    @staticmethod
    def validate_list_schema(data: list, schema: dict) -> bool:
        """Validate list of items against schema."""
        return all(Schemas.validate_schema(item, schema) for item in data)
