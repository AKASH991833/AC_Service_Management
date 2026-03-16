"""
Main Application Window - PySide6 Professional UI
Modern sidebar navigation with stacked widget content area
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFrame,
    QLabel, QPushButton, QStackedWidget, QScrollArea, QSizePolicy,
    QStatusBar, QMenu, QMessageBox, QGraphicsDropShadowEffect, QSpacerItem,
    QGraphicsOpacityEffect
)
from PySide6.QtCore import Qt, Signal, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QPixmap, QIcon, QAction, QPalette, QColor

from utils.unified_theme import UnifiedTheme
from views.base_window import BaseView

# TYPE_CHECKING import to avoid circular dependency
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from views.enhanced_dashboard_view import EnhancedDashboardView


class MainWindow(QMainWindow):
    """Main application window with sidebar navigation - Modern Windows 11 Style"""

    logout_requested = Signal()

    def __init__(self, user_data, on_logout=None):
        super().__init__()
        self.user_data = user_data
        self.on_logout = on_logout
        self.theme_manager = UnifiedTheme()  # Use unified theme
        self.current_view_index = 0

        # Set window name and modern styling
        self.setObjectName("mainWindow")
        self.setWindowTitle(f"Ansh Air Cool - Billing System | {user_data.get('full_name', 'User')}")
        self.setMinimumSize(1280, 720)
        self.resize(1440, 800)

        # Apply unified cyan/blue theme stylesheet
        self.setStyleSheet(self.theme_manager.get_main_stylesheet())

        # Enable acrylic-like effect (Windows 11 style)
        self._setup_modern_window_effects()

        # Center window
        self._center_window()

        # Setup UI
        self._setup_ui()

        # Show dashboard by default
        self._show_dashboard()
    
    def _center_window(self):
        """Center window on screen"""
        from PySide6.QtWidgets import QApplication
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def _setup_modern_window_effects(self):
        """Setup modern window effects (shadows, transparency, etc.)"""
        # Set window background
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(15, 15, 15))
        self.setPalette(palette)

        # Add drop shadow effect to main window
        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(30)
        shadow_effect.setColor(QColor(0, 0, 0, 128))
        shadow_effect.setOffset(0, 0)
        self.setGraphicsEffect(shadow_effect)

    def _setup_ui(self):
        """Setup main application UI"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        self._create_header(main_layout)
        
        # Content area (sidebar + main content)
        content_frame = QFrame()
        content_frame.setObjectName("contentFrame")
        main_layout.addWidget(content_frame, 1)
        
        content_layout = QHBoxLayout(content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Sidebar
        self._create_sidebar(content_layout)
        
        # Main content area
        self._create_content_area(content_layout)
        
        # Status bar
        self._create_status_bar()
    
    def _create_header(self, parent_layout):
        """Create application header"""
        colors = self.theme_manager.get_colors()
        
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_frame.setFixedHeight(70)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 10, 20, 10)
        header_layout.setSpacing(20)
        
        # Logo and title (left)
        logo_layout = QHBoxLayout()
        logo_layout.setSpacing(12)
        
        try:
            logo_path = 'assets/Logo.png'
            from PySide6.QtGui import QPixmap
            from PySide6.QtCore import Qt
            import os
            if os.path.exists(logo_path):
                logo_label = QLabel()
                pixmap = QPixmap(logo_path).scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio,
                                                    Qt.TransformationMode.SmoothTransformation)
                logo_label.setPixmap(pixmap)
                logo_layout.addWidget(logo_label)
            else:
                logo_label = QLabel("❄️")
                logo_label.setFont(QFont('Segoe UI', 20))
                logo_layout.addWidget(logo_label)
        except Exception:
            logo_label = QLabel("❄️")
            logo_label.setFont(QFont('Segoe UI', 20))
            logo_layout.addWidget(logo_label)
        
        title_label = QLabel("AC Service Billing")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18pt;
                font-weight: bold;
                color: white;
            }
        """)
        logo_layout.addWidget(title_label)
        header_layout.addLayout(logo_layout)

        # REMOVED: Top navigation buttons (now using sidebar only)
        # Navigation moved to sidebar for cleaner modern UI

        header_layout.addStretch()

        # Profile section (right)
        profile_layout = QHBoxLayout()
        profile_layout.setSpacing(15)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setObjectName("iconButton")
        refresh_btn.setStyleSheet("""
            QPushButton#iconButton {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 9pt;
            }
            QPushButton#iconButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)
        refresh_btn.clicked.connect(self._refresh_current_view)
        profile_layout.addWidget(refresh_btn)

        # Welcome label
        first_name = self.user_data.get('full_name', 'User').split()[0]
        welcome_label = QLabel(f"Welcome, {first_name}")
        welcome_label.setStyleSheet("color: white; font-size: 10pt;")
        profile_layout.addWidget(welcome_label)

        # Profile menu button
        profile_btn = QPushButton()
        profile_btn.setObjectName("profileBtn")
        profile_btn.setFixedSize(42, 42)
        profile_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        # Create icon label with emoji
        icon_label = QLabel("⚙️")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("color: white; font-size: 18pt;")

        # Layout for button
        btn_layout = QVBoxLayout(profile_btn)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.addWidget(icon_label)

        profile_btn.setStyleSheet("""
            QPushButton#profileBtn {
                background-color: rgba(255, 255, 255, 0.15);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 21px;
                padding: 0px;
            }
            QPushButton#profileBtn:hover {
                background-color: rgba(255, 255, 255, 0.25);
                border-color: rgba(255, 255, 255, 0.4);
            }
            QPushButton#profileBtn:pressed {
                background-color: rgba(255, 255, 255, 0.3);
            }
        """)
        
        # Profile menu
        self.profile_menu = QMenu(self)
        self.profile_menu.setStyleSheet("")

        profile_action = QAction("Profile Settings", self)
        profile_action.triggered.connect(self._show_profile_settings)
        self.profile_menu.addAction(profile_action)

        password_action = QAction("Change Password", self)
        password_action.triggered.connect(self._show_change_password)
        self.profile_menu.addAction(password_action)

        self.profile_menu.addSeparator()

        logout_action = QAction("🚪 Logout", self)
        logout_action.triggered.connect(self._confirm_logout)
        self.profile_menu.addAction(logout_action)

        profile_btn.setMenu(self.profile_menu)
        profile_layout.addWidget(profile_btn)
        
        header_layout.addLayout(profile_layout)
        
        parent_layout.addWidget(header_frame)
    
    def _create_sidebar(self, parent_layout):
        """Create sidebar navigation"""
        colors = self.theme_manager.get_colors()
        
        sidebar_frame = QFrame()
        sidebar_frame.setObjectName("sidebarFrame")
        sidebar_frame.setFixedWidth(220)
        sidebar_layout = QVBoxLayout(sidebar_frame)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(8)
        
        # Sidebar navigation buttons
        self.sidebar_buttons = {}
        
        nav_items = [
            ("📊", "Dashboard", lambda: self._switch_to_view("dashboard")),
            ("📝", "Invoice", lambda: self._switch_to_view("invoice")),
            ("📋", "Manage Invoices", lambda: self._switch_to_view("invoice management")),
            ("📝", "AMC Contracts", lambda: self._switch_to_view("amc")),
            ("👥", "Customers", lambda: self._switch_to_view("customers")),
            ("🔧", "Technicians", lambda: self._switch_to_view("technicians")),
            ("🌐", "Online Requests", lambda: self._switch_to_view("online requests")),
            ("⚙️", "Settings", lambda: self._switch_to_view("settings")),
        ]
        
        for icon, text, handler in nav_items:
            btn = QPushButton(f"{icon}  {text}")
            btn.setObjectName("sidebarButton")
            btn.setCheckable(True)
            btn.setAutoExclusive(True)  # Only one button checked at a time
            btn.setMinimumHeight(45)
            btn.clicked.connect(handler)
            sidebar_layout.addWidget(btn)
            self.sidebar_buttons[text.lower()] = btn
        
        sidebar_layout.addStretch()
        
        # App version at bottom
        version_label = QLabel("v1.0.0")
        version_label.setStyleSheet("""
            color: #64748b;
            font-size: 9pt;
            padding: 10px;
        """)
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(version_label)
        
        parent_layout.addWidget(sidebar_frame)
    
    def _create_content_area(self, parent_layout):
        """Create main content area with stacked widget"""
        # Content frame
        content_frame = QFrame()
        content_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.theme_manager.get_colors()['bg']};
            }}
        """)
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Stacked widget for views
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: transparent;")
        content_layout.addWidget(self.stacked_widget)
        
        parent_layout.addWidget(content_frame, 1)
    
    def _create_status_bar(self):
        """Create status bar"""
        self.status_bar = QStatusBar()
        self.status_bar.setObjectName("statusBarFrame")
        self.setStatusBar(self.status_bar)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_bar.addWidget(self.status_label)
        
        self.status_bar.addPermanentWidget(QLabel("● Database Connected"))
        permanent_widget = self.status_bar.children()[1]
        if permanent_widget:
            permanent_widget.setStyleSheet("color: #22c55e; font-weight: bold;")
    
    def _clear_stacked_widget(self):
        """Clear all widgets from stacked widget"""
        while self.stacked_widget.count():
            widget = self.stacked_widget.widget(0)
            self.stacked_widget.removeWidget(widget)
            widget.deleteLater()
    
    def _show_dashboard(self):
        """Show enhanced dashboard view with clickable cards"""
        # Check if dashboard already exists
        for i in range(self.stacked_widget.count()):
            widget = self.stacked_widget.widget(i)
            if widget and widget.__class__.__name__ == 'EnhancedDashboardView':
                # Dashboard exists - just switch to it and refresh
                self.stacked_widget.setCurrentIndex(i)
                widget.refresh_data()  # Refresh the data
                self._update_navigation("dashboard")
                self.status_label.setText("Dashboard")
                return
        
        # Dashboard doesn't exist - create new one
        from views.enhanced_dashboard_view import EnhancedDashboardView
        view = EnhancedDashboardView(self.user_data)
        self.stacked_widget.addWidget(view)
        self._update_navigation("dashboard")
        self.status_label.setText("Dashboard")
    
    def _show_invoice(self):
        """Show invoice view"""
        # Check if invoice view already exists
        for i in range(self.stacked_widget.count()):
            widget = self.stacked_widget.widget(i)
            if widget and widget.__class__.__name__ == 'InvoiceView':
                self.stacked_widget.setCurrentIndex(i)
                self._update_navigation("invoice")
                self.status_label.setText("New Invoice")
                return
        
        from views.invoice_view import InvoiceView
        view = InvoiceView()
        self.stacked_widget.addWidget(view)
        self._update_navigation("invoice")
        self.status_label.setText("New Invoice")

    def _show_amc(self):
        """Show AMC view"""
        # Check if AMC view already exists
        for i in range(self.stacked_widget.count()):
            widget = self.stacked_widget.widget(i)
            if widget and widget.__class__.__name__ == 'AMCView':
                self.stacked_widget.setCurrentIndex(i)
                self._update_navigation("amc")
                self.status_label.setText("AMC Contracts")
                return
        
        from views.amc_view import AMCView
        view = AMCView()
        self.stacked_widget.addWidget(view)
        self._update_navigation("amc")
        self.status_label.setText("AMC Contracts")

    def _show_customers(self):
        """Show customers view"""
        # Check if customers view already exists
        for i in range(self.stacked_widget.count()):
            widget = self.stacked_widget.widget(i)
            if widget and widget.__class__.__name__ == 'CustomerView':
                self.stacked_widget.setCurrentIndex(i)
                self._update_navigation("customers")
                self.status_label.setText("Customer Management")
                return
        
        from views.customer_view import CustomerView
        view = CustomerView()
        self.stacked_widget.addWidget(view)
        self._update_navigation("customers")
        self.status_label.setText("Customer Management")

    def _show_technicians(self):
        """Show technicians view"""
        # Check if technicians view already exists
        for i in range(self.stacked_widget.count()):
            widget = self.stacked_widget.widget(i)
            if widget and widget.__class__.__name__ == 'TechnicianView':
                self.stacked_widget.setCurrentIndex(i)
                self._update_navigation("technicians")
                self.status_label.setText("Technician Management")
                return
        
        from views.technician_view import TechnicianView
        view = TechnicianView()
        self.stacked_widget.addWidget(view)
        self._update_navigation("technicians")
        self.status_label.setText("Technician Management")

    def _show_online_requests(self):
        """Show online requests view"""
        # Check if online requests view already exists
        for i in range(self.stacked_widget.count()):
            widget = self.stacked_widget.widget(i)
            if widget and widget.__class__.__name__ == 'OnlineRequestView':
                self.stacked_widget.setCurrentIndex(i)
                self._update_navigation("online requests")
                self.status_label.setText("Online Requests")
                return

        from database.db_connection import DatabaseConnection
        from controllers.online_request_controller import OnlineRequestController
        from views.online_request_view import OnlineRequestView

        db = DatabaseConnection()
        controller = OnlineRequestController(db)
        view = OnlineRequestView(db, controller)
        self.stacked_widget.addWidget(view)
        self._update_navigation("online requests")
        self.status_label.setText("Online Requests")

    def _switch_to_view(self, view_name):
        """Helper to switch views with proper cleanup"""
        current_widget = self.stacked_widget.currentWidget()
        
        # Cleanup OnlineRequestView timer if active
        if current_widget and hasattr(current_widget, 'cleanup'):
            try:
                current_widget.cleanup()
            except Exception as e:
                print(f"[WARN] Cleanup failed: {e}")
        
        # Now call the appropriate show method based on view name
        if view_name == "online requests":
            self._show_online_requests()
        elif view_name == "dashboard":
            self._show_dashboard()
        elif view_name == "invoice":
            self._show_invoice()
        elif view_name == "invoice management":
            self._show_invoice_management()
        elif view_name == "amc":
            self._show_amc()
        elif view_name == "customers":
            self._show_customers()
        elif view_name == "technicians":
            self._show_technicians()
        elif view_name == "settings":
            self._show_settings()

    def _show_settings(self):
        """Show settings view"""
        # Check if settings already exists
        for i in range(self.stacked_widget.count()):
            widget = self.stacked_widget.widget(i)
            if widget and widget.__class__.__name__ == 'SettingsView':
                # Settings exists - just switch to it
                self.stacked_widget.setCurrentIndex(i)
                self._update_navigation("settings")
                self.status_label.setText("Settings")
                return
        
        # Settings doesn't exist - create new one
        from views.settings_view import SettingsView
        view = SettingsView(self.user_data)
        # Connect settings_saved signal to refresh dashboard
        view.settings_saved.connect(self._on_settings_saved)
        self.stacked_widget.addWidget(view)
        self._update_navigation("settings")
        self.status_label.setText("Settings")
    
    def _show_invoice_management(self):
        """Show invoice management page"""
        # Check if invoice management view already exists
        for i in range(self.stacked_widget.count()):
            widget = self.stacked_widget.widget(i)
            if widget and widget.__class__.__name__ == 'InvoiceManagementView':
                self.stacked_widget.setCurrentIndex(i)
                self._update_navigation("invoice management")
                self.status_label.setText("Manage Invoices")
                return
        
        from views.invoice_management_view import InvoiceManagementView
        view = InvoiceManagementView()
        self.stacked_widget.addWidget(view)
        self._update_navigation("invoice management")
        self.status_label.setText("Manage Invoices")

    def _show_profile_settings(self):
        """Show profile settings"""
        # Check if profile settings view already exists
        for i in range(self.stacked_widget.count()):
            widget = self.stacked_widget.widget(i)
            if widget and widget.__class__.__name__ == 'ProfileSettingsView':
                self.stacked_widget.setCurrentIndex(i)
                self._update_navigation("settings")
                self.status_label.setText("Profile Settings")
                return
        
        from views.settings_view import ProfileSettingsView
        view = ProfileSettingsView(self.user_data)
        self.stacked_widget.addWidget(view)
        self._update_navigation("settings")
        self.status_label.setText("Profile Settings")
    
    def _show_change_password(self):
        """Show change password dialog"""
        from views.settings_view import ChangePasswordDialog
        dialog = ChangePasswordDialog(self.user_data.get('id'), self)
        dialog.exec()

    def _refresh_current_view(self):
        """Refresh current view and apply theme"""
        current_widget = self.stacked_widget.currentWidget()
        if current_widget:
            # Call update_theme_colors if method exists (for InvoiceView and AMCView)
            if hasattr(current_widget, 'update_theme_colors'):
                current_widget.update_theme_colors()
                self.status_label.setText(f"Theme updated in {type(current_widget).__name__}")
            elif hasattr(current_widget, 'theme_manager'):
                # Apply theme to current widget
                colors = current_widget.theme_manager.get_colors()
                current_widget.setStyleSheet(
                    current_widget.theme_manager.get_main_stylesheet()
                )
                # Refresh data if method exists
                if hasattr(current_widget, 'refresh_data'):
                    current_widget.refresh_data()
                self.status_label.setText(f"Theme applied to {type(current_widget).__name__}")
            else:
                self.status_label.setText("View doesn't support theme refresh")
        else:
            self.status_label.setText("No active view to refresh")

    def _on_settings_saved(self):
        """Handle settings saved event - refresh dashboard data and update user_data"""
        print(f"[DEBUG] Settings saved signal received - refreshing dashboard")
        
        # CRITICAL: Refresh user_data from session manager to get latest profile data
        from utils.session_manager import get_session
        session = get_session()
        if session and session.get_current_user():
            updated_user = session.get_current_user()
            self.user_data = updated_user.copy()  # Make a copy to avoid reference issues
            print(f"[MAIN_WINDOW] Updated user_data from session: {self.user_data}")
            
            # Update window title with new user name
            first_name = self.user_data.get('full_name', 'User').split()[0]
            self.setWindowTitle(f"Ansh Air Cool - Billing System | {first_name}")
            
            # Update welcome label in header if it exists
            header = self.findChild(QFrame, "headerFrame")
            if header:
                for widget in header.findChildren(QLabel):
                    if widget.text().startswith("Welcome,"):
                        widget.setText(f"Welcome, {first_name}")
                        break
        
        # Find dashboard and refresh it
        for i in range(self.stacked_widget.count()):
            widget = self.stacked_widget.widget(i)
            if widget and widget.__class__.__name__ == 'EnhancedDashboardView':
                print(f"[DEBUG] Found dashboard, calling refresh_data()")
                widget.refresh_data()
                break
        self.status_label.setText("Settings saved - Dashboard refreshed")
    
    def _confirm_logout(self):
        """Confirm and perform logout"""
        from PySide6.QtWidgets import QMessageBox
        
        result = QMessageBox.question(
            self, "Logout",
            "Are you sure you want to logout?\n\nAll unsaved changes will be lost.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if result == QMessageBox.StandardButton.Yes:
            # Clear session
            from utils.session_manager import logout_user
            logout_user()
            
            print("[INFO] User logged out successfully")
            
            if self.on_logout:
                self.on_logout()
            self.logout_requested.emit()
    
    def _update_navigation(self, view_name):
        """Update navigation button states"""
        for name, btn in self.sidebar_buttons.items():
            btn.blockSignals(True)  # Block signals while updating
            btn.setChecked(name == view_name.lower())
            btn.blockSignals(False)  # Re-enable signals

    def closeEvent(self, event):
        """Handle application close - cleanup all views"""
        # Clear stacked widget and cleanup views
        while self.stacked_widget.count():
            widget = self.stacked_widget.widget(0)
            self.stacked_widget.removeWidget(widget)
            if hasattr(widget, '_cleanup_workers'):
                widget._cleanup_workers()
            widget.deleteLater()
        super().closeEvent(event)
