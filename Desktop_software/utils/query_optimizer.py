"""
Query Optimization Utilities - Performance Enhancement
Features:
- Query result caching
- Batch query execution
- N+1 query problem solver
- Query performance monitoring
"""
import time
from typing import Dict, List, Any, Optional, Callable
from functools import wraps
from datetime import datetime, timedelta
import threading
import hashlib
import json


class QueryCache:
    """
    In-memory query result cache with TTL support
    Thread-safe implementation
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize cache storage"""
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._enabled = True
        self._default_ttl = 300  # 5 minutes default
        self._max_size = 1000  # Maximum cache entries
    
    def enable(self):
        """Enable caching"""
        self._enabled = True
    
    def disable(self):
        """Disable caching"""
        self._enabled = False
    
    def clear(self):
        """Clear all cached data"""
        with self._lock:
            self._cache.clear()
            print("[CACHE] Cleared all cached data")
    
    def _generate_key(self, query: str, params: Optional[tuple] = None) -> str:
        """Generate cache key from query and parameters"""
        key_data = f"{query}:{json.dumps(params, default=str, sort_keys=True)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, query: str, params: Optional[tuple] = None) -> Optional[Any]:
        """
        Get cached result if available and not expired
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            Cached result or None
        """
        if not self._enabled:
            return None
        
        key = self._generate_key(query, params)
        
        with self._lock:
            if key in self._cache:
                entry = self._cache[key]
                # Check if expired
                if datetime.now() < entry['expires_at']:
                    return entry['data']
                else:
                    # Remove expired entry
                    del self._cache[key]
        
        return None
    
    def set(self, query: str, data: Any, params: Optional[tuple] = None, 
            ttl: Optional[int] = None) -> bool:
        """
        Cache query result
        
        Args:
            query: SQL query string
            data: Data to cache
            params: Query parameters
            ttl: Time to live in seconds (default: 300)
            
        Returns:
            True if cached successfully
        """
        if not self._enabled:
            return False
        
        key = self._generate_key(query, params)
        ttl = ttl or self._default_ttl
        
        with self._lock:
            # Remove oldest entry if cache is full
            if len(self._cache) >= self._max_size:
                self._remove_oldest()
            
            self._cache[key] = {
                'data': data,
                'expires_at': datetime.now() + timedelta(seconds=ttl),
                'created_at': datetime.now(),
                'query': query[:100]  # Store query snippet for debugging
            }
        
        return True
    
    def _remove_oldest(self):
        """Remove oldest cache entry"""
        if not self._cache:
            return
        
        oldest_key = min(
            self._cache.keys(),
            key=lambda k: self._cache[k]['created_at']
        )
        del self._cache[oldest_key]
    
    def invalidate_pattern(self, pattern: str):
        """
        Invalidate cache entries matching pattern
        
        Args:
            pattern: Pattern to match in query strings
        """
        with self._lock:
            keys_to_remove = [
                key for key, entry in self._cache.items()
                if pattern.lower() in entry['query'].lower()
            ]
            for key in keys_to_remove:
                del self._cache[key]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        with self._lock:
            now = datetime.now()
            valid_entries = sum(
                1 for entry in self._cache.values()
                if now < entry['expires_at']
            )
            expired_entries = len(self._cache) - valid_entries
            
            return {
                'total_entries': len(self._cache),
                'valid_entries': valid_entries,
                'expired_entries': expired_entries,
                'max_size': self._max_size,
                'enabled': self._enabled,
                'default_ttl': self._default_ttl
            }


class QueryOptimizer:
    """
    Query optimization utilities
    Helps solve N+1 query problems with batch operations
    """
    
    def __init__(self, db_connection):
        """
        Initialize query optimizer
        
        Args:
            db_connection: Database connection object
        """
        self.db = db_connection
        self.cache = QueryCache()
        self._query_log = []
        self._enable_logging = False
    
    def enable_query_logging(self):
        """Enable query performance logging"""
        self._enable_logging = True
    
    def disable_query_logging(self):
        """Disable query performance logging"""
        self._enable_logging = False
    
    def _log_query(self, query: str, duration: float, rows: int = 0):
        """Log query for performance analysis"""
        if not self._enable_logging:
            return
        
        self._query_log.append({
            'query': query[:200],
            'duration': duration,
            'rows': rows,
            'timestamp': datetime.now()
        })
    
    def execute_with_cache(self, query: str, params: Optional[tuple] = None,
                          fetch_all: bool = False, ttl: int = 300):
        """
        Execute query with caching
        
        Args:
            query: SQL query
            params: Query parameters
            fetch_all: Fetch all results (vs fetch_one)
            ttl: Cache TTL in seconds
            
        Returns:
            Query result (from cache or database)
        """
        # Try cache first
        cached_result = self.cache.get(query, params)
        if cached_result is not None:
            return cached_result
        
        # Execute query
        start_time = time.time()
        result = self.db.execute_query(query, params, fetch_all=fetch_all)
        duration = time.time() - start_time
        
        # Log query
        rows = len(result) if isinstance(result, list) else 1
        self._log_query(query, duration, rows)
        
        # Cache result
        self.cache.set(query, result, params, ttl)
        
        return result
    
    def batch_fetch(self, table: str, ids: List[Any], 
                    id_column: str = 'id',
                    columns: Optional[List[str]] = None) -> Dict[Any, Any]:
        """
        Fetch multiple records in single query (solves N+1 problem)
        
        Args:
            table: Table name
            ids: List of IDs to fetch
            id_column: ID column name
            columns: Columns to select (default: all)
            
        Returns:
            Dictionary mapping ID to record
        """
        if not ids:
            return {}
        
        # Build query
        columns_str = '*' if not columns else ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(ids))
        query = f"""
            SELECT {columns_str}
            FROM {table}
            WHERE {id_column} IN ({placeholders})
        """
        
        # Execute single query instead of N queries
        start_time = time.time()
        results = self.db.execute_query(query, tuple(ids), fetch_all=True)
        duration = time.time() - start_time
        
        # Log
        self._log_query(query, duration, len(results))
        
        # Convert to dictionary
        return {row[id_column]: row for row in results} if results else {}
    
    def batch_fetch_with_mapping(self, table: str, foreign_ids: List[Any],
                                 foreign_key: str,
                                 local_key: str = 'id',
                                 columns: Optional[List[str]] = None) -> Dict[Any, List[Any]]:
        """
        Fetch related records for multiple parent records
        
        Example: Fetch all invoice items for multiple invoices
        Instead of: N queries (one per invoice)
        Use: 1 query with IN clause
        
        Args:
            table: Table name (e.g., 'invoice_items')
            foreign_ids: List of parent IDs (e.g., invoice IDs)
            foreign_key: Foreign key column (e.g., 'invoice_id')
            local_key: Local key column (e.g., 'id')
            columns: Columns to select
            
        Returns:
            Dictionary mapping parent ID to list of child records
        """
        if not foreign_ids:
            return {}
        
        columns_str = '*' if not columns else ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(foreign_ids))
        query = f"""
            SELECT {columns_str}
            FROM {table}
            WHERE {foreign_key} IN ({placeholders})
            ORDER BY {foreign_key}
        """
        
        start_time = time.time()
        results = self.db.execute_query(query, tuple(foreign_ids), fetch_all=True)
        duration = time.time() - start_time
        
        self._log_query(query, duration, len(results))
        
        # Group by foreign key
        grouped = {}
        for row in results:
            key = row[foreign_key]
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(row)
        
        return grouped
    
    def get_query_log(self) -> List[Dict]:
        """Get query performance log"""
        return self._query_log
    
    def clear_query_log(self):
        """Clear query log"""
        self._query_log.clear()
    
    def analyze_queries(self) -> Dict[str, Any]:
        """Analyze query performance"""
        if not self._query_log:
            return {'status': 'No queries logged'}
        
        total_queries = len(self._query_log)
        total_duration = sum(q['duration'] for q in self._query_log)
        avg_duration = total_duration / total_queries
        slowest = max(self._query_log, key=lambda q: q['duration'])
        slowest_queries = sorted(
            self._query_log, 
            key=lambda q: q['duration'], 
            reverse=True
        )[:5]
        
        return {
            'total_queries': total_queries,
            'total_duration_sec': total_duration,
            'avg_duration_ms': avg_duration * 1000,
            'slowest_query': slowest['query'][:100],
            'slowest_duration_ms': slowest['duration'] * 1000,
            'top_5_slowest': [
                {'query': q['query'][:50], 'duration_ms': q['duration'] * 1000}
                for q in slowest_queries
            ]
        }


def cached_query(ttl: int = 300):
    """
    Decorator for caching query results
    
    Usage:
        @cached_query(ttl=600)
        def get_customer_data(customer_id):
            return db.execute_query(
                "SELECT * FROM customers WHERE id = %s",
                (customer_id,),
                fetch_one=True
            )
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache = QueryCache()
            
            # Try cache first
            # Generate key from function name and arguments
            key_data = f"{func.__name__}:{args}:{kwargs}"
            key = hashlib.md5(key_data.encode()).hexdigest()
            
            cached_result = cache._cache.get(key)
            if cached_result and datetime.now() < cached_result['expires_at']:
                return cached_result['data']
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Cache result
            cache.set(func.__name__, result, ttl=ttl)
            
            return result
        return wrapper
    return decorator


# Global instances
_query_optimizer = None


def get_query_optimizer(db_connection):
    """Get global query optimizer instance"""
    global _query_optimizer
    if _query_optimizer is None:
        _query_optimizer = QueryOptimizer(db_connection)
    return _query_optimizer


def get_cache():
    """Get global cache instance"""
    return QueryCache()
