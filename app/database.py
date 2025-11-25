"""
Database connection and management for SQLite Database
"""
import sqlite3
import logging
from typing import Optional, List, Dict, Any
from contextlib import contextmanager
from pathlib import Path
from app.config import get_settings

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database connections and queries for SQLite"""
    
    def __init__(self):
        self.settings = get_settings()
        self.db_path = self.settings.database_path
        self._ensure_database_exists()
        
    def _ensure_database_exists(self):
        """Create database and schema if it doesn't exist"""
        db_file = Path(self.db_path)
        if not db_file.exists():
            logger.info(f"Database not found at {self.db_path}, creating new database")
            # Create empty database
            conn = sqlite3.connect(self.db_path)
            conn.close()
            # Initialize schema
            self._initialize_schema()
        else:
            logger.info(f"Using existing database at {self.db_path}")
    
    def _initialize_schema(self):
        """Initialize database schema from schema_sqlite.sql"""
        schema_path = Path(__file__).parent.parent / "schema_sqlite.sql"
        if schema_path.exists():
            logger.info(f"Initializing database schema from {schema_path}")
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            
            with self.get_connection() as conn:
                conn.executescript(schema_sql)
                conn.commit()
            logger.info("Database schema initialized successfully")
        else:
            logger.warning(f"Schema file not found at {schema_path}")
        
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable column access by name
            logger.info("Database connection established")
            yield conn
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            raise
        finally:
            if conn:
                conn.close()
                logger.info("Database connection closed")
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """
        Execute a SELECT query and return results as list of dictionaries
        
        Args:
            query: SQL query string
            params: Optional tuple of query parameters
            
        Returns:
            List of dictionaries containing query results
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                # Fetch all rows and convert to dictionaries
                rows = cursor.fetchall()
                results = [dict(row) for row in rows]
                
                logger.info(f"Query executed successfully, returned {len(results)} rows")
                return results
                
            except sqlite3.Error as e:
                logger.error(f"Query execution error: {e}")
                raise
            finally:
                cursor.close()
    
    def execute_non_query(self, query: str, params: Optional[tuple] = None) -> int:
        """
        Execute an INSERT, UPDATE, or DELETE query
        
        Args:
            query: SQL query string
            params: Optional tuple of query parameters
            
        Returns:
            Number of rows affected
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                conn.commit()
                rows_affected = cursor.rowcount
                logger.info(f"Non-query executed successfully, {rows_affected} rows affected")
                return rows_affected
                
            except sqlite3.Error as e:
                conn.rollback()
                logger.error(f"Non-query execution error: {e}")
                raise
            finally:
                cursor.close()
    
    def test_connection(self) -> bool:
        """Test database connectivity"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                cursor.fetchone()
                logger.info("Database connection test successful")
                return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False


# Singleton instance
db_manager = DatabaseManager()
