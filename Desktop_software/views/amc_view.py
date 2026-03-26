"""
AMC View - PySide6 Annual Maintenance Contract Management
Professional AMC contract creation and management
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea,
    QSizePolicy, QTabWidget, QComboBox, QDoubleSpinBox, QSpinBox,
    QTextEdit, QFormLayout, QMessageBox, QDateEdit, QDialog,
    QDialogButtonBox, QSplitter
)
from PySide6.QtCore import Qt, QDate
from datetime import datetime, timedelta

from utils.unified_theme import UnifiedTheme
from views.base_window import BaseView


class AMCView(BaseView):
    """AMC contract management view"""
    
    def __init__(self):
        super().__init__()
        self.selected_customer = None
        self.amc_units = []
        self.selected_amc_id = None
        self.customer_list = []
        self.technicians_list = []
        
        self._setup_ui()
        self.load_amc_data()
        self.load_technicians()
    
    def _setup_ui(self):
        """Setup AMC UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Tab widget
        self.tabs = QTabWidget()
        
        # Tab 1: New AMC Contract
        self.new_contract_tab = self._create_new_contract_tab()
        self.tabs.addTab(self.new_contract_tab, "➕ New AMC Contract")
        
        # Tab 2: AMC List
        self.amc_list_tab = self._create_amc_list_tab()
        self.tabs.addTab(self.amc_list_tab, "📋 AMC Contracts")
        
        # Tab 3: Visit Schedule
        self.visits_tab = self._create_visits_tab()
        self.tabs.addTab(self.visits_tab, "📅 Visit Schedule")
        
        main_layout.addWidget(self.tabs)
    
    def _create_new_contract_tab(self):
        """Create new AMC contract form - WHITE THEME"""
        # Use fixed white theme colors
        colors = {
            'bg': '#FFFFFF',
            'fg': '#1e293b',
            'card_bg': '#FFFFFF',
            'border': '#e2e8f0',
            'primary': '#0891b2',
            'secondary': '#64748b',
            'hover': '#f1f5f9',
            'success': '#10b981',
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'muted': '#94a3b8'
        }

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background-color: transparent;")

        content = QWidget()
        content.setStyleSheet(f"""
            QWidget {{
                background-color: {colors['bg']};
                color: {colors['fg']};
            }}
            QLineEdit, QComboBox, QTextEdit, QSpinBox, QDoubleSpinBox, QDateEdit {{
                background-color: {colors['card_bg']};
                color: {colors['fg']};
                border: 1px solid {colors['border']};
                padding: 8px;
                border-radius: 4px;
            }}
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus, QDateEdit:focus {{
                border: 2px solid {colors['primary']};
            }}
            QLabel {{
                color: {colors['fg']};
                font-weight: 600;
            }}
        """)
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # Contract Info
        info_group = self._create_group_box("📄 Contract Information")
        info_layout = QFormLayout()

        self.amc_id_label = QLabel("Auto-generated")
        self.amc_id_label.setStyleSheet(f"font-weight: bold; color: {colors['fg']}; font-size: 11pt;")
        info_layout.addRow("AMC ID:", self.amc_id_label)
        self._generate_amc_id()

        status_label = QLabel("● Active")
        status_label.setStyleSheet(f"color: {colors['success']}; font-weight: bold; font-size: 11pt;")
        info_layout.addRow("Status:", status_label)

        info_group.layout().addLayout(info_layout)
        layout.addWidget(info_group)

        # Customer Selection
        customer_group = self._create_group_box("👤 Customer Details")
        customer_layout = QFormLayout()

        # Search
        search_layout = QHBoxLayout()
        self.customer_search_input = QLineEdit()
        self.customer_search_input.setPlaceholderText("Search by name or mobile...")
        self.customer_search_input.setStyleSheet(f"color: {colors['fg']}; padding: 6px;")
        self.customer_search_input.textChanged.connect(self._search_customer)
        search_layout.addWidget(self.customer_search_input)

        search_btn = QPushButton("🔍 Search")
        search_btn.setObjectName("primaryButton")
        search_btn.setStyleSheet("padding: 6px 12px;")
        search_btn.clicked.connect(self._search_customer)
        search_layout.addWidget(search_btn)

        customer_layout.addRow("Search:", search_layout)

        # Customer combo
        self.customer_combo = QComboBox()
        self.customer_combo.addItem("Select Customer", "")
        self.customer_combo.setMinimumWidth(300)
        self.customer_combo.setStyleSheet(f"color: {colors['fg']}; padding: 6px;")
        self.customer_combo.currentTextChanged.connect(self._on_customer_select)
        customer_layout.addRow("Select Customer:", self.customer_combo)

        # Customer details
        self.customer_details_label = QLabel("")
        self.customer_details_label.setWordWrap(True)
        self.customer_details_label.setStyleSheet(f"color: {colors['fg']}; font-size: 10pt;")
        customer_layout.addRow("", self.customer_details_label)

        customer_group.layout().addLayout(customer_layout)
        layout.addWidget(customer_group)

        # Contract Details
        contract_group = self._create_group_box("📋 Contract Details")
        contract_layout = QFormLayout()

        self.contract_type_combo = QComboBox()
        self.contract_type_combo.addItems(["Comprehensive", "Non-Comprehensive"])
        self.contract_type_combo.setStyleSheet(f"color: {colors['fg']}; padding: 6px;")
        contract_layout.addRow("Contract Type:", self.contract_type_combo)

        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(1, 5)
        self.duration_spin.setValue(1)
        self.duration_spin.setSuffix(" year(s)")
        self.duration_spin.setStyleSheet(f"color: {colors['fg']}; padding: 6px;")
        contract_layout.addRow("Duration:", self.duration_spin)

        self.start_date_input = QDateEdit()
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setDate(QDate.currentDate())
        self.start_date_input.setDisplayFormat("dd-MM-yyyy")
        self.start_date_input.setStyleSheet(f"color: {colors['fg']}; padding: 6px;")
        contract_layout.addRow("Start Date:", self.start_date_input)

        self.end_date_input = QDateEdit()
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setDate(QDate.currentDate().addYears(1))
        self.end_date_input.setDisplayFormat("dd-MM-yyyy")
        self.end_date_input.setStyleSheet(f"color: {colors['fg']}; padding: 6px;")
        contract_layout.addRow("End Date:", self.end_date_input)

        self.contract_value_input = QDoubleSpinBox()
        self.contract_value_input.setRange(0, 999999)
        self.contract_value_input.setPrefix("₹ ")
        self.contract_value_input.setStyleSheet(f"color: {colors['fg']}; padding: 6px;")
        contract_layout.addRow("Contract Value:", self.contract_value_input)

        contract_group.layout().addLayout(contract_layout)
        layout.addWidget(contract_group)
        
        # Units
        units_group = self._create_group_box("❄️ AC Units")
        units_layout = QVBoxLayout()

        unit_select_layout = QHBoxLayout()

        self.unit_type_combo = QComboBox()
        self.unit_type_combo.addItems(["Split", "Window", "Cassette", "Tower"])
        self.unit_type_combo.setStyleSheet(f"color: {colors['fg']}; padding: 6px;")
        unit_select_layout.addWidget(self.unit_type_combo)

        self.unit_ton_combo = QComboBox()
        self.unit_ton_combo.addItems(["1.0", "1.5", "2.0", "3.0"])
        self.unit_ton_combo.setStyleSheet(f"color: {colors['fg']}; padding: 6px;")
        unit_select_layout.addWidget(self.unit_ton_combo)
        
        add_unit_btn = QPushButton("➕ Add Unit")
        add_unit_btn.setObjectName("primaryButton")
        add_unit_btn.clicked.connect(self._add_unit)
        unit_select_layout.addWidget(add_unit_btn)
        
        unit_select_layout.addStretch()
        units_layout.addLayout(unit_select_layout)
        
        self.units_table = QTableWidget()
        self.units_table.setColumnCount(3)
        self.units_table.setHorizontalHeaderLabels(['Type', 'Capacity', 'Actions'])
        
        header = self.units_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        
        self.units_table.setAlternatingRowColors(True)
        self.units_table.verticalHeader().setVisible(False)
        self.units_table.setMaximumHeight(150)
        units_layout.addWidget(self.units_table)
        
        units_group.layout().addLayout(units_layout)
        layout.addWidget(units_group)
        
        # Services Included
        services_group = self._create_group_box("🔧 Services Included")
        services_layout = QVBoxLayout()
        
        self.services_text = QTextEdit()
        self.services_text.setPlaceholderText("Enter services included in AMC (one per line)")
        self.services_text.setMaximumHeight(150)
        services_layout.addWidget(self.services_text)
        
        services_group.layout().addLayout(services_layout)
        layout.addWidget(services_group)
        
        # Action buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        save_btn = QPushButton("💾 Save AMC Contract")
        save_btn.setObjectName("successButton")
        save_btn.clicked.connect(self._save_amc)
        btn_layout.addWidget(save_btn)
        
        layout.addLayout(btn_layout)
        layout.addStretch()
        
        scroll.setWidget(content)
        return scroll
    
    def _create_amc_list_tab(self):
        """Create AMC list tab - WHITE THEME"""
        # Use fixed white theme colors
        colors = {
            'bg': '#FFFFFF',
            'fg': '#1e293b',
            'card_bg': '#FFFFFF',
            'border': '#e2e8f0',
            'primary': '#0891b2',
            'secondary': '#64748b',
            'hover': '#f1f5f9',
            'success': '#10b981',
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'muted': '#94a3b8'
        }

        layout = QVBoxLayout()

        # Controls
        control_layout = QHBoxLayout()

        search_label = QLabel("🔍 SEARCH:")
        search_label.setStyleSheet(f"font-weight: bold; color: {colors['fg']}; font-size: 11pt;")
        control_layout.addWidget(search_label)

        self.amc_search_input = QLineEdit()
        self.amc_search_input.setPlaceholderText("Search AMC...")
        self.amc_search_input.setStyleSheet(f"color: {colors['fg']}; padding: 6px;")
        self.amc_search_input.textChanged.connect(self.load_amc_data)
        control_layout.addWidget(self.amc_search_input)

        control_layout.addStretch()

        layout.addLayout(control_layout)
        
        # AMC table
        self.amc_table = QTableWidget()
        self.amc_table.setColumnCount(8)
        self.amc_table.setHorizontalHeaderLabels([
            'AMC ID', 'Customer', 'Type', 'Start Date', 'End Date',
            'Value (₹)', 'Status', 'Actions'
        ])
        self.amc_table.setShowGrid(True)
        self.amc_table.setAlternatingRowColors(True)
        self.amc_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.amc_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.amc_table.verticalHeader().setVisible(False)
        self.amc_table.verticalHeader().setDefaultSectionSize(35)
        
        # Style AMC table - THEME SUPPORT
        colors = self.theme_manager.get_colors()
        
        self.amc_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {colors['bg']};
                border: 1px solid {colors['border']};
                border-radius: 6px;
                gridline-color: {colors['border']};
            }}
            QTableWidget::item {{
                padding: 8px;
                border: 1px solid {colors['border']};
                color: {colors['fg']};
            }}
            QTableWidget::item:hover {{
                background-color: {colors['hover']};
            }}
            QHeaderView::section {{
                background-color: {colors['card_bg']};
                border: 1px solid {colors['border']};
                padding: 10px 8px;
                font-weight: bold;
                text-transform: uppercase;
                color: {colors['fg']};
            }}
        """)

        header = self.amc_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)

        self.amc_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.amc_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.amc_table.cellDoubleClicked.connect(self._on_amc_double_click)

        layout.addWidget(self.amc_table)
        
        return QWidgetWrapper(layout)
    
    def _create_visits_tab(self):
        """Create visit schedule tab - WHITE THEME"""
        # Use fixed white theme colors
        colors = {
            'bg': '#FFFFFF',
            'fg': '#1e293b',
            'card_bg': '#FFFFFF',
            'border': '#e2e8f0',
            'primary': '#0891b2',
            'secondary': '#64748b',
            'hover': '#f1f5f9',
            'success': '#10b981',
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'muted': '#94a3b8'
        }

        layout = QVBoxLayout()

        # Controls
        control_layout = QHBoxLayout()

        filter_label = QLabel("📅 FILTER:")
        filter_label.setStyleSheet(f"font-weight: bold; color: {colors['fg']}; font-size: 11pt;")
        control_layout.addWidget(filter_label)

        self.visit_status_combo = QComboBox()
        self.visit_status_combo.addItems(["All", "Scheduled", "Completed", "Cancelled"])
        self.visit_status_combo.setStyleSheet(f"color: {colors['fg']}; padding: 6px;")
        self.visit_status_combo.currentTextChanged.connect(self._load_visits)
        control_layout.addWidget(self.visit_status_combo)

        control_layout.addStretch()

        add_visit_btn = QPushButton("➕ Schedule Visit")
        add_visit_btn.setObjectName("primaryButton")
        add_visit_btn.setStyleSheet("padding: 8px 16px;")
        add_visit_btn.clicked.connect(self._schedule_visit)
        control_layout.addWidget(add_visit_btn)

        layout.addLayout(control_layout)
        
        # Visits table
        self.visits_table = QTableWidget()
        self.visits_table.setColumnCount(6)
        self.visits_table.setHorizontalHeaderLabels([
            'Visit ID', 'AMC ID', 'Customer', 'Visit Date', 'Technician', 'Status'
        ])
        self.visits_table.setShowGrid(True)
        self.visits_table.setAlternatingRowColors(True)
        self.visits_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.visits_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.visits_table.verticalHeader().setVisible(False)
        self.visits_table.verticalHeader().setDefaultSectionSize(35)
        
        # Style visits table - THEME SUPPORT
        colors = self.theme_manager.get_colors()
        
        self.visits_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {colors['bg']};
                border: 1px solid {colors['border']};
                border-radius: 6px;
                gridline-color: {colors['border']};
            }}
            QTableWidget::item {{
                padding: 8px;
                border: 1px solid {colors['border']};
                color: {colors['fg']};
            }}
            QTableWidget::item:hover {{
                background-color: {colors['hover']};
            }}
            QHeaderView::section {{
                background-color: {colors['card_bg']};
                border: 1px solid {colors['border']};
                padding: 10px 8px;
                font-weight: bold;
                text-transform: uppercase;
                color: {colors['fg']};
            }}
        """)

        header = self.visits_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)

        self.visits_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.visits_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.visits_table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.visits_table)

        return QWidgetWrapper(layout)

    def _generate_amc_id(self):
        """Generate AMC ID"""
        amc_id = f"AMC-{datetime.now().strftime('%Y%m')}-001"
        self.amc_id_label.setText(amc_id)
    
    def _search_customer(self):
        """Search for customers"""
        self.run_in_thread(
            self._search_customer_thread,
            self._update_customer_combo
        )
    
    def _search_customer_thread(self):
        """Search customers in background"""
        from database.db_connection import DatabaseContext
        
        search_term = self.customer_search_input.text().strip()
        
        with DatabaseContext() as db:
            query = """
            SELECT id, name, mobile, email, address
            FROM customers
            WHERE is_active = TRUE
            """
            params = []
            
            if search_term:
                query += " AND (name LIKE %s OR mobile LIKE %s)"
                params.extend([f"%{search_term}%", f"%{search_term}%"])
            
            query += " ORDER BY name"
            
            return db.execute_query(query, params, fetch_all=True)
    
    def _update_customer_combo(self, customers):
        """Update customer combo box"""
        self.customer_list = customers or []
        self.customer_combo.clear()
        self.customer_combo.addItem("Select Customer", "")
        
        for customer in self.customer_list:
            self.customer_combo.addItem(
                f"{customer['name']} - {customer['mobile']}",
                customer['id']
            )
    
    def _on_customer_select(self):
        """Handle customer selection"""
        customer_id = self.customer_combo.currentData()
        if not customer_id:
            self.customer_details_label.setText("")
            return
        
        customer = next((c for c in self.customer_list if c['id'] == customer_id), None)
        if customer:
            details = f"📱 {customer['mobile']}"
            if customer.get('email'):
                details += f" | ✉️ {customer['email']}"
            if customer.get('address'):
                details += f"\n📍 {customer['address']}"
            self.customer_details_label.setText(details)
    
    def _add_unit(self):
        """Add AC unit to AMC"""
        unit_type = self.unit_type_combo.currentText()
        unit_ton = self.unit_ton_combo.currentText()
        
        row = self.units_table.rowCount()
        self.units_table.insertRow(row)
        self.units_table.setItem(row, 0, QTableWidgetItem(unit_type))
        self.units_table.setItem(row, 1, QTableWidgetItem(f"{unit_ton} Ton"))
        
        # Delete button
        delete_btn = QPushButton("🗑️")
        delete_btn.setObjectName("iconButton")
        delete_btn.clicked.connect(lambda: self._remove_unit(row))
        self.units_table.setCellWidget(row, 2, delete_btn)
        
        self.amc_units.append({'type': unit_type, 'ton': unit_ton})
    
    def _remove_unit(self, row):
        """Remove AC unit"""
        self.units_table.removeRow(row)
        if 0 <= row < len(self.amc_units):
            self.amc_units.pop(row)
    
    def _save_amc(self):
        """Save AMC contract"""
        # Validate
        if not self.customer_combo.currentData():
            self.show_warning_message("Please select a customer")
            return
        
        if not self.amc_units:
            self.show_warning_message("Please add at least one AC unit")
            return
        
        self.show_success_message("AMC contract saved successfully")
    
    def load_amc_data(self):
        """Load AMC contracts"""
        self.run_in_thread(
            self._load_amc_data_thread,
            self._update_amc_table
        )
    
    def _load_amc_data_thread(self):
        """Load AMC data in background"""
        from database.db_connection import DatabaseContext

        search_term = self.amc_search_input.text().strip()

        with DatabaseContext() as db:
            query = """
            SELECT
                ac.id, ac.amc_id, ac.contract_type, ac.start_date, ac.end_date,
                ac.contract_amount, ac.amc_status,
                c.name as customer_name
            FROM amc_contracts ac
            JOIN customers c ON ac.customer_id = c.id
            WHERE ac.is_active = TRUE
            """

            params = []
            if search_term:
                query += " AND (ac.amc_id LIKE %s OR c.name LIKE %s)"
                params.extend([f"%{search_term}%", f"%{search_term}%"])

            query += " ORDER BY ac.created_at DESC"

            return db.execute_query(query, params, fetch_all=True)

    def _update_amc_table(self, amc_list):
        """Update AMC table"""
        self.amc_table.setRowCount(0)

        for amc in (amc_list or []):
            row = self.amc_table.rowCount()
            self.amc_table.insertRow(row)

            status_color = "#10b981" if amc['amc_status'] == 'Active' else "#64748b"

            id_item = QTableWidgetItem(amc['amc_id'])
            id_item.setData(Qt.ItemDataRole.UserRole, amc['id'])
            self.amc_table.setItem(row, 0, id_item)
            self.amc_table.setItem(row, 1, QTableWidgetItem(amc['customer_name']))
            self.amc_table.setItem(row, 2, QTableWidgetItem(amc['contract_type']))
            self.amc_table.setItem(row, 3, QTableWidgetItem(amc['start_date'].strftime('%d-%m-%Y')))
            self.amc_table.setItem(row, 4, QTableWidgetItem(amc['end_date'].strftime('%d-%m-%Y')))
            self.amc_table.setItem(row, 5, QTableWidgetItem(f"₹{amc['contract_amount']:,.2f}"))

            status_item = QTableWidgetItem(amc['amc_status'])
            status_item.setForeground(Qt.GlobalColor.darkGreen if amc['amc_status'] == 'Active' else Qt.GlobalColor.darkGray)
            self.amc_table.setItem(row, 6, status_item)

            self.amc_table.setItem(row, 7, QTableWidgetItem("👁️ ✏️"))
    
    def _on_amc_double_click(self, row, col):
        """Handle AMC double-click - View/Edit AMC details"""
        selected_rows = self.amc_table.selectedItems()
        if not selected_rows:
            self.show_warning_message("Please select an AMC to view")
            return
        
        # Get AMC database ID from UserRole data
        row = selected_rows[0].row()
        id_item = self.amc_table.item(row, 0)
        
        if not id_item:
            self.show_warning_message("No AMC ID found")
            return
        
        # Get the database ID stored in UserRole
        amc_database_id = id_item.data(Qt.ItemDataRole.UserRole)
        
        if amc_database_id:
            self._show_amc_details(int(amc_database_id))
        else:
            self.show_warning_message("Invalid AMC ID")
    
    def _show_amc_details(self, amc_id):
        """Show AMC details dialog"""
        try:
            from database.db_connection import DatabaseContext
            
            with DatabaseContext() as db:
                # Get AMC contract details
                query = """
                SELECT
                    ac.*,
                    c.name as customer_name,
                    c.mobile as customer_mobile,
                    c.address as customer_address
                FROM amc_contracts ac
                JOIN customers c ON ac.customer_id = c.id
                WHERE ac.id = %s
                """
                
                amc = db.execute_query(query, (amc_id,), fetch_one=True)
                
                if not amc:
                    self.show_error_message("AMC not found")
                    return
                
                # Show AMC details
                details_text = f"""
╔══════════════════════════════════════════════════════════╗
║              AMC CONTRACT DETAILS                        ║
╠══════════════════════════════════════════════════════════╣
║ AMC ID: {amc['amc_id']:<48} ║
║ Customer: {amc['customer_name']:<46} ║
║ Mobile: {amc['customer_mobile']:<48} ║
║ Address: {amc['customer_address']:<47} ║
╠══════════════════════════════════════════════════════════╣
║ Contract Type: {amc['contract_type']:<41} ║
║ Start Date: {amc['start_date'].strftime('%d-%m-%Y') if amc['start_date'] else 'N/A':<44} ║
║ End Date: {amc['end_date'].strftime('%d-%m-%Y') if amc['end_date'] else 'N/A':<46} ║
║ No. of Units: {amc['no_of_units']:<42} ║
║ Services/Year: {amc['services_per_year']:<41} ║
╠══════════════════════════════════════════════════════════╣
║ Contract Amount: Rs. {amc['contract_amount']:,.2f}{'':>32} ║
║ GST ({amc['gst_percent']}%): Rs. {amc['contract_amount'] * amc['gst_percent'] / 100:,.2f}{'':>26} ║
║ Total Amount: Rs. {amc['total_amount']:,.2f}{'':>36} ║
║ Paid: Rs. {amc['advance_paid']:,.2f}{'':>42} ║
║ Balance: Rs. {amc['balance_amount']:,.2f}{'':>41} ║
║ Payment Status: {amc['payment_status']:<40} ║
╠══════════════════════════════════════════════════════════╣
║ AMC Status: {amc['amc_status']:<44} ║
║ Notes: {amc['notes'] or 'N/A':<49} ║
╚══════════════════════════════════════════════════════════╝
                """
                
                # Show in message box
                from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit
                from PySide6.QtCore import Qt
                
                dialog = QDialog(self)
                dialog.setWindowTitle(f"AMC Details - {amc['amc_id']}")
                dialog.setMinimumSize(700, 600)
                
                layout = QVBoxLayout(dialog)
                
                # AMC details text
                details_edit = QTextEdit()
                details_edit.setReadOnly(True)
                details_edit.setFontFamily('Courier New')
                details_edit.setPlainText(details_text)
                layout.addWidget(details_edit)
                
                # Close button
                close_btn = QPushButton("Close")
                close_btn.setObjectName("primaryButton")
                close_btn.clicked.connect(dialog.close)
                layout.addWidget(close_btn)
                
                dialog.exec()
                
        except Exception as e:
            self.show_error_message(f"Error loading AMC details: {str(e)}")
    
    def load_technicians(self):
        """Load technicians list"""
        self.run_in_thread(
            self._load_technicians_thread,
            self._update_technician_data
        )
    
    def _load_technicians_thread(self):
        """Load technicians in background"""
        from database.db_connection import DatabaseContext
        
        with DatabaseContext() as db:
            return db.execute_query(
                "SELECT id, name FROM technicians WHERE is_active = TRUE",
                fetch_all=True
            )
    
    def _update_technician_data(self, technicians):
        """Update technician data"""
        self.technicians_list = technicians or []
    
    def _load_visits(self):
        """Load visit schedule"""
        self.run_in_thread(
            self._load_visits_thread,
            self._update_visits_table
        )
    
    def _load_visits_thread(self):
        """Load visits in background"""
        from database.db_connection import DatabaseContext
        
        status = self.visit_status_combo.currentText()
        
        with DatabaseContext() as db:
            query = """
            SELECT
                v.id, v.amc_id, v.visit_date, v.visit_status,
                ac.amc_id as amc_number,
                c.name as customer_name,
                t.name as technician_name
            FROM amc_visits v
            JOIN amc_contracts ac ON v.amc_id = ac.id
            JOIN customers c ON ac.customer_id = c.id
            LEFT JOIN technicians t ON v.technician_id = t.id
            WHERE v.is_active = TRUE
            """
            
            params = []
            if status != "All":
                query += " AND v.visit_status = %s"
                params.append(status)
            
            query += " ORDER BY v.visit_date"
            
            return db.execute_query(query, params, fetch_all=True)
    
    def _update_visits_table(self, visits):
        """Update visits table"""
        self.visits_table.setRowCount(0)
        
        for visit in (visits or []):
            row = self.visits_table.rowCount()
            self.visits_table.insertRow(row)
            
            self.visits_table.setItem(row, 0, QTableWidgetItem(str(visit['id'])))
            self.visits_table.setItem(row, 1, QTableWidgetItem(visit['amc_number']))
            self.visits_table.setItem(row, 2, QTableWidgetItem(visit['customer_name']))
            self.visits_table.setItem(row, 3, QTableWidgetItem(visit['visit_date'].strftime('%d-%m-%Y')))
            self.visits_table.setItem(row, 4, QTableWidgetItem(visit['technician_name'] or 'Not Assigned'))
            self.visits_table.setItem(row, 5, QTableWidgetItem(visit['visit_status']))
    
    def _schedule_visit(self):
        """Schedule new visit"""
        self.show_success_message("Schedule visit - coming soon")
    
    def refresh_data(self):
        """Refresh AMC data"""
        self.load_amc_data()
        self._load_visits()
    
    def update_theme_colors(self):
        """Update widget colors when theme changes"""
        colors = self.theme_manager.get_colors()

        # Apply QPalette colors
        self.theme_manager.apply_palette(self)
        
        # Apply theme directly to all tables for proper alternating colors
        if hasattr(self, 'amc_table'):
            self.theme_manager.apply_table_theme(self.amc_table)
        
        if hasattr(self, 'units_table'):
            self.theme_manager.apply_table_theme(self.units_table)
        
        if hasattr(self, 'visits_table'):
            self.theme_manager.apply_table_theme(self.visits_table)

        # Update labels and inputs
        if hasattr(self, 'amc_id_label'):
            self.amc_id_label.setStyleSheet(f"font-weight: bold; color: {colors['fg']}; font-size: 11pt;")

        if hasattr(self, 'customer_search_input'):
            self.customer_search_input.setStyleSheet(f"color: {colors['fg']}; padding: 6px;")

        if hasattr(self, 'customer_combo'):
            self.customer_combo.setStyleSheet(f"color: {colors['fg']}; padding: 6px;")

        if hasattr(self, 'customer_details_label'):
            self.customer_details_label.setStyleSheet(f"color: {colors['fg']}; font-size: 10pt;")

        if hasattr(self, 'contract_type_combo'):
            self.contract_type_combo.setStyleSheet(f"color: {colors['fg']}; padding: 6px;")

        if hasattr(self, 'duration_spin'):
            self.duration_spin.setStyleSheet(f"color: {colors['fg']}; padding: 6px;")

        if hasattr(self, 'start_date_input'):
            self.start_date_input.setStyleSheet(f"color: {colors['fg']}; padding: 6px;")

        if hasattr(self, 'end_date_input'):
            self.end_date_input.setStyleSheet(f"color: {colors['fg']}; padding: 6px;")

        if hasattr(self, 'contract_value_input'):
            self.contract_value_input.setStyleSheet(f"color: {colors['fg']}; padding: 6px;")

        if hasattr(self, 'unit_type_combo'):
            self.unit_type_combo.setStyleSheet(f"color: {colors['fg']}; padding: 6px;")

        if hasattr(self, 'unit_ton_combo'):
            self.unit_ton_combo.setStyleSheet(f"color: {colors['fg']}; padding: 6px;")

        if hasattr(self, 'amc_search_input'):
            self.amc_search_input.setStyleSheet(f"color: {colors['fg']}; padding: 6px;")

        if hasattr(self, 'visit_status_combo'):
            self.visit_status_combo.setStyleSheet(f"color: {colors['fg']}; padding: 6px;")

        # Refresh tab styles
        self._apply_theme_to_tabs()

    def _apply_theme_to_tabs(self):
        """Apply theme colors to tabs"""
        colors = self.theme_manager.get_colors()
        
        # Update tab widget style
        if hasattr(self, 'tabs'):
            self.tabs.setStyleSheet(f"""
                QTabWidget::pane {{
                    border: 1px solid {colors['border']};
                    background-color: {colors['bg']};
                }}
                QTabBar::tab {{
                    background-color: {colors['card_bg']};
                    color: {colors['fg']};
                    border: 1px solid {colors['border']};
                    padding: 8px 16px;
                    margin-right: 2px;
                }}
                QTabBar::tab:selected {{
                    background-color: {colors['primary']};
                    color: {colors['bg']};
                }}
                QTabBar::tab:hover {{
                    background-color: {colors['hover']};
                }}
            """)


class QWidgetWrapper(QWidget):
    """Wrapper for layout-only widgets"""
    def __init__(self, layout):
        super().__init__()
        self.setLayout(layout)
