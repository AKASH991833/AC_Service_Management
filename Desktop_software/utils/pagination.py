"""
Pagination Utility - Performance Optimization
Reusable pagination component for large data sets
Features:
- Configurable page size
- Navigate first/previous/next/last
- Jump to specific page
- Total count and page info
"""
from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class PageInfo:
    """Pagination metadata"""
    current_page: int
    page_size: int
    total_items: int
    total_pages: int
    has_previous: bool
    has_next: bool
    previous_page: Optional[int]
    next_page: Optional[int]
    start_item: int
    end_item: int


class Paginator:
    """
    Generic paginator for database query results
    Thread-safe and reusable
    """
    
    # Default page sizes
    SMALL = 10
    MEDIUM = 25
    LARGE = 50
    EXTRA_LARGE = 100
    
    def __init__(self, page_size: int = 25):
        """
        Initialize paginator
        
        Args:
            page_size: Number of items per page (default: 25)
        """
        if page_size < 1:
            raise ValueError("page_size must be at least 1")
        self.page_size = page_size
        self.current_page = 1
        self.total_items = 0
        self.total_pages = 0
        self.data = []
    
    def calculate_total_pages(self):
        """Calculate total pages from total items"""
        if self.total_items == 0:
            self.total_pages = 0
        else:
            self.total_pages = (self.total_items + self.page_size - 1) // self.page_size
    
    def set_total_items(self, total: int):
        """
        Set total item count and recalculate pages
        
        Args:
            total: Total number of items in dataset
        """
        self.total_items = total
        self.calculate_total_pages()
        
        # Adjust current page if out of range
        if self.current_page > self.total_pages and self.total_pages > 0:
            self.current_page = self.total_pages
    
    def set_data(self, data: List[Any]):
        """
        Set current page data
        
        Args:
            data: List of items for current page
        """
        self.data = data
    
    def get_page_info(self) -> PageInfo:
        """Get pagination metadata"""
        start_item = 0
        end_item = 0
        
        if self.total_items > 0:
            start_item = ((self.current_page - 1) * self.page_size) + 1
            end_item = min(self.current_page * self.page_size, self.total_items)
        
        return PageInfo(
            current_page=self.current_page,
            page_size=self.page_size,
            total_items=self.total_items,
            total_pages=self.total_pages,
            has_previous=self.current_page > 1,
            has_next=self.current_page < self.total_pages,
            previous_page=self.current_page - 1 if self.current_page > 1 else None,
            next_page=self.current_page + 1 if self.current_page < self.total_pages else None,
            start_item=start_item,
            end_item=end_item
        )
    
    def get_offset(self) -> int:
        """Get SQL OFFSET for current page"""
        return (self.current_page - 1) * self.page_size
    
    def get_limit(self) -> int:
        """Get SQL LIMIT for current page"""
        return self.page_size
    
    def goto_page(self, page: int) -> bool:
        """
        Navigate to specific page
        
        Args:
            page: Page number to go to
            
        Returns:
            True if successful, False if page out of range
        """
        if page < 1 or (self.total_pages > 0 and page > self.total_pages):
            return False
        
        self.current_page = page
        return True
    
    def next_page(self) -> bool:
        """
        Go to next page
        
        Returns:
            True if successful, False if already on last page
        """
        if self.current_page >= self.total_pages:
            return False
        self.current_page += 1
        return True
    
    def previous_page(self) -> bool:
        """
        Go to previous page
        
        Returns:
            True if successful, False if already on first page
        """
        if self.current_page <= 1:
            return False
        self.current_page -= 1
        return True
    
    def first_page(self) -> bool:
        """
        Go to first page
        
        Returns:
            True if successful
        """
        self.current_page = 1
        return True
    
    def last_page(self) -> bool:
        """
        Go to last page
        
        Returns:
            True if successful, False if no pages
        """
        if self.total_pages == 0:
            return False
        self.current_page = self.total_pages
        return True
    
    def reset(self):
        """Reset paginator to initial state"""
        self.current_page = 1
        self.total_items = 0
        self.total_pages = 0
        self.data = []
    
    def change_page_size(self, new_size: int):
        """
        Change page size and reset to first page
        
        Args:
            new_size: New page size
        """
        if new_size < 1:
            raise ValueError("page_size must be at least 1")
        self.page_size = new_size
        self.current_page = 1
        self.calculate_total_pages()
    
    def get_display_range(self) -> str:
        """Get human-readable display range (e.g., "Showing 1-25 of 100")"""
        info = self.get_page_info()
        if info.total_items == 0:
            return "No items"
        return f"Showing {info.start_item}-{info.end_item} of {info.total_items}"
    
    def get_status_text(self) -> str:
        """Get page status text (e.g., "Page 1 of 10")"""
        info = self.get_page_info()
        if info.total_pages == 0:
            return "Page 0 of 0"
        return f"Page {info.current_page} of {info.total_pages}"


class DatabasePaginator(Paginator):
    """
    Paginator with database query helpers
    Automatically generates SQL with LIMIT and OFFSET
    """
    
    def __init__(self, page_size: int = 25):
        super().__init__(page_size)
        self.base_query = ""
        self.count_query = ""
        self.params = []
    
    def set_query(self, base_query: str, count_query: Optional[str] = None, params: Optional[list] = None):
        """
        Set base query for pagination
        
        Args:
            base_query: SQL query without LIMIT/OFFSET
            count_query: Optional COUNT query (auto-generated if not provided)
            params: Query parameters
        """
        self.base_query = base_query
        self.params = params or []
        
        # Auto-generate count query if not provided
        if count_query:
            self.count_query = count_query
        else:
            # Simple count query generation
            # Remove ORDER BY for count query
            query_without_order = base_query.upper().split('ORDER BY')[0].strip()
            self.count_query = f"SELECT COUNT(*) as total FROM ({query_without_order}) as count_table"
    
    def get_paginated_query(self) -> str:
        """Get SQL query with LIMIT and OFFSET"""
        if not self.base_query:
            raise ValueError("No query set. Call set_query() first.")
        
        return f"{self.base_query} LIMIT {self.get_limit()} OFFSET {self.get_offset()}"
    
    def execute_pagination(self, db_connection) -> tuple:
        """
        Execute paginated query and return (data, total_count)
        
        Args:
            db_connection: Database connection object with execute_query method
            
        Returns:
            Tuple of (page_data, total_count)
        """
        if not self.base_query:
            raise ValueError("No query set")
        
        # Get total count
        count_result = db_connection.execute_query(self.count_query, self.params, fetch_one=True)
        total = count_result.get('total', 0) if count_result else 0
        self.set_total_items(total)
        
        # Get page data
        paginated_query = self.get_paginated_query()
        data = db_connection.execute_query(paginated_query, self.params, fetch_all=True)
        self.set_data(data or [])
        
        return data, total


# Convenience functions for common page sizes
def small_paginator() -> Paginator:
    """Create paginator with 10 items per page"""
    return Paginator(10)


def medium_paginator() -> Paginator:
    """Create paginator with 25 items per page"""
    return Paginator(25)


def large_paginator() -> Paginator:
    """Create paginator with 50 items per page"""
    return Paginator(50)
