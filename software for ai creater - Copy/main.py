"""
Main entry point for AC Service Billing Software - PySide6 Edition
Professional Qt-based UI with modern design
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QPixmap

from config import APP_NAME, APP_VERSION
from database.db_connection import DatabaseConnection

# ============================================================================
# LOGIN SYSTEM CONFIGURATION
# ============================================================================
# Set to True to enable login system (Production mode)
# Set to False to bypass login and go directly to main window (Testing mode)
# ============================================================================
LOGIN_ENABLED = False  # Disabled for development - enable for production
# ============================================================================


class Application:
    """Main application class for PySide6-based AC Service Billing"""

    def __init__(self):
        # Initialize Qt application
        self.app = QApplication(sys.argv)
        self.app.setApplicationName(APP_NAME)
        self.app.setApplicationVersion(APP_VERSION)

        # Set application-wide font
        font = QFont('Segoe UI', 10)
        self.app.setFont(font)

        # Initialize database connection
        self.db = None
        self.main_window = None
        self.login_window = None
        self.user_data = None

        # Setup database
        self._setup_database()

        # Show splash screen
        self._show_splash()

        # Show login window after splash (or bypass if disabled)
        QTimer.singleShot(2000, self._show_login)

    def _setup_database(self):
        """Initialize database connection"""
        try:
            self.db = DatabaseConnection()
            print("[OK] Database connected successfully")
        except Exception as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.critical(
                None,
                "Database Error",
                f"Cannot connect to database:\n{str(e)}\n\nPlease check your database configuration."
            )
            sys.exit(1)

    def _show_splash(self):
        """Show application splash screen"""
        try:
            # Try multiple logo paths to handle case sensitivity
            splash_pix = QPixmap('assets/logo.png')
            if splash_pix.isNull():
                splash_pix = QPixmap('assets/Logo.png')
            if splash_pix.isNull():
                # Create default splash
                splash_pix = QPixmap(400, 300)
                splash_pix.fill(Qt.GlobalColor.white)

            self.splash = QSplashScreen(splash_pix, Qt.WindowType.WindowStaysOnTopHint)
            self.splash.showMessage(
                f"\n\n{APP_NAME}\nVersion {APP_VERSION}\n\nStarting...",
                Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter,
                Qt.GlobalColor.darkBlue
            )
            self.splash.show()
            self.app.processEvents()
        except Exception as e:
            print(f"Splash screen error: {e}")
            self.splash = None

    def _show_login(self):
        """Show login window or bypass based on LOGIN_ENABLED setting"""
        if LOGIN_ENABLED:
            # Login enabled - show login window
            print("[INFO] Login system ENABLED")
            if self.splash:
                self.splash.finish(self.app.activeWindow() if self.app.activeWindow() else None)

            from views.login_view import LoginWindow
            self.login_window = LoginWindow(on_login_success=self._on_login_success)
            self.login_window.show()
        else:
            # Login bypassed - showing main window directly
            print("[INFO] Login system BYPASSED (Development mode)")
            if self.splash:
                self.splash.finish(self.app.activeWindow() if self.app.activeWindow() else None)

            self._show_main_window_direct()

    def _on_login_success(self, user_data):
        """Handle successful login"""
        self.user_data = user_data

        # Close login window
        if self.login_window:
            self.login_window.close()
            self.login_window = None

        # Show main window
        self._show_main_window()

    def _show_main_window(self):
        """Show main application window with authenticated user data"""
        from views.main_window import MainWindow

        self.main_window = MainWindow(
            user_data=self.user_data,
            on_logout=self._on_logout
        )
        self.main_window.show()

    def _show_main_window_direct(self):
        """Show main window directly without login - fetches admin user from DB"""
        from views.main_window import MainWindow
        from database.db_connection import DatabaseConnection

        # Fetch admin user from database for development
        admin_user = None
        try:
            db = DatabaseConnection()
            query = "SELECT id, username, full_name, email, phone, is_active FROM users WHERE username = %s AND is_active = TRUE"
            user_result = db.execute_query(query, ('admin',), fetch_one=True)

            if user_result:
                admin_user = user_result
                print(f"[MAIN] Loaded admin user from DB: {admin_user}")
            else:
                # Fallback only if DB query fails
                admin_user = {
                    'id': 1,
                    'username': 'admin',
                    'full_name': 'Admin User',
                    'email': 'admin@anshaircool.com',
                    'phone': '9918331262'
                }
                print(f"[MAIN] Using fallback admin user (DB query returned no results)")
        except Exception as e:
            print(f"[MAIN] Error fetching admin from DB, using fallback: {e}")
            admin_user = {
                'id': 1,
                'username': 'admin',
                'full_name': 'Admin User',
                'email': 'admin@anshaircool.com',
                'phone': '9918331262'
            }

        # Initialize session with fetched user data
        from utils.session_manager import get_session
        session = get_session()
        session.login(admin_user)

        if self.splash:
            self.splash.finish(self.app.activeWindow() if self.app.activeWindow() else None)

        self.main_window = MainWindow(
            user_data=admin_user,
            on_logout=self._on_logout
        )
        self.main_window.show()

    def _on_logout(self):
        """Handle logout"""
        # Close main window
        if self.main_window:
            self.main_window.close()
            self.main_window = None

        # Show login window again
        self._show_login()

    def run(self):
        """Start the application"""
        sys.exit(self.app.exec())


def main():
    """Main entry point"""
    # Note: High DPI scaling is enabled by default in PySide6 6.0+
    # No need to set attributes manually (deprecated in Qt 6)

    # Create and run application
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
