import os

class Config:
    """Configuration singleton for the test framework."""
    _instance = None
    
    BASE_URL = "https://jsonplaceholder.typicode.com"
    TIMEOUT = 30
    MAX_RETRIES = 3
    RESPONSE_TIME_THRESHOLD = 2.0  # seconds
    
    # Database
    DB_NAME = ":memory:"  # In-memory SQLite
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = "logs/test_execution.log"
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def get_instance(cls) -> "Config":
        return cls()


