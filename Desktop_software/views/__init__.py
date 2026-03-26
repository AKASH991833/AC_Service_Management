"""
Views module for AC Service Billing Software - PySide6 Edition
"""
from .login_view import LoginWindow
from .main_window import MainWindow
from .enhanced_dashboard_view import EnhancedDashboardView
from .invoice_view import InvoiceView
from .customer_view import CustomerView
from .amc_view import AMCView
from .technician_view import TechnicianView
from .settings_view import SettingsView, ProfileSettingsView, ChangePasswordDialog

# Legacy imports for backward compatibility
MainView = MainWindow
MasterDataView = SettingsView
ChangePasswordView = ChangePasswordDialog
DashboardView = EnhancedDashboardView  # Alias for backward compatibility

__all__ = [
    'LoginWindow',
    'MainWindow',
    'MainView',  # Legacy alias
    'DashboardView',
    'EnhancedDashboardView',
    'InvoiceView',
    'CustomerView',
    'AMCView',
    'TechnicianView',
    'SettingsView',
    'MasterDataView',  # Legacy alias
    'ProfileSettingsView',
    'ChangePasswordDialog',
    'ChangePasswordView'  # Legacy alias
]