"""
Technician View - PySide6 Technician Management
Professional technician management with performance tracking
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea,
    QSizePolicy, QSplitter, QMessageBox, QFormLayout, QComboBox,
    QTextEdit, QGroupBox, QDateEdit, QDialog, QDialogButtonBox
)
from PySide6.QtCore import Qt, QDate
from datetime import datetime, timedelta

from utils.unified_theme import UnifiedTheme
from views.base_window import BaseView


class TechnicianView(BaseView):
    """Technician management view"""

    def __init__(self):
        super().__init__()
        self.selected_technician_id = None
        self.technician_list = []

        self._setup_ui()
        self.load_technicians()

    def update_theme_colors(self):
        """Update theme colors for proper dark theme support"""
        colors = self.theme_manager.get_colors()
        
        # Apply QPalette colors
        self.theme_manager.apply_palette(self)
        
        # Apply stylesheet
        self.setStyleSheet(self.theme_manager.get_main_stylesheet())
        
        # Apply theme directly to all tables for proper alternating colors
        if hasattr(self, 'technician_table'):
            self.theme_manager.apply_table_theme(self.technician_table)
        
        if hasattr(self, 'services_table'):
            self.theme_manager.apply_table_theme(self.services_table)
        
        if hasattr(self, 'customers_table'):
            self.theme_manager.apply_table_theme(self.customers_table)
        
        # Refresh data to ensure proper display
        self.load_technicians()

    def _setup_ui(self):
        """Setup technician management UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Header
        self._create_header(main_layout)

        # Controls
        self._create_controls(main_layout)

        # Main content with splitter
        self._create_content(main_layout)
        
        # Store photo path
        self.photo_path = None
    
    def _create_header(self, layout):
        """Create header section"""
        colors = self.theme_manager.get_colors()

        title_label = QLabel("🔧 TECHNICIAN MANAGEMENT")
        title_label.setStyleSheet(f"""
            font-size: 18pt;
            font-weight: bold;
            color: {colors['primary']};
        """)
        layout.addWidget(title_label)

        subtitle_label = QLabel("Manage technician profiles and performance")
        subtitle_label.setStyleSheet(f"""
            font-size: 11pt;
            color: {colors['muted']};
        """)
        layout.addWidget(subtitle_label)
    
    def _create_controls(self, layout):
        """Create control buttons"""
        control_layout = QHBoxLayout()

        # Date range
        date_label = QLabel("📅 DATE RANGE:")
        date_label.setStyleSheet("font-weight: bold;")
        control_layout.addWidget(date_label)

        self.start_date_input = QDateEdit()
        self.start_date_input.setDate(QDate.currentDate().addDays(-30))
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setDisplayFormat("dd-MM-yyyy")
        control_layout.addWidget(self.start_date_input)

        to_label = QLabel("TO")
        control_layout.addWidget(to_label)

        self.end_date_input = QDateEdit()
        self.end_date_input.setDate(QDate.currentDate())
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setDisplayFormat("dd-MM-yyyy")
        control_layout.addWidget(self.end_date_input)

        filter_btn = QPushButton("🔍 FILTER")
        filter_btn.setObjectName("primaryButton")
        filter_btn.clicked.connect(self.load_technicians)
        control_layout.addWidget(filter_btn)
        
        # Export button
        export_btn = QPushButton("📊 EXPORT")
        export_btn.setObjectName("secondaryButton")
        export_btn.clicked.connect(self.export_to_excel)
        control_layout.addWidget(export_btn)

        control_layout.addStretch()

        add_btn = QPushButton("➕ ADD TECHNICIAN")
        add_btn.setObjectName("successButton")
        add_btn.clicked.connect(self.add_technician)
        control_layout.addWidget(add_btn)

        layout.addLayout(control_layout)
    
    def _create_content(self, layout):
        """Create main content with splitter"""
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left pane - Technician list
        left_pane = self._create_technician_list()
        splitter.addWidget(left_pane)
        
        # Right pane - Technician details
        right_pane = self._create_technician_details()
        splitter.addWidget(right_pane)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        splitter.setSizes([300, 600])
        
        layout.addWidget(splitter, 1)
    
    def _create_technician_list(self):
        """Create technician list pane"""
        colors = self.theme_manager.get_colors()

        pane = QFrame()
        layout = QVBoxLayout(pane)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header_label = QLabel("Technician List")
        header_label.setStyleSheet("font-size: 12pt; font-weight: bold;")
        layout.addWidget(header_label)

        # Table
        self.technician_table = QTableWidget()
        self.technician_table.setColumnCount(6)
        self.technician_table.setHorizontalHeaderLabels([
            'Status', 'Name', 'Mobile', 'Territory', 'Services', 'Collected (₹)'
        ])

        header = self.technician_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)

        self.technician_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.technician_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.technician_table.setAlternatingRowColors(True)
        self.technician_table.verticalHeader().setVisible(False)
        self.technician_table.itemSelectionChanged.connect(self.on_technician_select)

        layout.addWidget(self.technician_table)

        return pane
    
    def _create_technician_details(self):
        """Create technician details pane"""
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
        header_label = QLabel("Technician Details")
        header_label.setStyleSheet("font-size: 12pt; font-weight: bold;")
        layout.addWidget(header_label)
        
        # Technician info
        self.tech_name_label = QLabel("Select a technician")
        self.tech_name_label.setStyleSheet(f"""
            font-size: 16pt;
            font-weight: bold;
            color: {colors['primary']};
        """)
        layout.addWidget(self.tech_name_label)

        self.tech_mobile_label = QLabel("")
        self.tech_mobile_label.setStyleSheet(f"color: {colors['muted']};")
        layout.addWidget(self.tech_mobile_label)

        self.tech_address_label = QLabel("")
        self.tech_address_label.setStyleSheet(f"color: {colors['muted']};")
        self.tech_address_label.setWordWrap(True)
        layout.addWidget(self.tech_address_label)

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

        self.stats_collected = QLabel("₹0.00")
        self.stats_collected.setStyleSheet(f"font-weight: bold; color: {colors['primary']};")
        stats_layout.addRow("Amount Collected:", self.stats_collected)

        self.stats_pending = QLabel("₹0.00")
        self.stats_pending.setStyleSheet(f"font-weight: bold; color: {colors['danger']};")
        stats_layout.addRow("Pending Amount:", self.stats_pending)

        self.stats_rating = QLabel("N/A")
        self.stats_rating.setStyleSheet(f"font-weight: bold; color: {colors['primary']};")
        stats_layout.addRow("Performance Rating:", self.stats_rating)
        
        layout.addLayout(stats_layout)
        
        # Separator
        separator2 = QFrame()
        separator2.setFixedHeight(1)
        separator2.setStyleSheet(f"background-color: {colors['border']};")
        layout.addWidget(separator2)
        
        # Assigned services
        services_label = QLabel("📋 Assigned Services")
        services_label.setStyleSheet("font-size: 12pt; font-weight: bold; margin-top: 15px;")
        layout.addWidget(services_label)

        self.services_table = QTableWidget()
        self.services_table.setColumnCount(5)
        self.services_table.setHorizontalHeaderLabels([
            'Invoice', 'Customer', 'Date', 'Amount', 'Status'
        ])

        header = self.services_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

        self.services_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.services_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.services_table.setAlternatingRowColors(True)
        self.services_table.verticalHeader().setVisible(False)
        self.services_table.setMinimumHeight(150)

        layout.addWidget(self.services_table)

        # Customers Served Table (NEW)
        customers_label = QLabel("👥 Customers Served (Contact Details)")
        customers_label.setStyleSheet(f"font-size: 12pt; font-weight: bold; margin-top: 15px; color: {colors['primary']};")
        layout.addWidget(customers_label)

        self.customers_table = QTableWidget()
        self.customers_table.setColumnCount(5)
        self.customers_table.setHorizontalHeaderLabels([
            'Customer Name', 'Mobile', 'Address', 'Service Date', 'Service Type'
        ])

        header = self.customers_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

        self.customers_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.customers_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.customers_table.setAlternatingRowColors(True)
        self.customers_table.verticalHeader().setVisible(False)
        self.customers_table.setMinimumHeight(200)

        layout.addWidget(self.customers_table)

        # Action buttons
        btn_layout = QHBoxLayout()

        edit_btn = QPushButton("Edit")
        edit_btn.setObjectName("primaryButton")
        edit_btn.clicked.connect(self.edit_technician)
        btn_layout.addWidget(edit_btn)

        delete_btn = QPushButton("Delete")
        delete_btn.setObjectName("dangerButton")
        delete_btn.clicked.connect(self.delete_technician)
        btn_layout.addWidget(delete_btn)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        return pane
    
    def load_technicians(self):
        """Load technicians from database"""
        self.run_in_thread(
            self._load_technicians_thread,
            self._update_technician_list
        )
    
    def _load_technicians_thread(self):
        """Load technicians in background"""
        from database.db_connection import DatabaseContext

        start_date = self.start_date_input.date().toString("yyyy-MM-dd")
        end_date = self.end_date_input.date().toString("yyyy-MM-dd")

        with DatabaseContext() as db:
            query = """
            SELECT
                t.id, t.name, t.mobile, t.territory, t.availability_status,
                (SELECT COUNT(*) FROM invoices i
                 WHERE i.technician_id = t.id AND i.is_active = TRUE
                 AND DATE(i.created_at) BETWEEN %s AND %s) as total_services,
                (SELECT COALESCE(SUM(i.advance_payment), 0) FROM invoices i
                 WHERE i.technician_id = t.id AND i.is_active = TRUE
                 AND DATE(i.created_at) BETWEEN %s AND %s) as collected_amount
            FROM technicians t
            WHERE t.is_active = TRUE
            ORDER BY t.name
            """

            return db.execute_query(
                query,
                (start_date, end_date, start_date, end_date),
                fetch_all=True
            )
    
    def _update_technician_list(self, technicians):
        """Update technician table"""
        self.technician_list = technicians or []
        self.technician_table.setRowCount(0)

        for tech in self.technician_list:
            row = self.technician_table.rowCount()
            self.technician_table.insertRow(row)

            # Status badge with color
            status = tech.get('availability_status', 'Available')
            status_item = QTableWidgetItem(status)
            if status == 'Available':
                status_item.setBackground(Qt.GlobalColor.darkGreen)
                status_item.setForeground(Qt.GlobalColor.white)
            elif status == 'Busy':
                status_item.setBackground(Qt.GlobalColor.darkOrange)
                status_item.setForeground(Qt.GlobalColor.white)
            elif status == 'On Leave':
                status_item.setBackground(Qt.GlobalColor.darkRed)
                status_item.setForeground(Qt.GlobalColor.white)
            else:
                status_item.setBackground(Qt.GlobalColor.gray)
                status_item.setForeground(Qt.GlobalColor.white)
            self.technician_table.setItem(row, 0, status_item)

            self.technician_table.setItem(row, 1, QTableWidgetItem(tech['name']))
            self.technician_table.setItem(row, 2, QTableWidgetItem(tech['mobile']))
            self.technician_table.setItem(row, 3, QTableWidgetItem(tech.get('territory') or 'N/A'))
            self.technician_table.setItem(row, 4, QTableWidgetItem(str(tech['total_services'])))
            self.technician_table.setItem(row, 5, QTableWidgetItem(f"Rs.{tech['collected_amount']:,.2f}"))
    
    def on_technician_select(self):
        """Handle technician selection"""
        selected_rows = self.technician_table.selectedItems()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        technician = self.technician_list[row]
        self.selected_technician_id = technician['id']
        self.load_technician_details(technician['id'])
    
    def load_technician_details(self, technician_id):
        """Load technician details"""
        # Use run_in_thread with proper argument passing
        def load_data():
            return self._load_technician_details_thread(technician_id)
        
        self.run_in_thread(
            load_data,
            self._update_technician_details
        )
    
    def _load_technician_details_thread(self, technician_id):
        """Load technician details in background"""
        from database.db_connection import DatabaseContext

        start_date = self.start_date_input.date().toString("yyyy-MM-dd")
        end_date = self.end_date_input.date().toString("yyyy-MM-dd")

        with DatabaseContext() as db:
            # Get technician details
            query = """
            SELECT
                t.*,
                (SELECT COUNT(*) FROM invoices i
                 WHERE i.technician_id = t.id AND i.is_active = TRUE
                 AND DATE(i.created_at) BETWEEN %s AND %s) as total_services,
                (SELECT COALESCE(SUM(i.advance_payment), 0) FROM invoices i
                 WHERE i.technician_id = t.id AND i.is_active = TRUE
                 AND DATE(i.created_at) BETWEEN %s AND %s) as collected_amount,
                (SELECT COALESCE(SUM(i.balance_amount), 0) FROM invoices i
                 WHERE i.technician_id = t.id AND i.is_active = TRUE
                 AND DATE(i.created_at) BETWEEN %s AND %s) as pending_amount
            FROM technicians t
            WHERE t.id = %s
            """

            technician = db.execute_query(
                query,
                (start_date, end_date, start_date, end_date, start_date, end_date, technician_id),
                fetch_one=True
            )

            # Get assigned services
            services_query = """
            SELECT
                i.invoice_number, c.name as customer_name,
                DATE(i.created_at) as service_date,
                i.total_amount, i.payment_status
            FROM invoices i
            JOIN customers c ON i.customer_id = c.id
            WHERE i.technician_id = %s AND i.is_active = TRUE
            AND DATE(i.created_at) BETWEEN %s AND %s
            ORDER BY i.created_at DESC
            LIMIT 20
            """

            services = db.execute_query(
                services_query,
                (technician_id, start_date, end_date),
                fetch_all=True
            )

            # Get customers served with full details (NEW)
            customers_query = """
            SELECT 
                c.name as customer_name,
                c.mobile as customer_mobile,
                c.address as customer_address,
                MAX(DATE(i.created_at)) as service_date,
                GROUP_CONCAT(DISTINCT s.service_name ORDER BY s.service_name SEPARATOR ', ') as services_performed
            FROM invoices i
            JOIN customers c ON i.customer_id = c.id
            LEFT JOIN invoice_items ii ON i.id = ii.invoice_id
            LEFT JOIN services s ON ii.service_id = s.id
            WHERE i.technician_id = %s AND i.is_active = TRUE
            AND DATE(i.created_at) BETWEEN %s AND %s
            GROUP BY c.id, c.name, c.mobile, c.address
            ORDER BY service_date DESC
            LIMIT 50
            """

            customers = db.execute_query(
                customers_query,
                (technician_id, start_date, end_date),
                fetch_all=True
            )

            return {
                'technician': technician,
                'services': services,
                'customers': customers
            }
    
    def _update_technician_details(self, data):
        """Update technician details UI"""
        technician = data['technician']
        services = data['services']
        
        if not technician:
            return
        
        # Update basic info
        self.tech_name_label.setText(technician['name'])
        self.tech_mobile_label.setText(f"📱 {technician['mobile']}")
        
        if technician.get('address'):
            self.tech_address_label.setText(f"📍 {technician['address']}")
            self.tech_address_label.show()
        else:
            self.tech_address_label.hide()
        
        # Update stats
        self.stats_services.setText(str(technician['total_services']))
        self.stats_collected.setText(f"₹{technician['collected_amount']:,.2f}")
        self.stats_pending.setText(f"₹{technician['pending_amount']:,.2f}")
        
        # Calculate rating (placeholder)
        if technician['total_services'] > 0:
            rating = "⭐⭐⭐⭐⭐" if technician['total_services'] > 50 else "⭐⭐⭐⭐"
            self.stats_rating.setText(rating)
        else:
            self.stats_rating.setText("N/A")
        
        # Update services table
        self.services_table.setRowCount(0)
        for service in (services or []):
            row = self.services_table.rowCount()
            self.services_table.insertRow(row)
            
            self.services_table.setItem(row, 0, QTableWidgetItem(service['invoice_number']))
            self.services_table.setItem(row, 1, QTableWidgetItem(service['customer_name']))
            self.services_table.setItem(row, 2, QTableWidgetItem(service['service_date'].strftime('%d-%m-%Y')))
            self.services_table.setItem(row, 3, QTableWidgetItem(f"₹{service['total_amount']:,.2f}"))
            self.services_table.setItem(row, 4, QTableWidgetItem(service['payment_status']))
            
        # Update customers table (NEW)
        self.customers_table.setRowCount(0)
        for customer in (data.get('customers') or []):
            row = self.customers_table.rowCount()
            self.customers_table.insertRow(row)
            
            # Customer Name
            name_item = QTableWidgetItem(customer['customer_name'])
            name_item.setToolTip(customer['customer_name'])
            self.customers_table.setItem(row, 0, name_item)
            
            # Mobile
            mobile_item = QTableWidgetItem(customer['customer_mobile'])
            mobile_item.setToolTip(f"Call: {customer['customer_mobile']}")
            self.customers_table.setItem(row, 1, mobile_item)
            
            # Address
            address_item = QTableWidgetItem(customer['customer_address'] or 'N/A')
            address_item.setToolTip(customer['customer_address'] or 'No address')
            self.customers_table.setItem(row, 2, address_item)
            
            # Service Date
            date_str = customer['service_date'].strftime('%d-%m-%Y') if customer['service_date'] else 'N/A'
            date_item = QTableWidgetItem(date_str)
            self.customers_table.setItem(row, 3, date_item)
            
            # Service Type
            services_text = customer['services_performed'] or 'General Service'
            services_item = QTableWidgetItem(services_text)
            services_item.setToolTip(services_text)
            self.customers_table.setItem(row, 4, services_item)
    
    def add_technician(self):
        """Add new technician"""
        dialog = AddTechnicianDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_technicians()
            self.show_success_message("Technician added successfully")
    
    def edit_technician(self):
        """Edit selected technician"""
        if not self.selected_technician_id:
            self.show_warning_message("Please select a technician to edit")
            return
        
        dialog = EditTechnicianDialog(self.selected_technician_id, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_technicians()
            if self.selected_technician_id:
                self.load_technician_details(self.selected_technician_id)
            self.show_success_message("Technician updated successfully")
    
    def delete_technician(self):
        """Delete selected technician"""
        if not self.selected_technician_id:
            self.show_warning_message("Please select a technician to delete")
            return
        
        if self.show_question("Are you sure you want to delete this technician?"):
            from database.db_connection import DatabaseContext
            
            with DatabaseContext() as db:
                db.execute_query(
                    "UPDATE technicians SET is_active = FALSE WHERE id = %s",
                    (self.selected_technician_id,)
                )
            
            self.selected_technician_id = None
            self.load_technicians()
            self.show_success_message("Technician deleted successfully")
    
    def refresh_data(self):
        """Refresh technician data"""
        self.load_technicians()
    
    def export_to_excel(self):
        """Export technician data to Excel"""
        try:
            from openpyxl import Workbook
            from PySide6.QtWidgets import QFileDialog
            from datetime import datetime
            
            # Create workbook
            wb = Workbook()
            ws = wb.active
            ws.title = "Technicians"
            
            # Headers
            headers = [
                'Status', 'Name', 'Mobile', 'Territory', 'Email', 'Address',
                'Commission %', 'Availability', 'Joining Date', 'Emergency Contact',
                'Total Services', 'Amount Collected', 'Pending Amount'
            ]
            ws.append(headers)
            
            # Get data
            start_date = self.start_date_input.date().toString("yyyy-MM-dd")
            end_date = self.end_date_input.date().toString("yyyy-MM-dd")
            
            from database.db_connection import DatabaseContext
            with DatabaseContext() as db:
                query = """
                SELECT
                    t.availability_status, t.name, t.mobile, t.territory, t.email,
                    t.address, t.commission_rate, t.joining_date, t.emergency_contact,
                    (SELECT COUNT(*) FROM invoices i
                     WHERE i.technician_id = t.id AND i.is_active = TRUE
                     AND DATE(i.created_at) BETWEEN %s AND %s) as total_services,
                    (SELECT COALESCE(SUM(i.advance_payment), 0) FROM invoices i
                     WHERE i.technician_id = t.id AND i.is_active = TRUE
                     AND DATE(i.created_at) BETWEEN %s AND %s) as collected_amount,
                    (SELECT COALESCE(SUM(i.balance_amount), 0) FROM invoices i
                     WHERE i.technician_id = t.id AND i.is_active = TRUE
                     AND DATE(i.created_at) BETWEEN %s AND %s) as pending_amount
                FROM technicians t
                WHERE t.is_active = TRUE
                ORDER BY t.name
                """
                
                technicians = db.execute_query(
                    query,
                    (start_date, end_date, start_date, end_date, start_date, end_date),
                    fetch_all=True
                )
                
                for tech in (technicians or []):
                    ws.append([
                        tech.get('availability_status', 'Available'),
                        tech['name'],
                        tech['mobile'],
                        tech.get('territory') or '',
                        tech.get('email') or '',
                        tech.get('address') or '',
                        float(tech.get('commission_rate', 10)),
                        tech.get('joining_date', ''),
                        tech.get('emergency_contact') or '',
                        tech['total_services'],
                        float(tech['collected_amount']),
                        float(tech['pending_amount'])
                    ])
            
            # Save file
            default_filename = f"Technician_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Technician Report",
                default_filename,
                "Excel Files (*.xlsx)"
            )
            
            if file_path:
                wb.save(file_path)
                self.show_success_message(f"Report exported to: {file_path}")
                
        except Exception as e:
            self.show_error_message(f"Export failed: {str(e)}")


class AddTechnicianDialog(QDialog):
    """Dialog for adding new technician"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Technician")
        self.setMinimumWidth(600)
        self.setMinimumHeight(700)
        self.setStyleSheet(parent.theme_manager.get_main_stylesheet() if parent else "")
        self.photo_path = None

        self._setup_ui()

    def _setup_ui(self):
        """Setup dialog UI"""
        layout = QVBoxLayout(self)

        # Photo section
        photo_layout = QHBoxLayout()
        
        self.photo_label = QLabel()
        self.photo_label.setFixedSize(150, 150)
        colors = self.theme_manager.get_colors()
        self.photo_label.setStyleSheet(f"""
            QLabel {{
                background-color: {colors['hover']};
                border: 2px dashed {colors['border']};
                border-radius: 75px;
            }}
        """)
        self.photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.photo_label.setText("No Photo\nSelected")
        photo_layout.addWidget(self.photo_label)
        
        photo_btn_layout = QVBoxLayout()
        
        upload_photo_btn = QPushButton("📷 Upload Photo")
        upload_photo_btn.setObjectName("primaryButton")
        upload_photo_btn.clicked.connect(self._upload_photo)
        photo_btn_layout.addWidget(upload_photo_btn)
        
        remove_photo_btn = QPushButton("❌ Remove Photo")
        remove_photo_btn.setObjectName("dangerButton")
        remove_photo_btn.clicked.connect(self._remove_photo)
        photo_btn_layout.addWidget(remove_photo_btn)
        
        photo_btn_layout.addStretch()
        photo_layout.addLayout(photo_btn_layout)
        
        layout.addLayout(photo_layout)

        # Scrollable form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        form_layout = QFormLayout(scroll_content)
        form_layout.setSpacing(15)

        self.name_input = QLineEdit()
        form_layout.addRow("Name *:", self.name_input)

        self.mobile_input = QLineEdit()
        form_layout.addRow("Mobile *:", self.mobile_input)

        self.email_input = QLineEdit()
        form_layout.addRow("Email:", self.email_input)

        self.territory_input = QLineEdit()
        form_layout.addRow("Territory/Area:", self.territory_input)

        self.availability_combo = QComboBox()
        self.availability_combo.addItems(['Available', 'Busy', 'On Leave', 'Off Duty'])
        form_layout.addRow("Availability Status:", self.availability_combo)

        self.joining_date_input = QDateEdit()
        self.joining_date_input.setDate(QDate.currentDate())
        self.joining_date_input.setCalendarPopup(True)
        self.joining_date_input.setDisplayFormat("dd-MM-yyyy")
        form_layout.addRow("Joining Date:", self.joining_date_input)

        self.emergency_contact_input = QLineEdit()
        form_layout.addRow("Emergency Contact:", self.emergency_contact_input)

        self.address_input = QTextEdit()
        self.address_input.setMaximumHeight(80)
        form_layout.addRow("Address:", self.address_input)

        self.commission_input = QLineEdit("10")
        form_layout.addRow("Commission Rate (%):", self.commission_input)

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._validate_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _upload_photo(self):
        """Upload technician photo"""
        from PySide6.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Photo",
            "",
            "Images (*.png *.xpm *.jpg *.jpeg)"
        )
        if file_path:
            self.photo_path = file_path
            from PySide6.QtGui import QPixmap
            pixmap = QPixmap(file_path).scaled(
                150, 150,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.photo_label.setPixmap(pixmap)
            self.photo_label.setText("")

    def _remove_photo(self):
        """Remove technician photo"""
        self.photo_path = None
        self.photo_label.clear()
        colors = self.theme_manager.get_colors()
        self.photo_label.setStyleSheet(f"""
            QLabel {{
                background-color: {colors['hover']};
                border: 2px dashed {colors['border']};
                border-radius: 75px;
            }}
        """)
        self.photo_label.setText("No Photo\nSelected")

    def _validate_and_accept(self):
        """Validate and save technician"""
        name = self.name_input.text().strip()
        mobile = self.mobile_input.text().strip()

        if not name or not mobile:
            QMessageBox.warning(self, "Validation", "Name and Mobile are required")
            return

        # Save technician
        from database.db_connection import DatabaseContext

        with DatabaseContext() as db:
            db.execute_query(
                """
                INSERT INTO technicians (
                    name, mobile, address, email, territory, availability_status,
                    joining_date, emergency_contact, commission_rate, photo, is_active
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE)
                """,
                (
                    name, mobile,
                    self.address_input.toPlainText().strip() or None,
                    self.email_input.text().strip() or None,
                    self.territory_input.text().strip() or None,
                    self.availability_combo.currentText(),
                    self.joining_date_input.date().toString("yyyy-MM-dd"),
                    self.emergency_contact_input.text().strip() or None,
                    float(self.commission_input.text().strip() or 10),
                    self.photo_path
                )
            )

        self.accept()


class EditTechnicianDialog(QDialog):
    """Dialog for editing technician"""

    def __init__(self, technician_id, parent=None):
        super().__init__(parent)
        self.technician_id = technician_id
        self.setWindowTitle("Edit Technician")
        self.setMinimumWidth(600)
        self.setMinimumHeight(700)
        self.setStyleSheet(parent.theme_manager.get_main_stylesheet() if parent else "")
        self.photo_path = None

        self._setup_ui()
        self._load_technician()

    def _setup_ui(self):
        """Setup dialog UI"""
        layout = QVBoxLayout(self)

        # Photo section
        photo_layout = QHBoxLayout()
        
        self.photo_label = QLabel()
        self.photo_label.setFixedSize(150, 150)
        self.photo_label.setStyleSheet("""
            QLabel {
                background-color: #e2e8f0;
                border: 2px dashed #94a3b8;
                border-radius: 75px;
            }
        """)
        self.photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.photo_label.setText("Loading...")
        photo_layout.addWidget(self.photo_label)
        
        photo_btn_layout = QVBoxLayout()
        
        upload_photo_btn = QPushButton("📷 Upload Photo")
        upload_photo_btn.setObjectName("primaryButton")
        upload_photo_btn.clicked.connect(self._upload_photo)
        photo_btn_layout.addWidget(upload_photo_btn)
        
        remove_photo_btn = QPushButton("❌ Remove Photo")
        remove_photo_btn.setObjectName("dangerButton")
        remove_photo_btn.clicked.connect(self._remove_photo)
        photo_btn_layout.addWidget(remove_photo_btn)
        
        photo_btn_layout.addStretch()
        photo_layout.addLayout(photo_btn_layout)
        
        layout.addLayout(photo_layout)

        # Scrollable form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        form_layout = QFormLayout(scroll_content)
        form_layout.setSpacing(15)

        self.name_input = QLineEdit()
        form_layout.addRow("Name *:", self.name_input)

        self.mobile_input = QLineEdit()
        form_layout.addRow("Mobile *:", self.mobile_input)

        self.email_input = QLineEdit()
        form_layout.addRow("Email:", self.email_input)

        self.territory_input = QLineEdit()
        form_layout.addRow("Territory/Area:", self.territory_input)

        self.availability_combo = QComboBox()
        self.availability_combo.addItems(['Available', 'Busy', 'On Leave', 'Off Duty'])
        form_layout.addRow("Availability Status:", self.availability_combo)

        self.joining_date_input = QDateEdit()
        self.joining_date_input.setCalendarPopup(True)
        self.joining_date_input.setDisplayFormat("dd-MM-yyyy")
        form_layout.addRow("Joining Date:", self.joining_date_input)

        self.emergency_contact_input = QLineEdit()
        form_layout.addRow("Emergency Contact:", self.emergency_contact_input)

        self.address_input = QTextEdit()
        self.address_input.setMaximumHeight(80)
        form_layout.addRow("Address:", self.address_input)

        self.commission_input = QLineEdit()
        form_layout.addRow("Commission Rate (%):", self.commission_input)

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._validate_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _upload_photo(self):
        """Upload technician photo"""
        from PySide6.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Photo",
            "",
            "Images (*.png *.xpm *.jpg *.jpeg)"
        )
        if file_path:
            self.photo_path = file_path
            from PySide6.QtGui import QPixmap
            pixmap = QPixmap(file_path).scaled(
                150, 150,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.photo_label.setPixmap(pixmap)
            self.photo_label.setText("")

    def _remove_photo(self):
        """Remove technician photo"""
        self.photo_path = None
        self.photo_label.clear()
        self.photo_label.setStyleSheet("""
            QLabel {
                background-color: #e2e8f0;
                border: 2px dashed #94a3b8;
                border-radius: 75px;
            }
        """)
        self.photo_label.setText("No Photo\nSelected")

    def _load_technician(self):
        """Load technician data"""
        from database.db_connection import DatabaseContext

        with DatabaseContext() as db:
            technician = db.execute_query(
                "SELECT * FROM technicians WHERE id = %s",
                (self.technician_id,),
                fetch_one=True
            )

            if technician:
                self.name_input.setText(technician['name'])
                self.mobile_input.setText(technician['mobile'])
                self.email_input.setText(technician.get('email') or '')
                self.territory_input.setText(technician.get('territory') or '')
                self.availability_combo.setCurrentText(technician.get('availability_status', 'Available'))
                
                if technician.get('joining_date'):
                    from PySide6.QtCore import QDate
                    joining_date = QDate.fromString(
                        technician['joining_date'].strftime('%Y-%m-%d'),
                        'yyyy-MM-dd'
                    )
                    self.joining_date_input.setDate(joining_date)
                
                self.emergency_contact_input.setText(technician.get('emergency_contact') or '')
                self.address_input.setText(technician.get('address') or '')
                self.commission_input.setText(str(technician.get('commission_rate', 10)))
                
                if technician.get('photo'):
                    from PySide6.QtGui import QPixmap
                    pixmap = QPixmap(technician['photo']).scaled(
                        150, 150,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                    self.photo_label.setPixmap(pixmap)
                    self.photo_label.setText("")
                    self.photo_path = technician['photo']
                else:
                    self.photo_label.setText("No Photo")

    def _validate_and_accept(self):
        """Validate and save technician"""
        name = self.name_input.text().strip()
        mobile = self.mobile_input.text().strip()

        if not name or not mobile:
            QMessageBox.warning(self, "Validation", "Name and Mobile are required")
            return

        # Update technician
        from database.db_connection import DatabaseContext

        with DatabaseContext() as db:
            db.execute_query(
                """
                UPDATE technicians
                SET name = %s, mobile = %s, email = %s, territory = %s,
                    availability_status = %s, joining_date = %s,
                    emergency_contact = %s, address = %s,
                    commission_rate = %s, photo = %s, updated_at = NOW()
                WHERE id = %s
                """,
                (
                    name, mobile,
                    self.email_input.text().strip() or None,
                    self.territory_input.text().strip() or None,
                    self.availability_combo.currentText(),
                    self.joining_date_input.date().toString("yyyy-MM-dd"),
                    self.emergency_contact_input.text().strip() or None,
                    self.address_input.toPlainText().strip() or None,
                    float(self.commission_input.text().strip() or 10),
                    self.photo_path,
                    self.technician_id
                )
            )

        self.accept()
