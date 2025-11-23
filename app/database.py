"""
Database connection and management for Azure SQL Database
"""
import pyodbc
import logging
from typing import Optional, List, Dict, Any
from contextlib import contextmanager
from app.config import get_settings

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database connections and queries for Azure SQL"""
    
    def __init__(self):
        self.settings = get_settings()
        self.connection_string = self.settings.database_connection_string
        
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = None
        try:
            conn = pyodbc.connect(self.connection_string)
            logger.info("Database connection established")
            yield conn
        except pyodbc.Error as e:
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
                
                # Get column names
                columns = [column[0] for column in cursor.description]
                
                # Fetch all rows and convert to dictionaries
                results = []
                for row in cursor.fetchall():
                    results.append(dict(zip(columns, row)))
                
                logger.info(f"Query executed successfully, returned {len(results)} rows")
                return results
                
            except pyodbc.Error as e:
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
                
            except pyodbc.Error as e:
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
