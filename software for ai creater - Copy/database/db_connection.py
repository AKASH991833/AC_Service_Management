"""
Database connection management - THREAD-SAFE with AUTO-RECONNECT
"""
import mysql.connector
from mysql.connector import Error
import threading
import time
from config import DB_CONFIG

class DatabaseConnection:
    _instance = None
    _lock = threading.Lock()
    _query_lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize_connection()
        return cls._instance

    def _initialize_connection(self):
        """Initialize connection with improved error handling"""
        try:
            from config import DB_CONFIG
            
            # Build connection parameters dynamically
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
                'ssl_verify_cert': DB_CONFIG.get('ssl_verify_cert', False)
            }
            
            # Add pool settings if available
            if 'pool_name' in DB_CONFIG:
                conn_params['pool_name'] = DB_CONFIG['pool_name']
            if 'pool_size' in DB_CONFIG:
                conn_params['pool_size'] = DB_CONFIG['pool_size']
            if 'pool_reset_session' in DB_CONFIG:
                conn_params['pool_reset_session'] = DB_CONFIG['pool_reset_session']
            
            self.connection = mysql.connector.connect(**conn_params)
            self.cursor = self.connection.cursor(dictionary=True)
            self._connection_failed = False
            print("[OK] Database connected!")

        except Error as e:
            print(f"[ERROR] MySQL Error: {e}")
            self._connection_failed = True
            raise
        except Exception as e:
            print(f"[ERROR] Connection Error: {e}")
            self._connection_failed = True
            raise

    def _check_connection(self):
        """Check if connection is alive, reconnect if needed"""
        try:
            if not hasattr(self, 'connection') or not self.connection.is_connected():
                print("[WARN] Connection lost, reconnecting...")
                self._initialize_connection()
                return False
            return True
        except:
            return False

    def _reconnect_with_retry(self, max_retries=3):
        """Reconnect with retry logic"""
        for attempt in range(max_retries):
            try:
                time.sleep(0.5 * attempt)  # Exponential backoff
                if hasattr(self, 'cursor') and self.cursor:
                    try:
                        self.cursor.close()
                    except:
                        pass
                self._initialize_connection()
                return True
            except Exception as e:
                print(f"[WARN] Reconnect attempt {attempt + 1}/{max_retries} failed: {e}")
                if attempt == max_retries - 1:
                    return False
        return False

    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        """Execute SQL query with thread-safety and auto-reconnect"""
        with self._query_lock:
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    # Check and reconnect if needed
                    if not self._check_connection():
                        if not self._reconnect_with_retry():
                            raise Exception("Failed to reconnect to database")

                    # Validate inputs
                    if not query or not isinstance(query, str):
                        raise ValueError("Query must be a non-empty string")

                    # Execute query with proper parameter handling
                    if params is None:
                        self.cursor.execute(query)
                    else:
                        if not isinstance(params, (tuple, list)):
                            params = (params,)
                        self.cursor.execute(query, params)

                    if fetch_one:
                        return self.cursor.fetchone()
                    elif fetch_all:
                        return self.cursor.fetchall()
                    elif query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
                        self.connection.commit()
                        return self.cursor.lastrowid
                    else:
                        return None

                except Error as e:
                    error_msg = str(e)
                    # Check if it's a connection error
                    if any(code in error_msg for code in ['2003', '2006', '2013', 'Lost connection']):
                        print(f"[WARN] Connection error, attempting reconnect ({attempt + 1}/{max_retries})")
                        if attempt < max_retries - 1:
                            if self._reconnect_with_retry():
                                continue
                    print(f"[ERROR] Query Error: {e}")
                    print(f"Query: {query[:100]}...")
                    if hasattr(self, 'connection') and self.connection:
                        try:
                            self.connection.rollback()
                        except:
                            pass
                    raise
                except Exception as e:
                    print(f"[ERROR] Unexpected Error: {e}")
                    if hasattr(self, 'connection') and self.connection:
                        try:
                            self.connection.rollback()
                        except:
                            pass
                    raise
            raise Exception("Max retries exceeded")

    def execute_many(self, query, params_list):
        """Execute query with multiple parameter sets - thread-safe"""
        with self._query_lock:
            try:
                if not params_list:
                    return 0

                if not self._check_connection():
                    if not self._reconnect_with_retry():
                        raise Exception("Failed to reconnect to database")

                self.cursor.executemany(query, params_list)
                self.connection.commit()
                return self.cursor.rowcount
            except Error as e:
                print(f"[ERROR] Query Error: {e}")
                print(f"Query: {query[:100]}...")
                if hasattr(self, 'connection') and self.connection:
                    try:
                        self.connection.rollback()
                    except:
                        pass
                raise
            except Exception as e:
                print(f"[ERROR] Unexpected Error: {e}")
                if hasattr(self, 'connection') and self.connection:
                    try:
                        self.connection.rollback()
                    except:
                        pass
                raise

    def close(self):
        """Close connection"""
        try:
            if hasattr(self, 'cursor') and self.cursor:
                self.cursor.close()
            if hasattr(self, 'connection') and self.connection and self.connection.is_connected():
                self.connection.close()
            print("[OK] Database disconnected")
        except Exception as e:
            print(f"[ERROR] Error closing connection: {e}")


class DatabaseContext:
    def __init__(self):
        self.db = DatabaseConnection()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass  # Connection close मत करो - reuse करो