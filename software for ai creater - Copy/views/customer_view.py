"""
Customer View - PySide6 Customer Management
Professional customer management with list, details, and service history
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea,
    QSizePolicy, QSplitter, QMessageBox, QMenu, QDialog, QDialogButtonBox,
    QFormLayout, QComboBox, QTextEdit, QGroupBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from utils.unified_theme import UnifiedTheme
from views.base_window import BaseView


class CustomerView(BaseView):
    """Customer management view with list and details"""

    def __init__(self):
        super().__init__()
        self.selected_customer_id = None
        self.customer_list = []

        self._setup_ui()
        self.load_customers()

    def update_theme_colors(self):
        """Update theme colors for proper dark theme support"""
        colors = self.theme_manager.get_colors()
        
        # Apply QPalette colors
        self.theme_manager.apply_palette(self)
        
        # Apply stylesheet
        self.setStyleSheet(self.theme_manager.get_main_stylesheet())
        
        # Apply theme directly to tables for proper alternating colors
        if hasattr(self, 'customer_table'):
            self.theme_manager.apply_table_theme(self.customer_table)
        
        if hasattr(self, 'invoices_table'):
            self.theme_manager.apply_table_theme(self.invoices_table)
        
        # Refresh data to ensure proper display
        self.load_customers()

    def _setup_ui(self):
        """Setup customer management UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Header
        self._create_header(main_layout)
        
        # Search and controls
        self._create_controls(main_layout)
        
        # Main content with splitter
        self._create_content(main_layout)
    
    def _create_header(self, layout):
        """Create header section"""
        colors = self.theme_manager.get_colors()

        title_label = QLabel("👥 CUSTOMER MANAGEMENT")
        title_label.setStyleSheet(f"""
            font-size: 18pt;
            font-weight: bold;
            color: {colors['primary']};
        """)
        layout.addWidget(title_label)

        subtitle_label = QLabel("View and manage customer information")
        subtitle_label.setStyleSheet(f"""
            font-size: 11pt;
            color: {colors['muted']};
        """)
        layout.addWidget(subtitle_label)
    
    def _create_controls(self, layout):
        """Create search and action controls"""
        colors = self.theme_manager.get_colors()
        
        control_frame = QFrame()
        control_layout = QHBoxLayout(control_frame)
        control_layout.setContentsMargins(0, 0, 0, 0)
        
        # Search
        search_label = QLabel("🔍 SEARCH:")
        search_label.setStyleSheet("font-weight: bold;")
        control_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, mobile, or address...")
        self.search_input.setMinimumWidth(300)
        self.search_input.textChanged.connect(self.load_customers)
        control_layout.addWidget(self.search_input)
        
        control_layout.addStretch()
        
        # Add customer button
        add_btn = QPushButton("➕ ADD CUSTOMER")
        add_btn.setObjectName("successButton")
        add_btn.clicked.connect(self.add_customer)
        control_layout.addWidget(add_btn)
        
        # Export button
        export_btn = QPushButton("📤 EXPORT")
        export_btn.setObjectName("primaryButton")
        export_btn.clicked.connect(self.export_customers)
        control_layout.addWidget(export_btn)
        
        layout.addWidget(control_frame)
    
    def _create_content(self, layout):
        """Create main content with splitter"""
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left pane - Customer list
        left_pane = self._create_customer_list()
        splitter.addWidget(left_pane)
        
        # Right pane - Customer details
        right_pane = self._create_customer_details()
        splitter.addWidget(right_pane)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([400, 600])
        
        layout.addWidget(splitter, 1)
    
    def _create_customer_list(self):
        """Create customer list pane"""
        colors = self.theme_manager.get_colors()
        
        pane = QFrame()
        layout = QVBoxLayout(pane)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header_label = QLabel("Customer List")
        header_label.setStyleSheet("font-size: 12pt; font-weight: bold;")
        layout.addWidget(header_label)
        
        # Table
        self.customer_table = QTableWidget()
        self.customer_table.setColumnCount(6)
        self.customer_table.setHorizontalHeaderLabels([
            'Name', 'Mobile', 'Services', 'Total (₹)', 'Pending (₹)', 'Last Visit'
        ])
        
        header = self.customer_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        
        self.customer_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.customer_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.customer_table.setAlternatingRowColors(True)
        self.customer_table.verticalHeader().setVisible(False)
        self.customer_table.itemSelectionChanged.connect(self.on_customer_select)
        
        layout.addWidget(self.customer_table)
        
        return pane
    
    def _create_customer_details(self):
        """Create customer details pane"""
        colors = self.theme_manager.get_colors()
        
        pane = QFrame()
        pane.setObjectName("cardFrame")
        pane.setStyleSheet(f"""
            QFrame#cardFrame {{
                background-color: {colors['card_bg']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
            }}
        """)
        
        layout = QVBoxLayout(pane)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header_label = QLabel("Customer Details")
        header_label.setStyleSheet("font-size: 12pt; font-weight: bold;")
        layout.addWidget(header_label)
        
        # Customer info
        self.customer_name_label = QLabel("Select a customer")
        self.customer_name_label.setStyleSheet(f"""
            font-size: 16pt;
            font-weight: bold;
            color: {colors['primary']};
        """)
        layout.addWidget(self.customer_name_label)

        self.customer_mobile_label = QLabel("")
        self.customer_mobile_label.setStyleSheet(f"color: {colors['muted']};")
        layout.addWidget(self.customer_mobile_label)

        self.customer_email_label = QLabel("")
        self.customer_email_label.setStyleSheet(f"color: {colors['muted']};")
        layout.addWidget(self.customer_email_label)

        self.customer_address_label = QLabel("")
        self.customer_address_label.setStyleSheet(f"color: {colors['muted']};")
        self.customer_address_label.setWordWrap(True)
        layout.addWidget(self.customer_address_label)

        # Separator
        separator = QFrame()
        separator.setFixedHeight(1)
        separator.setStyleSheet(f"background-color: {colors['border']};")
        layout.addWidget(separator)

        # Stats
        stats_layout = QFormLayout()
        stats_layout.setSpacing(10)

        self.stats_services = QLabel("0")
        self.stats_services.setStyleSheet(f"font-weight: bold; color: {colors['primary']};")
        stats_layout.addRow("Total Services:", self.stats_services)

        self.stats_total = QLabel("₹0.00")
        self.stats_total.setStyleSheet(f"font-weight: bold; color: {colors['primary']};")
        stats_layout.addRow("Total Amount:", self.stats_total)

        self.stats_pending = QLabel("₹0.00")
        self.stats_pending.setStyleSheet(f"font-weight: bold; color: {colors['danger']};")
        stats_layout.addRow("Pending Amount:", self.stats_pending)

        self.stats_last = QLabel("Never")
        self.stats_last.setStyleSheet(f"font-weight: bold; color: {colors['primary']};")
        stats_layout.addRow("Last Service:", self.stats_last)
        
        layout.addLayout(stats_layout)
        
        # Service history
        history_label = QLabel("Service History")
        history_label.setStyleSheet("font-size: 12pt; font-weight: bold; margin-top: 15px;")
        layout.addWidget(history_label)
        
        self.invoices_table = QTableWidget()
        self.invoices_table.setColumnCount(7)
        self.invoices_table.setHorizontalHeaderLabels([
            'Invoice', 'Date', 'Amount', 'Advance', 'Balance', 'Status', 'Actions'
        ])
        
        header = self.invoices_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for i in range(1, 7):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
        
        self.invoices_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.invoices_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.invoices_table.setAlternatingRowColors(True)
        self.invoices_table.verticalHeader().setVisible(False)
        self.invoices_table.setMinimumHeight(150)
        self.invoices_table.cellDoubleClicked.connect(self.on_invoice_double_click)
        
        layout.addWidget(self.invoices_table)
        
        # Action buttons
        btn_layout = QHBoxLayout()

        # WhatsApp button (COMMENTED OUT - Will add later)
        # whatsapp_btn = QPushButton("📱 WhatsApp")
        # whatsapp_btn.setStyleSheet("...")
        # whatsapp_btn.clicked.connect(self.send_whatsapp_message)
        # btn_layout.addWidget(whatsapp_btn)

        edit_btn = QPushButton("Edit")
        edit_btn.setObjectName("primaryButton")
        edit_btn.clicked.connect(self.edit_customer)
        btn_layout.addWidget(edit_btn)

        new_inv_btn = QPushButton("New Invoice")
        new_inv_btn.setObjectName("successButton")
        new_inv_btn.clicked.connect(self.new_invoice_for_customer)
        btn_layout.addWidget(new_inv_btn)

        delete_btn = QPushButton("Delete")
        delete_btn.setObjectName("dangerButton")
        delete_btn.clicked.connect(self.delete_customer)
        btn_layout.addWidget(delete_btn)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        return pane
    
    def load_customers(self):
        """Load customers from database"""
        self.run_in_thread(
            self._load_customers_thread,
            self._update_customer_list
        )
    
    def _load_customers_thread(self):
        """Load customers in background"""
        from database.db_connection import DatabaseContext
        
        search_term = self.search_input.text().strip()
        
        with DatabaseContext() as db:
            query = """
            SELECT
                c.id, c.name, c.mobile, c.email, c.address, c.landmark,
                DATE(c.created_at) as created_date,
                (SELECT COUNT(*) FROM invoices i WHERE i.customer_id = c.id AND i.is_active = TRUE) as total_services,
                (SELECT COALESCE(SUM(i.total_amount), 0) FROM invoices i WHERE i.customer_id = c.id AND i.is_active = TRUE) as total_amount,
                (SELECT COALESCE(SUM(i.balance_amount), 0) FROM invoices i WHERE i.customer_id = c.id AND i.is_active = TRUE) as pending_amount,
                (SELECT MAX(DATE(i.created_at)) FROM invoices i WHERE i.customer_id = c.id AND i.is_active = TRUE) as last_visit
            FROM customers c
            WHERE c.is_active = TRUE
            """
            
            params = []
            if search_term:
                query += " AND (c.name LIKE %s OR c.mobile LIKE %s OR c.address LIKE %s)"
                params.extend([f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"])
            
            query += " ORDER BY c.name"
            
            return db.execute_query(query, params, fetch_all=True)
    
    def _update_customer_list(self, customers):
        """Update customer table"""
        self.customer_list = customers or []
        self.customer_table.setRowCount(0)
        
        for customer in self.customer_list:
            row = self.customer_table.rowCount()
            self.customer_table.insertRow(row)
            
            last_visit = customer['last_visit'].strftime('%d-%m-%Y') if customer['last_visit'] else 'Never'
            
            self.customer_table.setItem(row, 0, QTableWidgetItem(customer['name']))
            self.customer_table.setItem(row, 1, QTableWidgetItem(customer['mobile']))
            self.customer_table.setItem(row, 2, QTableWidgetItem(str(customer['total_services'])))
            self.customer_table.setItem(row, 3, QTableWidgetItem(f"₹{customer['total_amount']:,.2f}"))
            self.customer_table.setItem(row, 4, QTableWidgetItem(f"₹{customer['pending_amount']:,.2f}"))
            self.customer_table.setItem(row, 5, QTableWidgetItem(last_visit))
    
    def on_customer_select(self):
        """Handle customer selection"""
        selected_rows = self.customer_table.selectedItems()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        customer = self.customer_list[row]
        self.selected_customer_id = customer['id']
        self.load_customer_details(customer['id'])

    def load_customer_details(self, customer_id):
        """Load customer details"""
        self.run_in_thread(
            self._load_customer_details_thread,
            self._update_customer_details,
            None,  # on_error - use default handler
            customer_id
        )
    
    def _load_customer_details_thread(self, customer_id):
        """Load customer details in background"""
        from database.db_connection import DatabaseContext
        
        with DatabaseContext() as db:
            # Get customer details
            query = """
            SELECT
                c.*,
                (SELECT COUNT(*) FROM invoices i WHERE i.customer_id = c.id AND i.is_active = TRUE) as total_services,
                (SELECT COALESCE(SUM(i.total_amount), 0) FROM invoices i WHERE i.customer_id = c.id AND i.is_active = TRUE) as total_amount,
                (SELECT COALESCE(SUM(i.balance_amount), 0) FROM invoices i WHERE i.customer_id = c.id AND i.is_active = TRUE) as pending_amount,
                (SELECT MAX(DATE(i.created_at)) FROM invoices i WHERE i.customer_id = c.id AND i.is_active = TRUE) as last_service
            FROM customers c
            WHERE c.id = %s
            """
            customer = db.execute_query(query, (customer_id,), fetch_one=True)
            
            # Get invoices
            query = """
            SELECT
                i.id, i.invoice_number, DATE(i.created_at) as invoice_date,
                i.total_amount, i.advance_payment, i.balance_amount,
                i.payment_status, i.payment_mode
            FROM invoices i
            WHERE i.customer_id = %s AND i.is_active = TRUE
            ORDER BY i.created_at DESC
            LIMIT 20
            """
            invoices = db.execute_query(query, (customer_id,), fetch_all=True)
            
            return {'customer': customer, 'invoices': invoices}
    
    def _update_customer_details(self, data):
        """Update customer details UI"""
        customer = data['customer']
        invoices = data['invoices']
        
        if not customer:
            return
        
        # Update basic info
        self.customer_name_label.setText(customer['name'])
        self.customer_mobile_label.setText(f"📱 {customer['mobile']}")
        
        if customer['email']:
            self.customer_email_label.setText(f"✉️ {customer['email']}")
            self.customer_email_label.show()
        else:
            self.customer_email_label.hide()
        
        address_parts = []
        if customer['address']:
            address_parts.append(customer['address'])
        if customer['landmark']:
            address_parts.append(f"Landmark: {customer['landmark']}")
        
        if address_parts:
            self.customer_address_label.setText("📍 " + " | ".join(address_parts))
            self.customer_address_label.show()
        else:
            self.customer_address_label.hide()
        
        # Update stats
        self.stats_services.setText(str(customer['total_services']))
        self.stats_total.setText(f"₹{customer['total_amount']:,.2f}")
        self.stats_pending.setText(f"₹{customer['pending_amount']:,.2f}")
        
        if customer['pending_amount'] > 0:
            self.stats_pending.setStyleSheet("font-weight: bold; color: #dc2626;")
        else:
            self.stats_pending.setStyleSheet("font-weight: bold; color: #059669;")
        
        if customer['last_service']:
            self.stats_last.setText(customer['last_service'].strftime('%d-%m-%Y'))
        else:
            self.stats_last.setText("Never")
        
        # Update invoices table
        self.invoices_table.setRowCount(0)
        for inv in invoices:
            row = self.invoices_table.rowCount()
            self.invoices_table.insertRow(row)
            
            self.invoices_table.setItem(row, 0, QTableWidgetItem(inv['invoice_number']))
            self.invoices_table.setItem(row, 1, QTableWidgetItem(inv['invoice_date'].strftime('%d-%m-%Y')))
            self.invoices_table.setItem(row, 2, QTableWidgetItem(f"₹{inv['total_amount']:,.2f}"))
            self.invoices_table.setItem(row, 3, QTableWidgetItem(f"₹{inv['advance_payment']:,.2f}"))
            self.invoices_table.setItem(row, 4, QTableWidgetItem(f"₹{inv['balance_amount']:,.2f}"))
            self.invoices_table.setItem(row, 5, QTableWidgetItem(inv['payment_status']))
            self.invoices_table.setItem(row, 6, QTableWidgetItem("👁️ 📥 ✏️"))
    
    def on_invoice_double_click(self, row, col):
        """Handle invoice double-click"""
        menu = QMenu(self)
        menu.addAction("View Invoice", lambda: self.view_invoice(row))
        menu.addAction("Download PDF", lambda: self.download_invoice_pdf(row))
        menu.addAction("Edit Invoice", lambda: self.edit_invoice(row))
        
        # Get cell position correctly
        item = self.invoices_table.item(row, col)
        if item:
            rect = self.invoices_table.visualItemRect(item)
            menu.exec(self.invoices_table.viewport().mapToGlobal(rect.topLeft()))
    
    def view_invoice(self, row):
        """View invoice details"""
        self.show_success_message("View invoice feature - coming soon")
    
    def download_invoice_pdf(self, row):
        """Download invoice PDF"""
        self.show_success_message("Download PDF feature - coming soon")
    
    def edit_invoice(self, row):
        """Edit invoice"""
        self.show_success_message("Edit invoice feature - coming soon")
    
    def add_customer(self):
        """Add new customer"""
        dialog = AddCustomerDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_customers()
            self.show_success_message("Customer added successfully")
    
    def edit_customer(self):
        """Edit selected customer"""
        if not self.selected_customer_id:
            self.show_warning_message("Please select a customer to edit")
            return
        
        dialog = EditCustomerDialog(self.selected_customer_id, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_customers()
            if self.selected_customer_id:
                self.load_customer_details(self.selected_customer_id)
            self.show_success_message("Customer updated successfully")
    
    def delete_customer(self):
        """Delete selected customer"""
        if not self.selected_customer_id:
            self.show_warning_message("Please select a customer to delete")
            return
        
        if self.show_question("Are you sure you want to delete this customer?"):
            from controllers.customer_controller import CustomerController
            from database.db_connection import DatabaseConnection
            
            db = DatabaseConnection()
            controller = CustomerController(db)
            controller.delete_customer(self.selected_customer_id)
            
            self.selected_customer_id = None
            self.load_customers()
            self.show_success_message("Customer deleted successfully")
    
    def new_invoice_for_customer(self):
        """Create new invoice for selected customer"""
        if not self.selected_customer_id:
            self.show_warning_message("Please select a customer")
            return

        # Navigate to invoice view
        parent = self.parent()
        while parent:
            if hasattr(parent, '_show_invoice'):
                parent._show_invoice()
                # TODO: Pre-fill customer in invoice view
                break
            parent = parent.parent()

    def send_whatsapp_message(self):
        """Send WhatsApp message to customer"""
        try:
            from utils.whatsapp_helper import WhatsAppHelper
            
            if not self.selected_customer_id:
                self.show_warning_message("Please select a customer first")
                return
            
            # Get customer data
            from database.db_connection import DatabaseContext
            
            with DatabaseContext() as db:
                query = "SELECT * FROM customers WHERE id = %s"
                customer = db.execute_query(query, (self.selected_customer_id,), fetch_one=True)
            
            if not customer:
                self.show_warning_message("Customer not found")
                return
            
            customer_name = customer['name']
            customer_mobile = customer['mobile']
            
            if not customer_mobile:
                self.show_warning_message("Customer mobile number not available")
                return
            
            # Show template selection dialog
            from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel

            dialog = QDialog(self)
            dialog.setWindowTitle("Select WhatsApp Message")
            dialog.setMinimumWidth(400)

            layout = QVBoxLayout()

            # WhatsApp green color (theme-aware)
            whatsapp_green = "#25D366"
            whatsapp_dark = "#128C7E"

            title = QLabel(f"📱 Send message to: {customer_name}")
            title.setStyleSheet(f"font-size: 14pt; font-weight: bold; color: {whatsapp_green};")
            layout.addWidget(title)

            subtitle = QLabel("Choose a message template:")
            subtitle.setStyleSheet("font-size: 11pt;")
            layout.addWidget(subtitle)

            # Template buttons
            templates = [
                ("🙏 Greeting", 'greeting'),
                ("✅ Service Confirmed", 'service_confirm'),
                ("💳 Payment Reminder", 'payment_reminder'),
                ("🌟 Thank You", 'thank_you'),
                ("⭐ Feedback Request", 'feedback_request'),
            ]

            for btn_text, template_key in templates:
                btn = QPushButton(btn_text)
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {whatsapp_green};
                        color: white;
                        border: none;
                        padding: 10px 16px;
                        border-radius: 6px;
                        font-weight: bold;
                        text-align: left;
                    }}
                    QPushButton:hover {{
                        background-color: {whatsapp_dark};
                    }}
                """)
                btn.clicked.connect(lambda checked, key=template_key:
                                   self._send_template_and_close(dialog, key, customer_mobile, customer_name))
                layout.addWidget(btn)

            dialog.setLayout(layout)
            dialog.exec()
            
        except Exception as e:
            self.show_error_message(f"Error: {str(e)}")

    def _send_template_and_close(self, dialog, template_key, phone, name):
        """Send template and close dialog"""
        try:
            from utils.whatsapp_helper import WhatsAppHelper
            
            data = {
                'phone': phone,
                'name': name,
                'service_type': 'AC Service',
                'location': 'Mumbai',
                'amount': '0',
                'invoice_number': 'INV-XXXX',
                'date': 'DD/MM/YYYY',
                'expiry_date': 'DD/MM/YYYY',
            }
            
            success = WhatsAppHelper.send_template(template_key, **data)
            
            if success:
                self.show_success_message(f"✅ WhatsApp opened for '{template_key}' message")
            else:
                self.show_warning_message("Failed to open WhatsApp")
            
            dialog.accept()
            
        except Exception as e:
            self.show_error_message(f"Error: {str(e)}")
    
    def export_customers(self):
        """Export customers to Excel"""
        self.show_success_message("Export feature - coming soon")
    
    def refresh_data(self):
        """Refresh customer data"""
        self.load_customers()


class AddCustomerDialog(QDialog):
    """Dialog for adding new customer"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Customer")
        self.setMinimumWidth(500)
        self.setStyleSheet(parent.theme_manager.get_main_stylesheet() if parent else "")
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup dialog UI"""
        layout = QVBoxLayout(self)
        
        form = QFormLayout()
        form.setSpacing(15)
        
        self.name_input = QLineEdit()
        form.addRow("Name *:", self.name_input)
        
        self.mobile_input = QLineEdit()
        form.addRow("Mobile *:", self.mobile_input)
        
        self.email_input = QLineEdit()
        form.addRow("Email:", self.email_input)
        
        self.address_input = QTextEdit()
        self.address_input.setMaximumHeight(80)
        form.addRow("Address:", self.address_input)
        
        self.landmark_input = QLineEdit()
        form.addRow("Landmark:", self.landmark_input)
        
        layout.addLayout(form)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._validate_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def _validate_and_accept(self):
        """Validate and save customer"""
        name = self.name_input.text().strip()
        mobile = self.mobile_input.text().strip()
        
        if not name or not mobile:
            QMessageBox.warning(self, "Validation", "Name and Mobile are required")
            return
        
        # Save customer
        from controllers.customer_controller import CustomerController
        from database.db_connection import DatabaseConnection
        
        db = DatabaseConnection()
        controller = CustomerController(db)
        controller.add_customer(
            name=name,
            mobile=mobile,
            email=self.email_input.text().strip() or None,
            address=self.address_input.toPlainText().strip() or None,
            landmark=self.landmark_input.text().strip() or None
        )
        
        self.accept()


class EditCustomerDialog(QDialog):
    """Dialog for editing customer"""
    
    def __init__(self, customer_id, parent=None):
        super().__init__(parent)
        self.customer_id = customer_id
        self.setWindowTitle("Edit Customer")
        self.setMinimumWidth(500)
        self.setStyleSheet(parent.theme_manager.get_main_stylesheet() if parent else "")
        
        self._setup_ui()
        self._load_customer()
    
    def _setup_ui(self):
        """Setup dialog UI"""
        layout = QVBoxLayout(self)
        
        form = QFormLayout()
        form.setSpacing(15)
        
        self.name_input = QLineEdit()
        form.addRow("Name *:", self.name_input)
        
        self.mobile_input = QLineEdit()
        form.addRow("Mobile *:", self.mobile_input)
        
        self.email_input = QLineEdit()
        form.addRow("Email:", self.email_input)
        
        self.address_input = QTextEdit()
        self.address_input.setMaximumHeight(80)
        form.addRow("Address:", self.address_input)
        
        self.landmark_input = QLineEdit()
        form.addRow("Landmark:", self.landmark_input)
        
        layout.addLayout(form)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._validate_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def _load_customer(self):
        """Load customer data"""
        from database.db_connection import DatabaseContext
        
        with DatabaseContext() as db:
            query = "SELECT * FROM customers WHERE id = %s"
            customer = db.execute_query(query, (self.customer_id,), fetch_one=True)
            
            if customer:
                self.name_input.setText(customer['name'])
                self.mobile_input.setText(customer['mobile'])
                self.email_input.setText(customer.get('email') or '')
                self.address_input.setText(customer.get('address') or '')
                self.landmark_input.setText(customer.get('landmark') or '')
    
    def _validate_and_accept(self):
        """Validate and save customer"""
        name = self.name_input.text().strip()
        mobile = self.mobile_input.text().strip()
        
        if not name or not mobile:
            QMessageBox.warning(self, "Validation", "Name and Mobile are required")
            return
        
        # Update customer
        from controllers.customer_controller import CustomerController
        from database.db_connection import DatabaseConnection
        
        db = DatabaseConnection()
        controller = CustomerController(db)
        controller.update_customer(
            customer_id=self.customer_id,
            name=name,
            mobile=mobile,
            email=self.email_input.text().strip() or None,
            address=self.address_input.toPlainText().strip() or None,
            landmark=self.landmark_input.text().strip() or None
        )
        
        self.accept()
