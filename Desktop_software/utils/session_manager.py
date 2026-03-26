"""
Session Manager - Handle user sessions across the application
Singleton pattern to ensure only one session exists at a time
"""
from datetime import datetime
import threading
import logging

logger = logging.getLogger(__name__)


class SessionManager:
    """
    Singleton session manager for tracking logged-in user
    Thread-safe implementation
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                # Double-check locking pattern
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize_session()
                    cls._instance._lock = threading.Lock()
        return cls._instance
    
    def _initialize_session(self):
        """Initialize session variables"""
        self._current_user = None
        self._login_time = None
        self._session_id = None
    
    def login(self, user_data):
        """
        Start a new session for logged-in user

        Args:
            user_data (dict): User information from database
        """
        with self._lock:
            self._current_user = user_data
            self._login_time = datetime.now()
            self._session_id = f"session_{user_data['id']}_{int(self._login_time.timestamp())}"

        print(f"[SESSION] User logged in: {user_data.get('username', 'Unknown')}")
        print(f"[SESSION] Session ID: {self._session_id}")
        print(f"[SESSION] Login time: {self._login_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def logout(self):
        """End current session"""
        with self._lock:
            if self._current_user:
                username = self._current_user.get('username', 'Unknown')
                print(f"[SESSION] User logged out: {username}")

            self._current_user = None
            self._login_time = None
            self._session_id = None
    
    def get_current_user(self):
        """
        Get current logged-in user data
        
        Returns:
            dict or None: User data if logged in, None otherwise
        """
        return self._current_user
    
    def get_user_id(self):
        """
        Get current user ID
        
        Returns:
            int or None: User ID if logged in, None otherwise
        """
        if self._current_user:
            return self._current_user.get('id')
        return None
    
    def get_username(self):
        """
        Get current username
        
        Returns:
            str or None: Username if logged in, None otherwise
        """
        if self._current_user:
            return self._current_user.get('username', 'Unknown')
        return None
    
    def is_logged_in(self):
        """
        Check if user is logged in
        
        Returns:
            bool: True if user is logged in, False otherwise
        """
        return self._current_user is not None
    
    def get_login_time(self):
        """
        Get session login time
        
        Returns:
            datetime or None: Login time if logged in, None otherwise
        """
        return self._login_time
    
    def get_session_duration(self):
        """
        Get current session duration
        
        Returns:
            timedelta or None: Session duration if logged in, None otherwise
        """
        if self._login_time:
            return datetime.now() - self._login_time
        return None
    
    def get_session_id(self):
        """
        Get current session ID
        
        Returns:
            str or None: Session ID if logged in, None otherwise
        """
        return self._session_id
    
    def get_user_full_name(self):
        """
        Get current user's full name
        
        Returns:
            str or None: Full name if logged in, None otherwise
        """
        if self._current_user:
            return self._current_user.get('full_name', 'Unknown')
        return None
    
    def get_user_email(self):
        """
        Get current user's email
        
        Returns:
            str or None: Email if logged in, None otherwise
        """
        if self._current_user:
            return self._current_user.get('email', '')
        return None
    
    def get_user_phone(self):
        """
        Get current user's phone number
        
        Returns:
            str or None: Phone number if logged in, None otherwise
        """
        if self._current_user:
            return self._current_user.get('phone', '')
        return None
    
    def is_admin(self):
        """
        Check if current user is admin

        Returns:
            bool: True if user is admin, False otherwise
        """
        if self._current_user:
            username = self._current_user.get('username', '').lower()
            return username == 'admin'
        return False

    def refresh_session(self, updated_user_data):
        """
        Refresh session with updated user data from database
        Called after profile update to ensure session has latest data

        Args:
            updated_user_data (dict): Updated user information from database
        """
        with self._lock:
            if self._current_user and updated_user_data:
                # Update only mutable fields, keep id and username unchanged
                self._current_user['full_name'] = updated_user_data.get('full_name', self._current_user.get('full_name'))
                self._current_user['email'] = updated_user_data.get('email', self._current_user.get('email'))
                self._current_user['phone'] = updated_user_data.get('phone', self._current_user.get('phone'))
                self._current_user['is_active'] = updated_user_data.get('is_active', self._current_user.get('is_active'))
                
                print(f"[SESSION] Refreshed user data: {self._current_user}")
                logger.info(f"[SESSION] User session refreshed: {self._current_user.get('username')}")
            elif updated_user_data:
                # If no current user, set it (edge case)
                self._current_user = updated_user_data
                print(f"[SESSION] Set user data: {self._current_user}")


# Global session instance
_session_manager = None


def get_session():
    """
    Get global session manager instance
    
    Returns:
        SessionManager: Global session instance
    """
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager


def is_user_logged_in():
    """
    Quick check if user is logged in
    
    Returns:
        bool: True if user is logged in
    """
    return get_session().is_logged_in()


def get_current_user():
    """
    Get current logged-in user
    
    Returns:
        dict or None: User data
    """
    return get_session().get_current_user()


def logout_user():
    """
    Logout current user
    """
    get_session().logout()
