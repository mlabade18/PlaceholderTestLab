import sqlite3
from typing import List, Dict, Any, Optional, Set
from src.utils.logger import Logger
from config.config import Config

class DatabaseManager:
    """Database manager that supports multiple database types."""
    _instance = None
    _connection = None
    _db_type = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_db()
        return cls._instance
    
    def _initialize_db(self):
        """Initialize database based on DB_TYPE configuration."""
        self.logger = Logger()
        self._db_type = Config.DB_TYPE
        
        if self._db_type == "postgresql":
            self._initialize_postgresql()
        elif self._db_type == "mysql":
            self._initialize_mysql()
        else:  # Default to SQLite
            self._initialize_sqlite()
        
        self._create_tables()
        self.logger.info(f"Database initialized successfully with {self._db_type}")
    
    def _initialize_sqlite(self):
        """Initialize SQLite connection."""
        self._connection = sqlite3.connect(":memory:", check_same_thread=False)
        self._connection.row_factory = sqlite3.Row
    
    def _initialize_postgresql(self):
        """Initialize PostgreSQL connection."""
        try:
            import psycopg2
            self._connection = psycopg2.connect(
                host=Config.POSTGRES_HOST,
                port=Config.POSTGRES_PORT,
                user=Config.POSTGRES_USER,
                password=Config.POSTGRES_PASSWORD,
                database=Config.POSTGRES_DB
            )
            self.logger.info("Connected to PostgreSQL")
        except ImportError:
            self.logger.error("psycopg2 not installed. Install with: pip install psycopg2-binary")
            raise
    
    def _initialize_mysql(self):
        """Initialize MySQL connection."""
        try:
            import mysql.connector
            self._connection = mysql.connector.connect(
                host=Config.MYSQL_HOST,
                port=Config.MYSQL_PORT,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DB
            )
            self.logger.info("Connected to MySQL")
        except ImportError:
            self.logger.error("mysql-connector-python not installed. Install with: pip install mysql-connector-python")
            raise
    
    def _create_tables(self):
        """Create all required tables."""
        cursor = self._connection.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                username TEXT,
                email TEXT,
                phone TEXT,
                website TEXT,
                company_name TEXT,
                address_city TEXT
            )
        """)
        
        # Posts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY,
                userId INTEGER,
                title TEXT,
                body TEXT,
                FOREIGN KEY (userId) REFERENCES users(id)
            )
        """)
        
        # Comments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY,
                postId INTEGER,
                name TEXT,
                email TEXT,
                body TEXT,
                FOREIGN KEY (postId) REFERENCES posts(id)
            )
        """)
        
        # Albums table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS albums (
                id INTEGER PRIMARY KEY,
                userId INTEGER,
                title TEXT,
                FOREIGN KEY (userId) REFERENCES users(id)
            )
        """)
        
        # Todos table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY,
                userId INTEGER,
                title TEXT,
                completed BOOLEAN,
                FOREIGN KEY (userId) REFERENCES users(id)
            )
        """)
        
        self._connection.commit()
        cursor.close()
    
    def insert_users(self, users: List[Dict[str, Any]]):
        """Insert users into database."""
        cursor = self._connection.cursor()
        for user in users:
            cursor.execute("""
                INSERT OR REPLACE INTO users 
                (id, name, username, email, phone, website, company_name, address_city)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user.get("id"),
                user.get("name"),
                user.get("username"),
                user.get("email"),
                user.get("phone"),
                user.get("website"),
                user.get("company", {}).get("name"),
                user.get("address", {}).get("city")
            ))
        self._connection.commit()
        self.logger.info(f"Inserted {len(users)} users into database")
    
    def insert_posts(self, posts: List[Dict[str, Any]]):
        """Insert posts into database."""
        cursor = self._connection.cursor()
        for post in posts:
            cursor.execute("""
                INSERT OR REPLACE INTO posts (id, userId, title, body)
                VALUES (?, ?, ?, ?)
            """, (post.get("id"), post.get("userId"), post.get("title"), post.get("body")))
        self._connection.commit()
        self.logger.info(f"Inserted {len(posts)} posts into database")
    
    def insert_comments(self, comments: List[Dict[str, Any]]):
        """Insert comments into database."""
        cursor = self._connection.cursor()
        for comment in comments:
            cursor.execute("""
                INSERT OR REPLACE INTO comments (id, postId, name, email, body)
                VALUES (?, ?, ?, ?, ?)
            """, (
                comment.get("id"),
                comment.get("postId"),
                comment.get("name"),
                comment.get("email"),
                comment.get("body")
            ))
        self._connection.commit()
        self.logger.info(f"Inserted {len(comments)} comments into database")
    
    def insert_albums(self, albums: List[Dict[str, Any]]):
        """Insert albums into database."""
        cursor = self._connection.cursor()
        for album in albums:
            cursor.execute("""
                INSERT OR REPLACE INTO albums (id, userId, title)
                VALUES (?, ?, ?)
            """, (album.get("id"), album.get("userId"), album.get("title")))
        self._connection.commit()
        self.logger.info(f"Inserted {len(albums)} albums into database")
    
    def insert_todos(self, todos: List[Dict[str, Any]]):
        """Insert todos into database."""
        cursor = self._connection.cursor()
        for todo in todos:
            cursor.execute("""
                INSERT OR REPLACE INTO todos (id, userId, title, completed)
                VALUES (?, ?, ?, ?)
            """, (todo.get("id"), todo.get("userId"), todo.get("title"), todo.get("completed")))
        self._connection.commit()
        self.logger.info(f"Inserted {len(todos)} todos into database")
    
    def get_all_users(self) -> List[Dict]:
        """Get all users from database."""
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM users")
        return [dict(row) for row in cursor.fetchall()]
    
    def get_user_count(self) -> int:
        """Get total user count."""
        cursor = self._connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        return cursor.fetchone()[0]
    
    def get_post_count_by_user(self, user_id: int) -> int:
        """Get post count for a specific user."""
        cursor = self._connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM posts WHERE userId = ?", (user_id,))
        return cursor.fetchone()[0]
    
    def get_all_posts(self) -> List[Dict]:
        """Get all posts from database."""
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM posts")
        return [dict(row) for row in cursor.fetchall()]
    
    def get_all_user_ids(self) -> Set:
        """Get all user IDs from database."""
        cursor = self._connection.cursor()
        cursor.execute("SELECT id FROM users")
        return {row[0] for row in cursor.fetchall()}
    
    def get_all_post_ids(self) -> Set:
        """Get all post IDs from database."""
        cursor = self._connection.cursor()
        cursor.execute("SELECT id FROM posts")
        return {row[0] for row in cursor.fetchall()}
    
    def get_completed_todos_count(self, user_id: int) -> int:
        """Get count of completed todos for a user."""
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM todos WHERE userId = ? AND completed = 1",
            (user_id,)
        )
        return cursor.fetchone()[0]
    
    def get_pending_todos_count(self, user_id: int) -> int:
        """Get count of pending todos for a user."""
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM todos WHERE userId = ? AND completed = 0",
            (user_id,)
        )
        return cursor.fetchone()[0]
    
    def clear_all_tables(self):
        """Clear all tables."""
        cursor = self._connection.cursor()
        for table in ["users", "posts", "comments", "albums", "todos"]:
            cursor.execute(f"DELETE FROM {table}")
        self._connection.commit()
        self.logger.info("All tables cleared")
    
    def close_connection(self):
        """Close database connection."""
        if self._connection:
            self._connection.close()
            self.logger.info("Database connection closed")
