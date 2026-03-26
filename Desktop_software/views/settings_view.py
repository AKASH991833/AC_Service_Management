"""
Settings View - PySide6 Settings and Master Data Management
Professional settings interface with profile, shop details, and master data
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea,
    QSizePolicy, QTabWidget, QComboBox, QDoubleSpinBox, QSpinBox,
    QTextEdit, QFormLayout, QMessageBox, QDialog,
    QDialogButtonBox, QCheckBox
)
from PySide6.QtCore import Qt, Signal

from utils.unified_theme import UnifiedTheme
from views.base_window import BaseView


class QWidgetWrapper(QWidget):
    """Simple wrapper class for QWidget layouts"""
    def __init__(self, layout):
        super().__init__()
        self.setLayout(layout)


class SettingsView(BaseView):
    """Settings and master data management view"""
    
    # Signal emitted when settings are saved
    settings_saved = Signal()

    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data

        self._setup_ui()
        self.load_user_profile()

    def update_theme_colors(self):
        """Update theme colors for proper dark theme support"""
        colors = self.theme_manager.get_colors()
        
        # Apply QPalette colors
        self.theme_manager.apply_palette(self)
        
        # Apply stylesheet
        self.setStyleSheet(self.theme_manager.get_main_stylesheet())
        
        # Apply theme directly to table for proper alternating colors
        if hasattr(self, 'master_table'):
            self.theme_manager.apply_table_theme(self.master_table)
        
        # Refresh data
        self.load_user_profile()

    def _setup_ui(self):
        """Setup settings UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Header
        header_label = QLabel("⚙️ SETTINGS")
        header_label.setStyleSheet("""
            font-size: 24pt;
            font-weight: bold;
            color: #60a5fa;
            background: linear-gradient(135deg, #60a5fa, #a78bfa);
            padding: 10px;
        """)
        main_layout.addWidget(header_label)

        subtitle_label = QLabel("Configure your profile, shop details, and application settings")
        subtitle_label.setStyleSheet("""
            font-size: 11pt;
            color: #94a3b8;
            padding: 5px 10px;
        """)
        main_layout.addWidget(subtitle_label)

        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #334155;
                border-radius: 8px;
                background-color: #1e293b;
            }
            QTabBar::tab {
                background-color: #334155;
                color: #94a3b8;
                padding: 12px 24px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: bold;
                font-size: 10pt;
            }
            QTabBar::tab:selected {
                background-color: #3b82f6;
                color: white;
            }
            QTabBar::tab:hover {
                background-color: #475569;
            }
        """)

        # Tab 1: User Profile
        self.user_tab = self._create_user_profile_tab()
        self.tabs.addTab(self.user_tab, "👤 User Profile")

        # Tab 2: Shop Details
        self.shop_tab = self._create_shop_details_tab()
        self.tabs.addTab(self.shop_tab, "🏪 Shop Details")

        # Tab 3: Application Settings
        self.app_tab = self._create_app_settings_tab()
        self.tabs.addTab(self.app_tab, "⚙️ Application")

        # Tab 4: Master Data
        self.master_tab = self._create_master_data_tab()
        self.tabs.addTab(self.master_tab, "📊 Master Data")

        main_layout.addWidget(self.tabs)
    
    def _create_user_profile_tab(self):
        """Create user profile tab"""
        colors = self.theme_manager.get_colors()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background-color: transparent;")

        content = QWidget()
        content.setStyleSheet("""
            QWidget {
                background-color: #1e293b;
            }
            QLabel {
                color: white;
            }
            QLineEdit {
                background-color: #334155;
                color: white;
                border: 1px solid #475569;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 10pt;
            }
            QLineEdit:focus {
                border: 2px solid #3b82f6;
            }
        """)
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # User Info
        info_group = self._create_group_box("User Information")
        info_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 11pt;
                border: 2px solid #475569;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 16px;
                background-color: #334155;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 12px;
                padding: 0 8px;
                color: #60a5fa;
                font-size: 12pt;
            }
        """)
        info_layout = QFormLayout()
        info_layout.setSpacing(15)
        info_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)

        # Username (read-only)
        self.username_label = QLabel(self.user_data.get('username', ''))
        self.username_label.setStyleSheet("font-weight: bold; color: #60a5fa;")
        info_layout.addRow("Username:", self.username_label)

        # Full Name
        self.full_name_input = QLineEdit()
        info_layout.addRow("Full Name:", self.full_name_input)

        # Email
        self.email_input = QLineEdit()
        info_layout.addRow("Email:", self.email_input)

        # Phone
        self.phone_input = QLineEdit()
        info_layout.addRow("Phone:", self.phone_input)

        # Status
        self.status_label = QLabel("● Active")
        self.status_label.setStyleSheet("color: #10b981; font-weight: bold;")
        info_layout.addRow("Status:", self.status_label)

        info_group.layout().addLayout(info_layout)
        layout.addWidget(info_group)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        save_btn = QPushButton("💾 Save Profile")
        save_btn.setObjectName("successButton")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 11pt;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
            QPushButton:pressed {
                background-color: #047857;
            }
        """)
        save_btn.clicked.connect(self.save_user_profile)
        btn_layout.addWidget(save_btn)

        layout.addLayout(btn_layout)
        layout.addStretch()

        scroll.setWidget(content)
        return scroll
    
    def _create_shop_details_tab(self):
        """Create shop details tab"""
        colors = self.theme_manager.get_colors()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background-color: transparent;")

        content = QWidget()
        content.setStyleSheet("""
            QWidget {
                background-color: #1e293b;
            }
            QLabel {
                color: white;
            }
            QLineEdit {
                background-color: #334155;
                color: white;
                border: 1px solid #475569;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 10pt;
            }
            QLineEdit:focus {
                border: 2px solid #3b82f6;
            }
            QTextEdit {
                background-color: #334155;
                color: white;
                border: 1px solid #475569;
                border-radius: 6px;
                padding: 8px;
            }
            QTextEdit:focus {
                border: 2px solid #3b82f6;
            }
        """)
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # Shop Details
        shop_group = self._create_group_box("Shop Details")
        shop_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 11pt;
                border: 2px solid #475569;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 16px;
                background-color: #334155;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 12px;
                padding: 0 8px;
                color: #60a5fa;
                font-size: 12pt;
            }
        """)
        shop_layout = QFormLayout()
        shop_layout.setSpacing(15)
        shop_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)

        self.shop_name_input = QLineEdit()
        shop_layout.addRow("Shop Name *:", self.shop_name_input)

        self.address_input = QTextEdit()
        self.address_input.setMaximumHeight(80)
        shop_layout.addRow("Address *:", self.address_input)

        self.shop_phone_input = QLineEdit()
        shop_layout.addRow("Phone:", self.shop_phone_input)

        self.shop_email_input = QLineEdit()
        shop_layout.addRow("Email:", self.shop_email_input)

        self.gst_input = QLineEdit()
        shop_layout.addRow("GST Number:", self.gst_input)

        shop_group.layout().addLayout(shop_layout)
        layout.addWidget(shop_group)

        # Owner Details
        owner_group = self._create_group_box("Owner Details")
        owner_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 11pt;
                border: 2px solid #475569;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 16px;
                background-color: #334155;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 12px;
                padding: 0 8px;
                color: #60a5fa;
                font-size: 12pt;
            }
        """)
        owner_layout = QFormLayout()
        owner_layout.setSpacing(15)
        owner_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)

        self.owner_name_input = QLineEdit()
        owner_layout.addRow("Owner Name *:", self.owner_name_input)

        self.owner_phone_input = QLineEdit()
        owner_layout.addRow("Owner Phone:", self.owner_phone_input)

        owner_group.layout().addLayout(owner_layout)
        layout.addWidget(owner_group)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        save_btn = QPushButton("💾 Save Shop Details")
        save_btn.setObjectName("successButton")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 11pt;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
            QPushButton:pressed {
                background-color: #047857;
            }
        """)
        save_btn.clicked.connect(self.save_shop_details)
        btn_layout.addWidget(save_btn)

        layout.addLayout(btn_layout)
        layout.addStretch()

        scroll.setWidget(content)
        return scroll
    
    def _create_app_settings_tab(self):
        """Create application settings tab"""
        colors = self.theme_manager.get_colors()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background-color: transparent;")

        content = QWidget()
        content.setStyleSheet("""
            QWidget {
                background-color: #1e293b;
            }
            QLabel {
                color: white;
            }
            QLineEdit {
                background-color: #334155;
                color: white;
                border: 1px solid #475569;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 10pt;
            }
            QLineEdit:focus {
                border: 2px solid #3b82f6;
            }
            QSpinBox, QDoubleSpinBox {
                background-color: #334155;
                color: white;
                border: 1px solid #475569;
                border-radius: 6px;
                padding: 8px;
                font-size: 10pt;
            }
            QSpinBox:focus, QDoubleSpinBox:focus {
                border: 2px solid #3b82f6;
            }
        """)
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # Invoice Settings
        invoice_group = self._create_group_box("Invoice Settings")
        invoice_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 11pt;
                border: 2px solid #475569;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 16px;
                background-color: #334155;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 12px;
                padding: 0 8px;
                color: #60a5fa;
                font-size: 12pt;
            }
        """)
        invoice_layout = QFormLayout()
        invoice_layout.setSpacing(15)
        invoice_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)

        self.invoice_prefix_input = QLineEdit("INV")
        invoice_layout.addRow("Invoice Prefix:", self.invoice_prefix_input)

        self.invoice_start_spin = QSpinBox()
        self.invoice_start_spin.setRange(1, 999999)
        self.invoice_start_spin.setValue(1001)
        invoice_layout.addRow("Starting Number:", self.invoice_start_spin)

        self.gst_spin = QDoubleSpinBox()
        self.gst_spin.setRange(0, 100)
        self.gst_spin.setValue(18.0)
        self.gst_spin.setSuffix("%")
        invoice_layout.addRow("GST Percentage:", self.gst_spin)

        invoice_group.layout().addLayout(invoice_layout)
        layout.addWidget(invoice_group)

        # Backup Settings
        backup_group = self._create_group_box("Backup Settings")
        backup_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 11pt;
                border: 2px solid #475569;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 16px;
                background-color: #334155;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 12px;
                padding: 0 8px;
                color: #60a5fa;
                font-size: 12pt;
            }
        """)
        backup_layout = QVBoxLayout()

        backup_info = QLabel("Create regular backups of your data to prevent data loss.")
        backup_info.setWordWrap(True)
        backup_info.setStyleSheet("color: #94a3b8; font-size: 10pt;")
        backup_layout.addWidget(backup_info)

        btn_layout = QHBoxLayout()

        backup_btn = QPushButton("💾 Create Backup")
        backup_btn.setObjectName("primaryButton")
        backup_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 11pt;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
        """)
        backup_btn.clicked.connect(self.create_backup)
        btn_layout.addWidget(backup_btn)

        restore_btn = QPushButton("📥 Restore Backup")
        restore_btn.setObjectName("secondaryButton")
        restore_btn.setStyleSheet("""
            QPushButton {
                background-color: #6b7280;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 11pt;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #4b5563;
            }
            QPushButton:pressed {
                background-color: #374151;
            }
        """)
        restore_btn.clicked.connect(self.restore_backup)
        btn_layout.addWidget(restore_btn)

        btn_layout.addStretch()
        backup_layout.addLayout(btn_layout)

        backup_group.layout().addLayout(backup_layout)
        layout.addWidget(backup_group)

        # Database Settings
        db_group = self._create_group_box("Database")
        db_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 11pt;
                border: 2px solid #475569;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 16px;
                background-color: #334155;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 12px;
                padding: 0 8px;
                color: #60a5fa;
                font-size: 12pt;
            }
        """)
        db_layout = QVBoxLayout()

        db_status = QLabel("● Database Connected")
        db_status.setStyleSheet("color: #10b981; font-weight: bold; font-size: 11pt;")
        db_layout.addWidget(db_status)

        db_info = QLabel("Database: ac_service_billing | Host: localhost")
        db_info.setStyleSheet("color: #94a3b8; font-size: 10pt;")
        db_layout.addWidget(db_info)

        db_group.layout().addLayout(db_layout)
        layout.addWidget(db_group)

        layout.addStretch()
        scroll.setWidget(content)
        return scroll
    
    def _create_master_data_tab(self):
        """Create master data management tab"""
        colors = self.theme_manager.get_colors()

        layout = QVBoxLayout()

        # Master data type selector
        selector_layout = QHBoxLayout()

        selector_label = QLabel("Manage:")
        selector_label.setStyleSheet("font-weight: bold; font-size: 11pt; color: white;")
        selector_layout.addWidget(selector_label)

        self.master_type_combo = QComboBox()
        self.master_type_combo.addItems([
            "Services", "Parts", "AC Brands", "Payment Modes"
        ])
        self.master_type_combo.currentTextChanged.connect(self._load_master_data)
        self.master_type_combo.setStyleSheet("""
            QComboBox {
                background-color: #334155;
                color: white;
                border: 1px solid #475569;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 10pt;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox QAbstractItemView {
                background-color: #334155;
                color: white;
                border: 1px solid #475569;
                selection-background-color: #3b82f6;
            }
        """)
        selector_layout.addWidget(self.master_type_combo)

        selector_layout.addStretch()

        add_btn = QPushButton("➕ Add New")
        add_btn.setObjectName("successButton")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 10pt;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
            QPushButton:pressed {
                background-color: #047857;
            }
        """)
        add_btn.clicked.connect(self._add_master_item)
        selector_layout.addWidget(add_btn)

        layout.addLayout(selector_layout)

        # Master data table
        self.master_table = QTableWidget()
        self.master_table.setColumnCount(4)
        self.master_table.setHorizontalHeaderLabels([
            'ID', 'Name', 'Rate/Value', 'Actions'
        ])
        self.master_table.setStyleSheet("""
            QTableWidget {
                background-color: #1e293b;
                color: white;
                border: 1px solid #334155;
                border-radius: 8px;
                gridline-color: #334155;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QTableWidget::item:selected {
                background-color: #3b82f6;
            }
            QHeaderView::section {
                background-color: #334155;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
                font-size: 11pt;
            }
        """)

        header = self.master_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)

        self.master_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.master_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.master_table.setAlternatingRowColors(True)
        self.master_table.verticalHeader().setVisible(False)

        layout.addWidget(self.master_table)

        return QWidgetWrapper(layout)

    def load_user_profile(self):
        """Load user profile data"""
        self.full_name_input.setText(self.user_data.get('full_name', ''))
        self.email_input.setText(self.user_data.get('email', ''))
        self.phone_input.setText(self.user_data.get('phone', ''))
        
        # Load shop details
        self.run_in_thread(
            self._load_shop_details_thread,
            self._update_shop_details
        )
    
    def _load_shop_details_thread(self):
        """Load shop details in background"""
        from controllers.auth_controller import AuthController
        from database.db_connection import DatabaseConnection
        
        db = DatabaseConnection()
        auth = AuthController(db)
        return auth.get_shop_details()
    
    def _update_shop_details(self, shop_details):
        """Update shop details UI"""
        if shop_details:
            self.shop_name_input.setText(shop_details.get('shop_name', ''))
            self.address_input.setText(shop_details.get('address', ''))
            self.shop_phone_input.setText(shop_details.get('phone', ''))
            self.shop_email_input.setText(shop_details.get('email', ''))
            self.gst_input.setText(shop_details.get('gst_number', ''))
            self.owner_name_input.setText(shop_details.get('owner_name', ''))
            self.owner_phone_input.setText(shop_details.get('owner_phone', ''))
        
        # Load master data
        self._load_master_data()
    
    def save_user_profile(self):
        """Save user profile with session refresh and real-time update"""
        full_name = self.full_name_input.text().strip()
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()

        if not full_name:
            self.show_warning_message("Full name is required")
            return

        from controllers.auth_controller import AuthController
        from database.db_connection import DatabaseConnection
        from utils.event_bus import get_event_bus

        db = DatabaseConnection()
        auth = AuthController(db)
        result = auth.update_profile(
            self.user_data.get('id'),
            full_name, email, phone
        )

        # Handle new 3-tuple return value (success, message, updated_user)
        if len(result) == 3:
            success, message, updated_user = result
        else:
            success, message = result
            updated_user = None

        if success:
            # Update local user_data with new values
            self.user_data['full_name'] = full_name
            self.user_data['email'] = email
            self.user_data['phone'] = phone

            # Update from DB response if available
            if updated_user:
                self.user_data.update(updated_user)

            # Refresh the input fields to show updated data
            self.full_name_input.setText(full_name)
            self.email_input.setText(email)
            self.phone_input.setText(phone)

            # CRITICAL: Refresh session manager with updated user data
            from utils.session_manager import get_session
            session = get_session()
            if session:
                session.refresh_session(self.user_data)
                print(f"[SESSION] Session refreshed after profile update")

            # Emit real-time update via event bus
            event_bus = get_event_bus()
            event_bus.emit_user_profile_updated(self.user_data)

            self.show_success_message(message)
            print(f"[DEBUG] Profile saved - emitting signal")
            self.settings_saved.emit()  # Emit signal to notify other views
        else:
            self.show_error_message(message)
    
    def save_shop_details(self):
        """Save shop details with real-time update"""
        shop_name = self.shop_name_input.text().strip()
        address = self.address_input.toPlainText().strip()
        owner_name = self.owner_name_input.text().strip()

        if not shop_name or not address or not owner_name:
            self.show_warning_message("Shop Name, Address, and Owner Name are required")
            return

        shop_data = {
            'shop_name': shop_name,
            'address': address,
            'phone': self.shop_phone_input.text().strip(),
            'email': self.shop_email_input.text().strip(),
            'gst_number': self.gst_input.text().strip(),
            'owner_name': owner_name,
            'owner_phone': self.owner_phone_input.text().strip()
        }

        from controllers.auth_controller import AuthController
        from database.db_connection import DatabaseConnection
        from utils.event_bus import get_event_bus

        db = DatabaseConnection()
        auth = AuthController(db)
        success, message = auth.update_shop_details(shop_data)

        if success:
            # Emit real-time update via event bus
            event_bus = get_event_bus()
            event_bus.emit_shop_details_updated(shop_data)

            self.show_success_message(message)
            print(f"[DEBUG] Shop settings saved - emitting signal")
            # Reload shop details to ensure UI shows updated data
            self.run_in_thread(
                self._load_shop_details_thread,
                self._update_shop_details
            )
            self.settings_saved.emit()  # Emit signal to notify other views
        else:
            self.show_error_message(message)
    
    def create_backup(self):
        """Create database backup"""
        self.show_success_message("Backup created successfully")
    
    def restore_backup(self):
        """Restore from backup"""
        self.show_warning_message("Restore feature - use with caution")
    
    def _load_master_data(self):
        """Load master data based on selected type"""
        master_type = self.master_type_combo.currentText()

        self.run_in_thread(
            self._load_master_data_thread,
            self._update_master_table,
            None,  # on_error - use default handler
            master_type
        )
    
    def _load_master_data_thread(self, master_type):
        """Load master data in background"""
        from database.db_connection import DatabaseContext

        with DatabaseContext() as db:
            if master_type == "Services":
                return db.execute_query(
                    "SELECT id, service_name as name, default_rate as rate FROM services WHERE is_active = TRUE",
                    fetch_all=True
                )
            elif master_type == "Parts":
                return db.execute_query(
                    "SELECT id, part_name as name, default_rate as rate FROM parts WHERE is_active = TRUE",
                    fetch_all=True
                )
            elif master_type == "AC Brands":
                return db.execute_query(
                    "SELECT id, brand_name as name, '' as rate FROM ac_brands WHERE is_active = TRUE",
                    fetch_all=True
                )
            elif master_type == "Payment Modes":
                return [
                    {'id': 1, 'name': 'Cash', 'rate': ''},
                    {'id': 2, 'name': 'Card', 'rate': ''},
                    {'id': 3, 'name': 'UPI', 'rate': ''},
                    {'id': 4, 'name': 'Bank Transfer', 'rate': ''},
                ]
        return []
    
    def _update_master_table(self, data):
        """Update master data table"""
        self.master_table.setRowCount(0)
        
        for item in (data or []):
            row = self.master_table.rowCount()
            self.master_table.insertRow(row)
            
            self.master_table.setItem(row, 0, QTableWidgetItem(str(item['id'])))
            self.master_table.setItem(row, 1, QTableWidgetItem(item['name']))
            self.master_table.setItem(row, 2, QTableWidgetItem(str(item.get('rate', ''))))
            
            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(5, 0, 5, 0)
            
            edit_btn = QPushButton("✏️")
            edit_btn.setObjectName("iconButton")
            edit_btn.clicked.connect(lambda checked, r=row: self._edit_master_item(r))
            actions_layout.addWidget(edit_btn)
            
            delete_btn = QPushButton("🗑️")
            delete_btn.setObjectName("iconButton")
            delete_btn.clicked.connect(lambda checked, r=row: self._delete_master_item(r))
            actions_layout.addWidget(delete_btn)
            
            self.master_table.setCellWidget(row, 3, actions_widget)
    
    def _add_master_item(self):
        """Add new master item with real-time update"""
        master_type = self.master_type_combo.currentText()
        dialog = AddMasterItemDialog(master_type, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._load_master_data()
            self.show_success_message(f"{master_type[:-1]} added successfully")
            # Emit real-time update
            from utils.event_bus import get_event_bus
            event_bus = get_event_bus()
            event_bus.emit_master_data_updated(master_type)

    def _edit_master_item(self, row):
        """Edit master item with real-time update"""
        master_type = self.master_type_combo.currentText()
        item_id = int(self.master_table.item(row, 0).text())
        dialog = EditMasterItemDialog(master_type, item_id, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._load_master_data()
            self.show_success_message(f"{master_type[:-1]} updated successfully")
            # Emit real-time update
            from utils.event_bus import get_event_bus
            event_bus = get_event_bus()
            event_bus.emit_master_data_updated(master_type)

    def _delete_master_item(self, row):
        """Delete master item with real-time update"""
        if self.show_question("Are you sure you want to delete this item?"):
            master_type = self.master_type_combo.currentText()
            item_id = int(self.master_table.item(row, 0).text())

            from database.db_connection import DatabaseContext

            with DatabaseContext() as db:
                if master_type == "Services":
                    db.execute_query("UPDATE services SET is_active = FALSE WHERE id = %s", (item_id,))
                elif master_type == "Parts":
                    db.execute_query("UPDATE parts SET is_active = FALSE WHERE id = %s", (item_id,))
                elif master_type == "AC Brands":
                    db.execute_query("UPDATE ac_brands SET is_active = FALSE WHERE id = %s", (item_id,))

            self._load_master_data()
            self.show_success_message("Item deleted successfully")
            # Emit real-time update
            from utils.event_bus import get_event_bus
            event_bus = get_event_bus()
            event_bus.emit_master_data_updated(master_type)
    
    def refresh_data(self):
        """Refresh settings data"""
        self.load_user_profile()


class ProfileSettingsView(SettingsView):
    """Profile settings view (alias for compatibility)"""
    pass


class ChangePasswordDialog(QDialog):
    """Dialog for changing password"""
    
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.setWindowTitle("Change Password")
        self.setMinimumWidth(400)
        self.setStyleSheet(parent.theme_manager.get_main_stylesheet() if parent else "")
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup dialog UI"""
        layout = QVBoxLayout(self)

        form = QFormLayout()
        form.setSpacing(15)

        self.current_password_input = QLineEdit()
        self.current_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.current_password_input.setPlaceholderText("Enter current password")
        form.addRow("Current Password:", self.current_password_input)

        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_password_input.setPlaceholderText("Enter new password")
        form.addRow("New Password:", self.new_password_input)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_input.setPlaceholderText("Re-enter new password")
        form.addRow("Confirm Password:", self.confirm_password_input)

        layout.addLayout(form)

        # Password requirements label
        requirements_label = QLabel(
            "💡 Password must be at least 8 characters and contain:\n"
            "   • At least one uppercase letter (A-Z)\n"
            "   • At least one lowercase letter (a-z)\n"
            "   • At least one number (0-9)\n"
            "   • At least one special character (!@#$%^&*...)"
        )
        requirements_label.setStyleSheet("""
            color: #94a3b8;
            font-size: 9pt;
            background-color: rgba(59, 130, 246, 0.1);
            border-left: 3px solid #3b82f6;
            padding: 10px;
            border-radius: 4px;
        """)
        requirements_label.setWordWrap(True)
        layout.addWidget(requirements_label)

        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._validate_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def _validate_and_accept(self):
        """Validate and change password with strong password rules"""
        current = self.current_password_input.text()
        new = self.new_password_input.text()
        confirm = self.confirm_password_input.text()

        if not current or not new or not confirm:
            QMessageBox.warning(self, "Validation", "All fields are required")
            return

        if new != confirm:
            QMessageBox.warning(self, "Validation", "New passwords do not match")
            return

        # Validate password strength using AuthController
        from controllers.auth_controller import AuthController
        from database.db_connection import DatabaseConnection

        is_valid, message = AuthController.validate_password_strength(None, new)
        if not is_valid:
            QMessageBox.warning(self, "Weak Password", message)
            return

        # Change password
        db = DatabaseConnection()
        auth = AuthController(db)
        success, msg = auth.change_password(self.user_id, current, new)

        if success:
            self.accept()
            QMessageBox.information(self, "Success", msg)
        else:
            QMessageBox.warning(self, "Error", msg)


class AddMasterItemDialog(QDialog):
    """Dialog for adding master item"""
    
    def __init__(self, master_type, parent=None):
        super().__init__(parent)
        self.master_type = master_type
        self.setWindowTitle(f"Add {master_type[:-1]}")
        self.setMinimumWidth(400)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup dialog UI"""
        layout = QVBoxLayout(self)
        
        form = QFormLayout()
        form.setSpacing(15)
        
        self.name_input = QLineEdit()
        form.addRow("Name *:", self.name_input)
        
        if self.master_type in ["Services", "Parts"]:
            self.rate_input = QDoubleSpinBox()
            self.rate_input.setRange(0, 999999)
            self.rate_input.setPrefix("₹ ")
            form.addRow("Rate:", self.rate_input)
        
        layout.addLayout(form)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._validate_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def _validate_and_accept(self):
        """Validate and save item"""
        name = self.name_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Validation", "Name is required")
            return

        from database.db_connection import DatabaseContext

        with DatabaseContext() as db:
            if self.master_type == "Services":
                rate = self.rate_input.value() if hasattr(self, 'rate_input') else 0
                db.execute_query(
                    "INSERT INTO services (service_name, default_rate, is_active) VALUES (%s, %s, TRUE)",
                    (name, rate)
                )
            elif self.master_type == "Parts":
                rate = self.rate_input.value() if hasattr(self, 'rate_input') else 0
                db.execute_query(
                    "INSERT INTO parts (part_name, default_rate, is_active) VALUES (%s, %s, TRUE)",
                    (name, rate)
                )
            elif self.master_type == "AC Brands":
                db.execute_query(
                    "INSERT INTO ac_brands (brand_name, is_active) VALUES (%s, TRUE)",
                    (name,)
                )

        self.accept()


class EditMasterItemDialog(QDialog):
    """Dialog for editing master item"""

    def __init__(self, master_type, item_id, parent=None):
        super().__init__(parent)
        self.master_type = master_type
        self.item_id = item_id
        self.setWindowTitle(f"Edit {master_type[:-1]}")
        self.setMinimumWidth(400)

        self._setup_ui()
        self._load_item()

    def _setup_ui(self):
        """Setup dialog UI"""
        layout = QVBoxLayout(self)

        form = QFormLayout()
        form.setSpacing(15)

        self.name_input = QLineEdit()
        form.addRow("Name *:", self.name_input)

        if self.master_type in ["Services", "Parts"]:
            self.rate_input = QDoubleSpinBox()
            self.rate_input.setRange(0, 999999)
            self.rate_input.setPrefix("₹ ")
            form.addRow("Rate:", self.rate_input)

        layout.addLayout(form)

        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._validate_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _load_item(self):
        """Load item data"""
        from database.db_connection import DatabaseContext

        with DatabaseContext() as db:
            if self.master_type == "Services":
                item = db.execute_query(
                    "SELECT service_name, default_rate FROM services WHERE id = %s",
                    (self.item_id,),
                    fetch_one=True
                )
            elif self.master_type == "Parts":
                item = db.execute_query(
                    "SELECT part_name, default_rate FROM parts WHERE id = %s",
                    (self.item_id,),
                    fetch_one=True
                )
            elif self.master_type == "AC Brands":
                item = db.execute_query(
                    "SELECT brand_name FROM ac_brands WHERE id = %s",
                    (self.item_id,),
                    fetch_one=True
                )
            else:
                item = None

            if item:
                self.name_input.setText(item.get('service_name') or item.get('part_name') or item.get('brand_name', ''))
                if hasattr(self, 'rate_input') and item.get('default_rate'):
                    self.rate_input.setValue(item.get('default_rate', 0))

    def _validate_and_accept(self):
        """Validate and save item"""
        name = self.name_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Validation", "Name is required")
            return

        from database.db_connection import DatabaseContext

        with DatabaseContext() as db:
            if self.master_type == "Services":
                rate = self.rate_input.value() if hasattr(self, 'rate_input') else 0
                db.execute_query(
                    "UPDATE services SET service_name = %s, default_rate = %s WHERE id = %s",
                    (name, rate, self.item_id)
                )
            elif self.master_type == "Parts":
                rate = self.rate_input.value() if hasattr(self, 'rate_input') else 0
                db.execute_query(
                    "UPDATE parts SET part_name = %s, default_rate = %s WHERE id = %s",
                    (name, rate, self.item_id)
                )
            elif self.master_type == "AC Brands":
                db.execute_query(
                    "UPDATE ac_brands SET brand_name = %s WHERE id = %s",
                    (name, self.item_id)
                )
        
        self.accept()


class QWidgetWrapper(QWidget):
    """Wrapper for layout-only widgets"""
    def __init__(self, layout):
        super().__init__()
        self.setLayout(layout)
