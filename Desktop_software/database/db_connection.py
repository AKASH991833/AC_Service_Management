"""
Database connection management - THREAD-SAFE with AUTO-RECONNECT
Production-ready with comprehensive logging and error handling
"""
import mysql.connector
from mysql.connector import Error, errorcode
import threading
import time
from typing import Optional, Any, Dict, List, Union
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import DB_CONFIG

# Import logging
try:
    from utils.logger import get_loggers, log_database_query
    loggers = get_loggers()
    logger = loggers['app']
    db_logger = loggers['database']
    error_logger = loggers['error']
except Exception:
    # Fallback if logging not available
    import logging
    logger = logging.getLogger(__name__)
    db_logger = logger
    error_logger = logger


class DatabaseConnection:
    """
    Thread-safe database connection with auto-reconnect and connection pooling
    Singleton pattern ensures single connection instance
    """
    _instance: Optional['DatabaseConnection'] = None
    _lock = threading.Lock()
    _query_lock = threading.Lock()
    _connection: Optional[Any] = None
    _cursor: Optional[Any] = None

    def __new__(cls) -> 'DatabaseConnection':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize_connection()
        return cls._instance

    def _initialize_connection(self) -> None:
        """Initialize database connection with comprehensive error handling"""
        try:
            # Build connection parameters
            conn_params = {
                'host': DB_CONFIG['host'],
                'user': DB_CONFIG['user'],
                'password': DB_CONFIG['password'],
                'database': DB_CONFIG['database'],
                'port': DB_CONFIG['port'],
                'charset': DB_CONFIG['charset'],
                'use_unicode': True,
                'autocommit': DB_CONFIG.get('autocommit', True),
                'connection_timeout': DB_CONFIG.get('connection_timeout', 60),
                'ssl_disabled': DB_CONFIG.get('ssl_disabled', True),
            }

            # Add pool settings if available
            if 'pool_name' in DB_CONFIG and 'pool_size' in DB_CONFIG:
                conn_params['pool_name'] = DB_CONFIG['pool_name']
                conn_params['pool_size'] = DB_CONFIG['pool_size']
                conn_params['pool_reset_session'] = DB_CONFIG.get('pool_reset_session', True)

            self._connection = mysql.connector.connect(**conn_params)
            self._cursor = self._connection.cursor(dictionary=True)
            
            logger.info("✅ Database connected successfully")
            db_logger.info(f"Connected to {DB_CONFIG['database']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}")

        except Error as e:
            error_msg = self._get_mysql_error_message(e)
            error_logger.error(f"MySQL Error: {error_msg}")
            db_logger.error(f"Connection failed: {error_msg}")
            raise ConnectionError(f"Database connection failed: {error_msg}")
        except Exception as e:
            error_logger.error(f"Unexpected connection error: {e}", exc_info=True)
            raise ConnectionError(f"Unexpected database error: {str(e)}")

    def _get_mysql_error_message(self, error: Error) -> str:
        """Get human-readable MySQL error message"""
        if hasattr(error, 'errno'):
            error_code = error.errno
            if error_code == errorcode.ER_ACCESS_DENIED_ERROR:
                return "Invalid database credentials (username/password)"
            elif error_code == errorcode.ER_BAD_DB_ERROR:
                return f"Database '{DB_CONFIG['database']}' does not exist"
            elif error_code == errorcode.CR_CONN_HOST_ERROR:
                return f"Cannot connect to database server at {DB_CONFIG['host']}:{DB_CONFIG['port']}"
            elif error_code == errorcode.CR_CONNECTION_ERROR:
                return "Connection refused - check if MySQL server is running"
        return str(error)

    def _check_connection(self) -> bool:
        """Check if connection is alive, reconnect if needed"""
        try:
            if not hasattr(self, '_connection') or not self._connection.is_connected():
                logger.warning("⚠️ Database connection lost, reconnecting...")
                self._initialize_connection()
                return False
            return True
        except Exception as e:
            error_logger.error(f"Connection check failed: {e}")
            return False

    def _reconnect_with_retry(self, max_retries: int = 3) -> bool:
        """Reconnect with retry logic and exponential backoff"""
        for attempt in range(max_retries):
            try:
                time.sleep(0.5 * attempt)  # Exponential backoff
                logger.info(f"Reconnect attempt {attempt + 1}/{max_retries}")
                
                # Close existing cursor
                if hasattr(self, '_cursor') and self._cursor:
                    try:
                        self._cursor.close()
                    except Exception:
                        pass
                
                self._initialize_connection()
                logger.info("✅ Reconnection successful")
                return True
            except Exception as e:
                error_logger.error(f"Reconnect attempt {attempt + 1}/{max_retries} failed: {e}")
                if attempt == max_retries - 1:
                    error_logger.error("❌ All reconnect attempts failed")
                    return False
        return False

    def execute_query(
        self,
        query: str,
        params: Optional[Union[tuple, list]] = None,
        fetch_one: bool = False,
        fetch_all: bool = False
    ) -> Optional[Union[Dict, List[Dict], int]]:
        """
        Execute SQL query with thread-safety and auto-reconnect
        
        Args:
            query: SQL query string
            params: Query parameters (tuple or list)
            fetch_one: Fetch single result
            fetch_all: Fetch all results
        
        Returns:
            Query result (dict, list, or row id)
        """
        with self._query_lock:
            max_retries = 3
            start_time = time.time()
            
            for attempt in range(max_retries):
                try:
                    # Check and reconnect if needed
                    if not self._check_connection():
                        if not self._reconnect_with_retry():
                            raise ConnectionError("Failed to reconnect to database")

                    # Validate inputs
                    if not query or not isinstance(query, str):
                        raise ValueError("Query must be a non-empty string")
                    
                    # Log query (without sensitive data)
                    db_logger.debug(f"Executing: {query[:100]}...")

                    # Execute query with proper parameter handling
                    if params is None:
                        self._cursor.execute(query)
                    else:
                        if not isinstance(params, (tuple, list)):
                            params = (params,)
                        self._cursor.execute(query, params)

                    # Handle different query types
                    if fetch_one:
                        result = self._cursor.fetchone()
                        duration = time.time() - start_time
                        log_database_query(query, params, duration)
                        return result
                    elif fetch_all:
                        result = self._cursor.fetchall()
                        duration = time.time() - start_time
                        log_database_query(query, params, duration)
                        return result
                    elif query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
                        self._connection.commit()
                        row_id = self._cursor.lastrowid
                        duration = time.time() - start_time
                        db_logger.info(f"Query executed in {duration:.3f}s, row_id: {row_id}")
                        return row_id
                    else:
                        return None

                except Error as e:
                    error_msg = str(e)
                    # Check for specific connection error codes
                    connection_error_codes = ['2003', '2006', '2013', 'Lost connection', '2002']
                    if any(code in error_msg for code in connection_error_codes):
                        logger.warning(f"⚠️ Connection error, attempting reconnect ({attempt + 1}/{max_retries})")
                        if attempt < max_retries - 1:
                            if self._reconnect_with_retry():
                                continue
                    
                    error_logger.error(f"MySQL Query Error: {error_msg}")
                    error_logger.error(f"Query: {query[:200]}...")
                    
                    # Rollback on error
                    if hasattr(self, '_connection') and self._connection:
                        try:
                            self._connection.rollback()
                            error_logger.info("Transaction rolled back")
                        except Exception as rollback_error:
                            error_logger.error(f"Rollback failed: {rollback_error}")
                    raise
                    
                except ValueError as ve:
                    error_logger.error(f"Validation error: {ve}")
                    raise
                    
                except Exception as e:
                    error_logger.error(f"Unexpected error in execute_query: {e}", exc_info=True)
                    if hasattr(self, '_connection') and self._connection:
                        try:
                            self._connection.rollback()
                        except Exception:
                            pass
                    raise
            
            error_logger.error("Max retries exceeded for query")
            raise ConnectionError("Max retries exceeded")

    def execute_many(self, query: str, params_list: List[Union[tuple, list]]) -> int:
        """
        Execute query with multiple parameter sets - thread-safe
        
        Args:
            query: SQL query string
            params_list: List of parameter tuples
        
        Returns:
            Number of affected rows
        """
        with self._query_lock:
            try:
                if not params_list:
                    logger.warning("execute_many called with empty params_list")
                    return 0

                if not self._check_connection():
                    if not self._reconnect_with_retry():
                        raise ConnectionError("Failed to reconnect to database")

                db_logger.info(f"Executing batch query with {len(params_list)} parameter sets")
                self._cursor.executemany(query, params_list)
                self._connection.commit()
                
                rowcount = self._cursor.rowcount
                logger.info(f"Batch query executed, affected rows: {rowcount}")
                return rowcount
                
            except Error as e:
                error_logger.error(f"MySQL batch query error: {e}")
                error_logger.error(f"Query: {query[:200]}...")
                if hasattr(self, '_connection') and self._connection:
                    try:
                        self._connection.rollback()
                    except Exception:
                        pass
                raise
            except Exception as e:
                error_logger.error(f"Unexpected error in execute_many: {e}", exc_info=True)
                if hasattr(self, '_connection') and self._connection:
                    try:
                        self._connection.rollback()
                    except Exception:
                        pass
                raise

    def close(self) -> None:
        """Close database connection gracefully"""
        try:
            if hasattr(self, '_cursor') and self._cursor:
                self._cursor.close()
                logger.info("Database cursor closed")
                
            if hasattr(self, '_connection') and self._connection and self._connection.is_connected():
                self._connection.close()
                logger.info("✅ Database disconnected")
        except Exception as e:
            error_logger.error(f"Error closing database connection: {e}")

    @property
    def connection(self) -> Any:
        """Get database connection"""
        return self._connection

    @property
    def cursor(self) -> Any:
        """Get database cursor"""
        return self._cursor


class DatabaseContext:
    """Context manager for database operations"""
    def __init__(self):
        self.db = DatabaseConnection()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Don't close connection - reuse it (singleton pattern)
        # Just log any exceptions
        if exc_type:
            error_logger.error(f"Database context error: {exc_val}")
        return False  # Don't suppress exceptions