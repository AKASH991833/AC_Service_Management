"""
Logging Configuration
Centralized logging setup for Ansh Air Cool
Logs to both file and console with proper rotation

IMPORTANT: Directory creation happens in setup_logging(), not at module import
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

# Global variable to track initialization
_initialized = False
_loggers = {}


def _get_logs_directory():
    """
    Get logs directory path without creating it
    Returns the path only
    """
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')


def _ensure_logs_directory():
    """
    Create logs directory if it doesn't exist
    Call this only when actually setting up logging
    """
    logs_dir = _get_logs_directory()
    os.makedirs(logs_dir, exist_ok=True)
    return logs_dir


def setup_logging(app=None):
    """
    Setup application logging with rotation
    
    Args:
        app: Flask app (optional, for app context logging)
    
    Returns:
        dict: Dictionary of loggers
    """
    global _initialized, _loggers
    
    # Return cached loggers if already initialized
    if _initialized and _loggers:
        return _loggers
    
    # Create logs directory (only when actually setting up logging)
    logs_dir = _ensure_logs_directory()
    
    # Main application logger
    app_logger = logging.getLogger('ansh_aircool')
    app_logger.setLevel(logging.INFO)
    
    # Security logger (separate file for security events)
    security_logger = logging.getLogger('ansh_aircool.security')
    security_logger.setLevel(logging.WARNING)
    
    # Admin actions logger
    admin_logger = logging.getLogger('ansh_aircool.admin')
    admin_logger.setLevel(logging.INFO)
    
    # Database logger
    db_logger = logging.getLogger('ansh_aircool.database')
    db_logger.setLevel(logging.WARNING)
    
    # Create formatters
    standard_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Security formatter (includes IP and user agent)
    security_formatter = logging.Formatter(
        '%(asctime)s - SECURITY - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handlers with rotation (10MB max, keep 5 backup files)
    app_file_handler = RotatingFileHandler(
        os.path.join(logs_dir, 'app.log'),
        maxBytes=10*1024*1024,
        backupCount=5,
        encoding='utf-8'
    )
    app_file_handler.setFormatter(standard_formatter)

    security_file_handler = RotatingFileHandler(
        os.path.join(logs_dir, 'security.log'),
        maxBytes=10*1024*1024,
        backupCount=10,  # Keep more security logs
        encoding='utf-8'
    )
    security_file_handler.setFormatter(security_formatter)

    admin_file_handler = RotatingFileHandler(
        os.path.join(logs_dir, 'admin.log'),
        maxBytes=10*1024*1024,
        backupCount=5,
        encoding='utf-8'
    )
    admin_file_handler.setFormatter(detailed_formatter)

    db_file_handler = RotatingFileHandler(
        os.path.join(logs_dir, 'database.log'),
        maxBytes=10*1024*1024,
        backupCount=3,
        encoding='utf-8'
    )
    db_file_handler.setFormatter(standard_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(standard_formatter)
    
    # Add handlers to loggers
    app_logger.addHandler(console_handler)
    app_logger.addHandler(app_file_handler)
    
    security_logger.addHandler(security_file_handler)
    security_logger.addHandler(console_handler)
    
    admin_logger.addHandler(admin_file_handler)
    admin_logger.addHandler(console_handler)
    
    db_logger.addHandler(db_file_handler)
    
    # Prevent log propagation to root logger
    for logger in [app_logger, security_logger, admin_logger, db_logger]:
        logger.propagate = False
    
    # Mark as initialized and cache loggers
    _initialized = True
    _loggers = {
        'app': app_logger,
        'security': security_logger,
        'admin': admin_logger,
        'database': db_logger
    }
    
    # Log initialization
    app_logger.info("=" * 60)
    app_logger.info("LOGGING SYSTEM INITIALIZED")
    app_logger.info(f"Logs directory: {logs_dir}")
    app_logger.info("=" * 60)
    
    return _loggers


def get_logger(name='app'):
    """
    Get a logger by name
    
    Args:
        name: Logger name ('app', 'security', 'admin', 'database')
    
    Returns:
        logging.Logger: Requested logger
    """
    loggers = setup_logging()
    return loggers.get(name, loggers['app'])
