import os

class Config:
    """Configuration singleton for the test framework."""
    _instance = None
    
    BASE_URL = "https://jsonplaceholder.typicode.com"
    TIMEOUT = 30
    MAX_RETRIES = 3
    RESPONSE_TIME_THRESHOLD = 2.0  # seconds
    
    # Database Configuration - EASILY SWITCH HERE
    DB_TYPE = os.getenv("DB_TYPE", "sqlite")  # sqlite, postgresql, mysql
    
    # SQLite (default)
    DB_NAME = ":memory:"
    
    # PostgreSQL Configuration
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "test_db")
    
    # MySQL Configuration
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")
    MYSQL_DB = os.getenv("MYSQL_DB", "test_db")
    
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

