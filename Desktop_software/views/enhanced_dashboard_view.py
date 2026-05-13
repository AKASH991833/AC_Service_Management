"""
Enhanced Dashboard View - PySide6 Professional Analytics Dashboard
Modern SaaS-style dashboard with clickable metrics, detailed views, search/filter
Features:
- Clickable metric cards with detailed data views
- Search and filter functionality
- Modern hover effects and animations
- Back navigation to dashboard
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton,
    QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea,
    QSizePolicy, QSpacerItem, QGraphicsDropShadowEffect, QMenu, QMessageBox,
    QDialog, QLineEdit, QGridLayout, QSplitter, QTabWidget, QTextEdit,
    QDateEdit, QDoubleSpinBox, QSpinBox, QProgressBar
)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, Signal
from PySide6.QtGui import QFont, QColor, QCursor, QPainter, QBrush, QPen
from datetime import datetime, timedelta
from decimal import Decimal

from utils.unified_theme import UnifiedTheme
from views.base_window import BaseView


class MetricCard(QFrame):
    """Clickable metric card with hover animations"""
    
    clicked = Signal(str)  # Signal with metric name
    
    def __init__(self, title, value, icon, color, parent=None):
        super().__init__(parent)
        self.title = title
        self.value = value
        self.icon = icon
        self.color = color
        self.theme_manager = UnifiedTheme()
        self.colors = self.theme_manager.get_colors()
        self._setup_ui()

    def _setup_ui(self):
        """Setup card UI - modern with gradient"""
        self.setObjectName("metricCard")
        self.setMinimumSize(200, 140)
        self.setMaximumHeight(160)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Apply initial styles
        self._apply_styles()

        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # Top row: Icon + Value
        top_layout = QHBoxLayout()
        top_layout.setSpacing(15)

        # Icon with background - properly centered
        icon_frame = QFrame()
        icon_frame.setFixedSize(50, 50)
        icon_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.color}20;
                border-radius: 25px;
                border: 2px solid {self.color};
            }}
        """)
        icon_layout = QVBoxLayout(icon_frame)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_label = QLabel(self.icon)
        icon_label.setStyleSheet(f"font-size: 20pt; color: {self.color};")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_layout.addWidget(icon_label)
        top_layout.addWidget(icon_frame)

        # Value (right side)
        self.value_label = QLabel(str(self.value))
        self.value_label.setObjectName("valueLabel")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        top_layout.addWidget(self.value_label)
        top_layout.setStretch(1, 1)

        layout.addLayout(top_layout)

        # Title (bottom)
        title_label = QLabel(self.title)
        title_label.setStyleSheet(f"""
            font-size: 10pt;
            color: {self.colors['muted']};
            font-weight: 500;
        """)
        title_label.setWordWrap(True)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Click handler
        self.clicked.connect(self._on_click)

    def _apply_styles(self):
        """Apply card styles - modern with gradient"""
        self.setStyleSheet(f"""
            QFrame#metricCard {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.colors['card_bg']},
                    stop:1 {self.colors['bg']});
                border: 1px solid {self.colors['border']};
                border-radius: 12px;
            }}
            QFrame#metricCard:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.color},
                    stop:1 {self.colors['bg']});
                border: 2px solid {self.color};
            }}
            QLabel#valueLabel {{
                font-size: 28pt;
                font-weight: bold;
                color: {self.color};
            }}
        """)

    def _on_click(self, metric_name):
        """Handle card click"""
        pass  # Debug removed

    def set_value(self, value):
        """Update card value with animation"""
        self.value = value
        self.value_label.setText(str(value))

    def enterEvent(self, event):
        """Hover enter effect - compact"""
        self.setStyleSheet(f"""
            QFrame#metricCard {{
                background-color: {self.colors['hover']};
                border: 2px solid {self.color};
                border-radius: 10px;
            }}
            QFrame#valueLabel {{
                font-size: 24pt;
                font-weight: bold;
                color: {self.color};
            }}
        """)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Hover leave effect"""
        self._apply_styles()
        super().leaveEvent(event)
        
    def mousePressEvent(self, event):
        """Handle click"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.title)
        super().mousePressEvent(event)


class DetailViewDialog(QDialog):
    """Detailed view dialog for each metric with search/filter"""
    
    def __init__(self, parent, metric_type, data, period='this_week'):
        super().__init__(parent)
        self.metric_type = metric_type
        self.data = data
        self.period = period  # Store current dashboard period
        self.theme_manager = UnifiedTheme()
        self.colors = self.theme_manager.get_colors()
        
        self.setWindowTitle(f"{metric_type} - Detailed View ({period.replace('_', ' ').title()})")
        self.setMinimumSize(1200, 700)
        self.resize(1400, 800)
        
        self._setup_ui()
        self.load_data()
        
    def _setup_ui(self):
        """Setup dialog UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header with back button and title
        self._create_header(layout)
        
        # Search and filter controls
        self._create_controls(layout)
        
        # Data table
        self._create_table(layout)
        
        # Status bar with count
        self._create_status_bar(layout)
        
    def _create_header(self, layout):
        """Create header with back navigation"""
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Back button
        back_btn = QPushButton("← Back to Dashboard")
        back_btn.setObjectName("primaryButton")
        back_btn.setFixedWidth(180)
        back_btn.clicked.connect(self.close)
        header_layout.addWidget(back_btn)
        
        # Title
        title_label = QLabel(f"📊 {self.metric_type} Details")
        title_label.setStyleSheet("""
            font-size: 18pt;
            font-weight: bold;
            color: white;
        """)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        layout.addWidget(header_frame)
        
    def _create_controls(self, layout):
        """Create search and filter controls"""
        control_frame = QFrame()
        control_layout = QHBoxLayout(control_frame)
        control_layout.setContentsMargins(0, 0, 0, 0)

        # Search
        search_label = QLabel("🔍 Search:")
        search_label.setStyleSheet("font-weight: bold; color: white;")
        control_layout.addWidget(search_label)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type to search...")
        self.search_input.setMinimumWidth(300)
        self.search_input.textChanged.connect(self.filter_data)
        # Prevent Enter key from closing dialog
        self.search_input.setClearButtonEnabled(True)
        control_layout.addWidget(self.search_input)

        control_layout.addStretch()
        
        # Export button
        export_btn = QPushButton("📤 Export")
        export_btn.setObjectName("successButton")
        export_btn.clicked.connect(self.export_data)
        control_layout.addWidget(export_btn)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setObjectName("primaryButton")
        refresh_btn.clicked.connect(self.load_data)
        control_layout.addWidget(refresh_btn)
        
        layout.addWidget(control_frame)
        
    def _create_table(self, layout):
        """Create data table"""
        self.table = QTableWidget()
        self.table.setStyleSheet("""
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
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        # Enable double-click to view details
        self.table.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked)
        self.table.cellDoubleClicked.connect(self._show_row_details)

        layout.addWidget(self.table)
        
    def _create_status_bar(self, layout):
        """Create status bar with count"""
        self.status_label = QLabel("Loading...")
        self.status_label.setStyleSheet("""
            font-size: 11pt;
            color: #94a3b8;
            padding: 10px;
            background-color: #1e293b;
            border-radius: 6px;
        """)
        layout.addWidget(self.status_label)
        
    def load_data(self):
        """Load data based on metric type"""
        try:
            if self.metric_type == "Total Customers":
                self._load_customers()
            elif self.metric_type == "Total Services":
                self._load_services()
            elif self.metric_type == "Total Revenue":
                self._load_revenue()
            elif self.metric_type == "Active AMC":
                self._load_amc()
            elif self.metric_type == "Online Requests":
                self._load_online_requests()
            elif self.metric_type == "Today's Services":
                self._load_todays_services()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load data: {str(e)}")
            
    def _load_customers(self):
        """Load customer data"""
        from database.db_connection import DatabaseContext
        
        with DatabaseContext() as db:
            query = """
                SELECT id, name, mobile, address, email, created_at
                FROM customers
                WHERE is_active = TRUE
                ORDER BY created_at DESC
            """
            customers = db.execute_query(query, fetch_all=True)
        
        # Setup table
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['ID', 'Name', 'Mobile', 'Address', 'Email', 'Created Date'])
        self.table.setRowCount(len(customers))
        
        for row, customer in enumerate(customers):
            self.table.setItem(row, 0, QTableWidgetItem(str(customer['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(customer['name'] or 'N/A'))
            self.table.setItem(row, 2, QTableWidgetItem(customer['mobile'] or 'N/A'))
            self.table.setItem(row, 3, QTableWidgetItem(customer['address'] or 'N/A'))
            self.table.setItem(row, 4, QTableWidgetItem(customer['email'] or 'N/A'))
            created_date = customer['created_at'].strftime('%d-%m-%Y') if customer['created_at'] else 'N/A'
            self.table.setItem(row, 5, QTableWidgetItem(created_date))
            
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        
        self.all_data = customers
        self.status_label.setText(f"Total Customers: {len(customers)}")
        
    def _load_services(self):
        """Load service/invoice data"""
        from database.db_connection import DatabaseContext
        
        with DatabaseContext() as db:
            query = """
                SELECT i.id, i.invoice_number, c.name as customer_name,
                       s.service_name, i.total_amount, i.created_at
                FROM invoices i
                JOIN customers c ON i.customer_id = c.id
                JOIN invoice_items ii ON i.id = ii.invoice_id
                JOIN services s ON ii.service_id = s.id
                WHERE i.is_active = TRUE
                ORDER BY i.created_at DESC
                LIMIT 100
            """
            services = db.execute_query(query, fetch_all=True)

        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['ID', 'Invoice No', 'Customer', 'Service', 'Amount', 'Date'])
        self.table.setRowCount(len(services))

        for row, service in enumerate(services):
            self.table.setItem(row, 0, QTableWidgetItem(str(service['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(service['invoice_number'] or 'N/A'))
            self.table.setItem(row, 2, QTableWidgetItem(service['customer_name'] or 'N/A'))
            self.table.setItem(row, 3, QTableWidgetItem(service['service_name'] or 'N/A'))
            self.table.setItem(row, 4, QTableWidgetItem(f"₹{service['total_amount']:,.2f}"))
            date_str = service['created_at'].strftime('%d-%m-%Y %H:%M') if service['created_at'] else 'N/A'
            self.table.setItem(row, 5, QTableWidgetItem(date_str))

        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

        self.all_data = services
        self.status_label.setText(f"Total Services: {len(services)} ({self.period.replace('_', ' ').title()})")
        
    def _get_date_range(self):
        """Calculate date range based on period"""
        today = datetime.now().date()
        
        if self.period == 'today':
            return today, today
        elif self.period == 'this_week':
            start = today - timedelta(days=today.weekday())  # Monday
            return start, today
        elif self.period == 'this_month':
            start = today.replace(day=1)
            return start, today
        else:  # this_year
            start = today.replace(month=1, day=1)
            return start, today
        
    def _load_services(self):
        """Load service/invoice data filtered by period"""
        from database.db_connection import DatabaseContext
        
        start_date, end_date = self._get_date_range()
        
        with DatabaseContext() as db:
            query = """
                SELECT i.id, i.invoice_number, c.name as customer_name,
                       s.service_name, i.total_amount, i.created_at
                FROM invoices i
                JOIN customers c ON i.customer_id = c.id
                JOIN invoice_items ii ON i.id = ii.invoice_id
                JOIN services s ON ii.service_id = s.id
                WHERE i.is_active = TRUE AND DATE(i.created_at) BETWEEN %s AND %s
                ORDER BY i.created_at DESC
                LIMIT 100
            """
            services = db.execute_query(query, (start_date, end_date), fetch_all=True)

        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['ID', 'Invoice No', 'Customer', 'Service', 'Amount', 'Date'])
        self.table.setRowCount(len(services))

        for row, service in enumerate(services):
            self.table.setItem(row, 0, QTableWidgetItem(str(service['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(service['invoice_number'] or 'N/A'))
            self.table.setItem(row, 2, QTableWidgetItem(service['customer_name'] or 'N/A'))
            self.table.setItem(row, 3, QTableWidgetItem(service['service_name'] or 'N/A'))
            self.table.setItem(row, 4, QTableWidgetItem(f"₹{service['total_amount']:,.2f}"))
            date_str = service['created_at'].strftime('%d-%m-%Y %H:%M') if service['created_at'] else 'N/A'
            self.table.setItem(row, 5, QTableWidgetItem(date_str))

        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

        self.all_data = services
        self.status_label.setText(f"Total Services: {len(services)} ({self.period.replace('_', ' ').title()})")
        
    def _load_revenue(self):
        """Load revenue/invoice data filtered by period"""
        from database.db_connection import DatabaseContext
        
        start_date, end_date = self._get_date_range()
        
        with DatabaseContext() as db:
            query = """
                SELECT i.invoice_number, c.name as customer_name,
                       i.total_amount, i.advance_payment, i.balance_amount,
                       i.created_at, i.payment_status
                FROM invoices i
                JOIN customers c ON i.customer_id = c.id
                WHERE i.is_active = TRUE AND DATE(i.created_at) BETWEEN %s AND %s
                ORDER BY i.created_at DESC
                LIMIT 100
            """
            revenues = db.execute_query(query, (start_date, end_date), fetch_all=True)

        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['Invoice No', 'Customer', 'Total Amount', 'Paid', 'Balance', 'Status', 'Date'])
        self.table.setRowCount(len(revenues))

        for row, rev in enumerate(revenues):
            self.table.setItem(row, 0, QTableWidgetItem(rev['invoice_number'] or 'N/A'))
            self.table.setItem(row, 1, QTableWidgetItem(rev['customer_name'] or 'N/A'))
            self.table.setItem(row, 2, QTableWidgetItem(f"₹{rev['total_amount']:,.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"₹{rev['advance_payment']:,.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(f"₹{rev['balance_amount']:,.2f}"))
            status = rev['payment_status'] or 'Pending'
            self.table.setItem(row, 5, QTableWidgetItem(status))
            date_str = rev['created_at'].strftime('%d-%m-%Y') if rev['created_at'] else 'N/A'
            self.table.setItem(row, 6, QTableWidgetItem(date_str))

        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        self.all_data = revenues
        total_revenue = sum(r['total_amount'] for r in revenues)
        self.status_label.setText(f"Total Revenue: ₹{total_revenue:,.2f} | Records: {len(revenues)} ({self.period.replace('_', ' ').title()})")

    def _load_amc(self):
        """Load AMC contract data"""
        from database.db_connection import DatabaseContext
        
        with DatabaseContext() as db:
            query = """
                SELECT ac.amc_id, c.name as customer_name, ac.contract_type,
                       ac.amc_status, ac.total_amount as amc_amount, ac.start_date, ac.end_date,
                       ac.services_per_year as total_visits, ac.services_per_year as visits_completed
                FROM amc_contracts ac
                JOIN customers c ON ac.customer_id = c.id
                WHERE ac.is_active = TRUE
                ORDER BY ac.created_at DESC
            """
            amc_data = db.execute_query(query, fetch_all=True)

        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(['AMC ID', 'Customer', 'Type', 'Status', 'Amount', 'Start Date', 'End Date', 'Visits', 'Progress'])
        self.table.setRowCount(len(amc_data) if amc_data else 0)

        for row, amc in enumerate(amc_data or []):
            self.table.setItem(row, 0, QTableWidgetItem(amc['amc_id'] or 'N/A'))
            self.table.setItem(row, 1, QTableWidgetItem(amc['customer_name'] or 'N/A'))
            self.table.setItem(row, 2, QTableWidgetItem(amc['contract_type'] or 'N/A'))
            status = amc['amc_status'] or 'Active'
            self.table.setItem(row, 3, QTableWidgetItem(status))
            self.table.setItem(row, 4, QTableWidgetItem(f"₹{amc['amc_amount']:,.2f}"))
            start_date = amc['start_date'].strftime('%d-%m-%Y') if amc['start_date'] else 'N/A'
            end_date = amc['end_date'].strftime('%d-%m-%Y') if amc['end_date'] else 'N/A'
            self.table.setItem(row, 5, QTableWidgetItem(start_date))
            self.table.setItem(row, 6, QTableWidgetItem(end_date))
            visits = f"{amc['visits_completed'] or 0}/{amc['total_visits'] or 0}"
            self.table.setItem(row, 7, QTableWidgetItem(visits))
            progress = f"{int((amc['visits_completed'] or 0) / max(amc['total_visits'] or 1, 1) * 100)}%"
            self.table.setItem(row, 8, QTableWidgetItem(progress))

        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        self.all_data = amc_data
        active_count = len([a for a in amc_data if a['amc_status'] == 'Active'])
        self.status_label.setText(f"Active AMC Contracts: {active_count} | Total: {len(amc_data)}")

    def _load_online_requests(self):
        """Load online requests from website filtered by period"""
        from database.db_connection import DatabaseContext
        
        start_date, end_date = self._get_date_range()

        # Combine contact messages and service requests
        with DatabaseContext() as db:
            query = """
                SELECT 'Contact' as type, id, name, phone as mobile,
                       service_type, created_at, status
                FROM contact_messages
                WHERE DATE(created_at) BETWEEN %s AND %s
                UNION ALL
                SELECT 'Service' as type, id, customer_name as name, customer_phone as mobile,
                       service_type, created_at, request_status as status
                FROM service_requests
                WHERE DATE(created_at) BETWEEN %s AND %s
                ORDER BY created_at DESC
                LIMIT 100
            """
            requests = db.execute_query(query, (start_date, end_date, start_date, end_date), fetch_all=True)

        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['Type', 'ID', 'Name', 'Mobile', 'Service Type', 'Status', 'Date'])
        self.table.setRowCount(len(requests))

        for row, req in enumerate(requests):
            self.table.setItem(row, 0, QTableWidgetItem(req['type']))
            self.table.setItem(row, 1, QTableWidgetItem(str(req['id'])))
            self.table.setItem(row, 2, QTableWidgetItem(req['name'] or 'N/A'))
            self.table.setItem(row, 3, QTableWidgetItem(req['mobile'] or 'N/A'))
            self.table.setItem(row, 4, QTableWidgetItem(req['service_type'] or 'N/A'))
            self.table.setItem(row, 5, QTableWidgetItem(req['status'] or 'Pending'))
            date_str = req['created_at'].strftime('%d-%m-%Y %H:%M') if req['created_at'] else 'N/A'
            self.table.setItem(row, 6, QTableWidgetItem(date_str))
            
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        
        self.all_data = requests
        unread = len([r for r in requests if r['status'] == 'unread' or r['status'] == 'pending'])
        self.status_label.setText(f"Total Requests: {len(requests)} | Unread/Pending: {unread}")
        
    def _load_todays_services(self):
        """Load services filtered by period"""
        from database.db_connection import DatabaseContext
        
        start_date, end_date = self._get_date_range()
        
        with DatabaseContext() as db:
            query = """
                SELECT i.id, i.invoice_number, c.name as customer_name,
                       s.service_name, i.total_amount, i.created_at,
                       t.name as technician_name
                FROM invoices i
                JOIN customers c ON i.customer_id = c.id
                JOIN invoice_items ii ON i.id = ii.invoice_id
                JOIN services s ON ii.service_id = s.id
                LEFT JOIN technicians t ON i.technician_id = t.id
                WHERE i.is_active = TRUE AND DATE(i.created_at) BETWEEN %s AND %s
                ORDER BY i.created_at DESC
            """
            services = db.execute_query(query, (start_date, end_date), fetch_all=True)

        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['ID', 'Invoice No', 'Customer', 'Service', 'Technician', 'Amount', 'Time'])
        self.table.setRowCount(len(services))

        for row, service in enumerate(services):
            self.table.setItem(row, 0, QTableWidgetItem(str(service['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(service['invoice_number'] or 'N/A'))
            self.table.setItem(row, 2, QTableWidgetItem(service['customer_name'] or 'N/A'))
            self.table.setItem(row, 3, QTableWidgetItem(service['service_name'] or 'N/A'))
            self.table.setItem(row, 4, QTableWidgetItem(service['technician_name'] or 'Unassigned'))
            self.table.setItem(row, 5, QTableWidgetItem(f"₹{service['total_amount']:,.2f}"))
            time_str = service['created_at'].strftime('%H:%M') if service['created_at'] else 'N/A'
            self.table.setItem(row, 6, QTableWidgetItem(time_str))

        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

        self.all_data = services
        total_amount = sum(s['total_amount'] for s in services)
        period_label = self.period.replace('_', ' ').title()
        self.status_label.setText(f"Services ({period_label}): {len(services)} | Revenue: ₹{total_amount:,.2f}")

    def filter_data(self, search_text):
        """Filter table data based on search text"""
        if not hasattr(self, 'all_data'):
            return

        search_text = search_text.lower()

        # Hide rows that don't match search
        for row in range(self.table.rowCount()):
            match = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and search_text in item.text().lower():
                    match = True
                    break
            self.table.setRowHidden(row, not match)

    def _show_row_details(self, row, column):
        """Show detailed view of selected row"""
        if self.metric_type == "Total Customers":
            self._show_customer_details(row)
        elif self.metric_type == "Total Services":
            self._show_service_details(row)
        elif self.metric_type == "Total Revenue":
            self._show_revenue_details(row)
        elif self.metric_type == "Active AMC":
            self._show_amc_details(row)
        elif self.metric_type == "Online Requests":
            self._show_request_details(row)
        elif self.metric_type == "Today's Services":
            self._show_service_details(row)

    def _show_customer_details(self, row):
        """Show customer details popup"""
        from database.db_connection import DatabaseContext
        
        # Get customer ID from table
        id_item = self.table.item(row, 0)
        if not id_item:
            return
            
        try:
            customer_id = int(id_item.text())
        except:
            QMessageBox.warning(self, "Error", "Could not get customer ID")
            return
        
        with DatabaseContext() as db:
            # Get customer details
            query = """
                SELECT id, name, mobile, email, address, landmark, created_at
                FROM customers
                WHERE id = %s AND is_active = TRUE
            """
            customer = db.execute_query(query, (customer_id,), fetch_one=True)
            
            if not customer:
                QMessageBox.warning(self, "Error", "Customer not found")
                return
            
            # Get customer's invoice count
            invoice_query = """
                SELECT COUNT(*) as count, COALESCE(SUM(total_amount), 0) as total
                FROM invoices
                WHERE customer_id = %s AND is_active = TRUE
            """
            invoice_stats = db.execute_query(invoice_query, (customer_id,), fetch_one=True)
            
            # Show details in message box
            details_text = f"""
<b>👤 CUSTOMER DETAILS</b>

<b>📋 ID:</b> {customer['id']}
<b>👤 Name:</b> {customer['name']}
<b>📱 Mobile:</b> {customer['mobile']}
<b>📧 Email:</b> {customer['email'] or 'N/A'}
<b>📍 Address:</b> {customer['address'] or 'N/A'}
<b>🏷️ Landmark:</b> {customer['landmark'] or 'N/A'}
<b>📅 Created:</b> {customer['created_at'].strftime('%d-%m-%Y') if customer['created_at'] else 'N/A'}

<b>📊 SERVICE HISTORY</b>
<b>📝 Total Invoices:</b> {invoice_stats['count'] or 0}
<b>💰 Total Revenue:</b> ₹{invoice_stats['total']:,.0f}
            """
            
            QMessageBox.information(self, f"Customer Details - {customer['name']}", details_text)

    def _show_service_details(self, row):
        """Show service/invoice details popup"""
        # Get invoice ID from table
        id_item = self.table.item(row, 0)
        if not id_item:
            return
            
        try:
            invoice_id = int(id_item.text())
        except:
            QMessageBox.warning(self, "Error", "Could not get invoice ID")
            return
        
        from database.db_connection import DatabaseContext
        with DatabaseContext() as db:
            query = """
                SELECT i.invoice_number, c.name, i.total_amount, i.created_at, s.service_name
                FROM invoices i
                JOIN customers c ON i.customer_id = c.id
                JOIN invoice_items ii ON i.id = ii.invoice_id
                JOIN services s ON ii.service_id = s.id
                WHERE i.id = %s
            """
            invoice = db.execute_query(query, (invoice_id,), fetch_one=True)
            
            if invoice:
                details_text = f"""
<b>🔧 SERVICE DETAILS</b>

<b>📝 Invoice:</b> {invoice['invoice_number']}
<b>👤 Customer:</b> {invoice['name']}
<b>🔧 Service:</b> {invoice['service_name']}
<b>💰 Amount:</b> ₹{invoice['total_amount']:,.0f}
<b>📅 Date:</b> {invoice['created_at'].strftime('%d-%m-%Y %H:%M') if invoice['created_at'] else 'N/A'}
                """
                QMessageBox.information(self, "Service Details", details_text)

    def _show_revenue_details(self, row):
        """Show revenue/invoice details popup"""
        invoice_no_item = self.table.item(row, 0)
        if not invoice_no_item:
            return
        
        invoice_number = invoice_no_item.text()
        
        from database.db_connection import DatabaseContext
        with DatabaseContext() as db:
            query = """
                SELECT i.invoice_number, c.name, i.total_amount, i.advance_payment, 
                       i.balance_amount, i.payment_status, i.created_at
                FROM invoices i
                JOIN customers c ON i.customer_id = c.id
                WHERE i.invoice_number = %s
            """
            invoice = db.execute_query(query, (invoice_number,), fetch_one=True)
            
            if invoice:
                details_text = f"""
<b>💰 INVOICE DETAILS</b>

<b>📝 Invoice No:</b> {invoice['invoice_number']}
<b>👤 Customer:</b> {invoice['name']}
<b>💵 Total Amount:</b> ₹{invoice['total_amount']:,.0f}
<b>💰 Paid:</b> ₹{invoice['advance_payment']:,.0f}
<b>⏳ Balance:</b> ₹{invoice['balance_amount']:,.0f}
<b>📊 Status:</b> {invoice['payment_status']}
<b>📅 Date:</b> {invoice['created_at'].strftime('%d-%m-%Y') if invoice['created_at'] else 'N/A'}
                """
                QMessageBox.information(self, "Invoice Details", details_text)

    def _show_amc_details(self, row):
        """Show AMC contract details popup"""
        amc_id_item = self.table.item(row, 0)
        if not amc_id_item:
            return
        
        amc_id = amc_id_item.text()

        from database.db_connection import DatabaseContext
        with DatabaseContext() as db:
            query = """
                SELECT ac.amc_id, c.name, ac.contract_type, ac.amc_status,
                       ac.total_amount as amc_amount, ac.start_date, ac.end_date,
                       ac.services_per_year as total_visits, ac.services_per_year as visits_completed
                FROM amc_contracts ac
                JOIN customers c ON ac.customer_id = c.id
                WHERE ac.amc_id = %s
            """
            amc = db.execute_query(query, (amc_id,), fetch_one=True)

            if amc:
                progress = int((amc['visits_completed'] or 0) / max(amc['total_visits'] or 1, 1) * 100)
                details_text = f"""
<b>📋 AMC CONTRACT DETAILS</b>

<b>🔖 AMC ID:</b> {amc['amc_id']}
<b>👤 Customer:</b> {amc['name']}
<b>📊 Type:</b> {amc['contract_type']}
<b>✅ Status:</b> {amc['amc_status']}
<b>💰 Amount:</b> ₹{amc['amc_amount']:,.0f}
<b>📅 Start Date:</b> {amc['start_date'].strftime('%d-%m-%Y') if amc['start_date'] else 'N/A'}
<b>📅 End Date:</b> {amc['end_date'].strftime('%d-%m-%Y') if amc['end_date'] else 'N/A'}
<b>🔧 Visits:</b> {amc['visits_completed'] or 0}/{amc['total_visits'] or 0} ({progress}%)
                """
                QMessageBox.information(self, "AMC Details", details_text)

    def _show_request_details(self, row):
        """Show online request details popup"""
        id_item = self.table.item(row, 1)
        req_type_item = self.table.item(row, 0)
        if not id_item or not req_type_item:
            return
        
        try:
            req_id = int(id_item.text())
            req_type = req_type_item.text()
        except:
            QMessageBox.warning(self, "Error", "Could not get request details")
            return

        from database.db_connection import DatabaseContext
        with DatabaseContext() as db:
            if req_type == "Contact":
                query = """
                    SELECT name, phone, email, service_type, message, created_at, status
                    FROM contact_messages
                    WHERE id = %s
                """
            else:
                query = """
                    SELECT customer_name as name, customer_phone as phone, customer_email as email, 
                           service_type, message, created_at, request_status as status
                    FROM service_requests
                    WHERE id = %s
                """

            request = db.execute_query(query, (req_id,), fetch_one=True)

            if request:
                details_text = f"""
<b>🌐 {req_type.upper()} REQUEST DETAILS</b>

<b>👤 Name:</b> {request['name']}
<b>📱 Phone:</b> {request['phone']}
<b>📧 Email:</b> {request['email'] or 'N/A'}
<b>🔧 Service Type:</b> {request['service_type']}
<b>📝 Message:</b> {request['message'] or 'N/A'}
<b>📅 Date:</b> {request['created_at'].strftime('%d-%m-%Y %H:%M') if request['created_at'] else 'N/A'}
<b>📊 Status:</b> {request['status']}
                """
                QMessageBox.information(self, "Request Details", details_text)

    def keyPressEvent(self, event):
        """Override key press to prevent Enter from closing dialog"""
        from PySide6.QtCore import Qt
        # Ignore Enter/Return keys that might close the dialog
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            # Just ignore - don't close the dialog
            return
        # Let other keys pass through
        super().keyPressEvent(event)

    def export_data(self):
        """Export data to CSV"""
        from PySide6.QtWidgets import QFileDialog
        import csv
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Data", "", "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    
                    # Write headers
                    headers = [self.table.horizontalHeaderItem(i).text() 
                              for i in range(self.table.columnCount())]
                    writer.writerow(headers)
                    
                    # Write data
                    for row in range(self.table.rowCount()):
                        if not self.table.isRowHidden(row):
                            row_data = []
                            for col in range(self.table.columnCount()):
                                item = self.table.item(row, col)
                                row_data.append(item.text() if item else '')
                            writer.writerow(row_data)
                            
                QMessageBox.information(self, "Success", f"Data exported to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export: {str(e)}")


class EnhancedDashboardView(BaseView):
    """Enhanced professional dashboard with clickable cards and detailed views"""

    def __init__(self, user_data, db, controller):
        super().__init__()
        self.user_data = user_data
        self.db = db
        self.controller = controller
        self.theme_manager = UnifiedTheme()
        self.period = 'this_week'  # Default: This Week
        self.metric_labels = {}
        self.metric_cards = {}
        self.loaded_data = {}
        self.last_online_count = 0
        self.last_pending_count = 0
        self.last_invoice_count = 0
        self.last_revenue_count = 0

        self._setup_ui()
        self.load_dashboard_data()
        QTimer.singleShot(500, self.load_analytics_data)
        
        # Auto-refresh timer for real-time updates
        self.auto_refresh_timer = QTimer()
        self.auto_refresh_timer.timeout.connect(self._auto_refresh_check)
        self.auto_refresh_timer.start(15000)  # Refresh every 15 seconds

    def cleanup(self):
        """Cleanup timers when view is closed"""
        try:
            if hasattr(self, 'auto_refresh_timer'):
                self.auto_refresh_timer.stop()
        except Exception as e:
            print(f"[WARN] Dashboard cleanup failed: {e}")

    def update_theme_colors(self):
        """Update theme colors for proper dark theme support"""
        colors = self.theme_manager.get_colors()

        # Apply QPalette colors
        self.theme_manager.apply_palette(self)

        # Apply stylesheet
        self.setStyleSheet(self.theme_manager.get_main_stylesheet())

        # Apply theme directly to all tables for proper alternating colors
        if hasattr(self, 'table'):
            self.theme_manager.apply_table_theme(self.table)

        if hasattr(self, 'top_services_table'):
            self.theme_manager.apply_table_theme(self.top_services_table)

        if hasattr(self, 'comparison_table'):
            self.theme_manager.apply_table_theme(self.comparison_table)

        if hasattr(self, 'alerts_table'):
            self.theme_manager.apply_table_theme(self.alerts_table)

        if hasattr(self, 'pending_table'):
            self.theme_manager.apply_table_theme(self.pending_table)

        # Refresh data to ensure proper display
        self.load_dashboard_data()

    def refresh_data(self):
        """Refresh dashboard data and user data from session"""
        print(f"[DEBUG] Dashboard refresh_data() called")
        
        # CRITICAL: Refresh user_data from session to get latest profile updates
        from utils.session_manager import get_session
        session = get_session()
        if session and session.get_current_user():
            self.user_data = session.get_current_user().copy()
            print(f"[DASHBOARD] Refreshed user_data from session: {self.user_data}")
            
            # Update greeting label if it exists
            for widget in self.findChildren(QLabel):
                if widget.text().startswith("Good") and "!" in widget.text():
                    current_hour = datetime.now().hour
                    if 5 <= current_hour < 12:
                        greeting = "Good morning"
                    elif 12 <= current_hour < 18:
                        greeting = "Good afternoon"
                    else:
                        greeting = "Good evening"
                    user_name = self.user_data.get('full_name', 'Admin').split()[0]
                    widget.setText(f"{greeting}, {user_name}! 👋")
                    break
        
        self.load_dashboard_data()
        self.load_analytics_data()

    def _auto_refresh_check(self):
        """Auto-refresh check for new online requests AND periodic dashboard refresh"""
        try:
            stats = self.controller.get_dashboard_stats(self.period)
            if stats:
                current_online = stats.get('online_requests', 0)
                current_invoices = stats.get('total_invoices', 0)
                current_revenue = stats.get('total_revenue', 0)
                
                # Check for new online requests
                if current_online > self.last_online_count and self.last_online_count > 0:
                    new_count = current_online - self.last_online_count
                    self.show_new_request_notification(new_count)
                
                # Check for new invoices/revenue changes
                if (current_invoices != self.last_invoice_count or 
                    current_revenue != self.last_revenue_count):
                    print(f"[AUTO-REFRESH] Data changed - refreshing dashboard")
                    self.refresh_data()
                    return  # Don't update counters again, refresh_data will handle it
                
                # Update last counts
                self.last_online_count = current_online
                self.last_invoice_count = current_invoices
                self.last_revenue_count = current_revenue
                
        except Exception as e:
            print(f"[ERROR] Dashboard auto-refresh check failed: {e}")

    def show_new_request_notification(self, count):
        """Show notification for new requests"""
        try:
            # Play notification sound
            import winsound
            winsound.PlaySound("SystemNotification", winsound.SND_ALIAS | winsound.SND_ASYNC)
        except Exception as e:
            print(f"[INFO] Sound play failed: {e}")
        
        # Update greeting label to show notification
        for widget in self.findChildren(QLabel):
            if widget.text().startswith("Good") and "!" in widget.text():
                current_text = widget.text()
                widget.setText(f"{current_text} 🔔 {count} new request{'s' if count > 1 else ''}!")
                # Reset after 5 seconds
                QTimer.singleShot(5000, lambda: widget.setText(widget.text().split(' 🔔')[0] + "!"))
                break

    def _setup_ui(self):
        """Setup enhanced dashboard UI - No scroll, compact layout"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(12)

        # Header section
        self._create_header(main_layout)

        # Filter section
        self._create_filter(main_layout)

        # Metric cards with click handlers
        self._create_metric_cards(main_layout)

        # Advanced Analytics Section (compact, no scroll needed)
        self._create_analytics_section(main_layout)

        # Main content removed - duplicate data already in analytics tabs
        self._create_main_content(main_layout)

    def _create_header(self, layout):
        """Create dashboard header - compact"""
        # Time-based greeting
        current_hour = datetime.now().hour
        if 5 <= current_hour < 12:
            greeting = "Good morning"
        elif 12 <= current_hour < 18:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"

        user_name = self.user_data.get('full_name', 'Admin').split()[0]

        # Modern greeting
        greeting_label = QLabel(f"{greeting}, {user_name}! 👋")
        greeting_label.setStyleSheet("""
            font-size: 24pt;
            font-weight: bold;
            color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #3498db,
                stop:1 #2ecc71);
        """)
        layout.addWidget(greeting_label)

        # Date label
        date_str = datetime.now().strftime('%A, %B %d, %Y')
        date_label = QLabel(date_str)
        date_label.setStyleSheet("""
            font-size: 10pt;
            color: #95a5a6;
            font-weight: 500;
        """)
        layout.addWidget(date_label)

    def _create_filter(self, layout):
        """Create period filter - modern UI"""
        colors = self.theme_manager.get_colors()
        
        filter_frame = QFrame()
        filter_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {colors['card_bg']};
                border: 1px solid {colors['border']};
                border-radius: 10px;
            }}
        """)
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(15, 10, 15, 10)

        # Filter label
        filter_label = QLabel("📅 Select Period:")
        filter_label.setStyleSheet(f"font-size: 10pt; font-weight: bold; color: {colors['fg']};")
        filter_layout.addWidget(filter_label)

        # Modern period combo
        self.period_combo = QComboBox()
        self.period_combo.addItems(['Today', 'This Week', 'This Month', 'This Year'])
        self.period_combo.setCurrentIndex(1)  # Default: This Week
        self.period_combo.setMinimumWidth(140)
        self.period_combo.setMaximumWidth(160)
        self.period_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {colors['hover']};
                color: {colors['fg']};
                border: 2px solid {colors['primary']};
                border-radius: 6px;
                padding: 8px 12px;
                font-weight: 600;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {colors['card_bg']};
                color: {colors['fg']};
                border: 2px solid {colors['primary']};
                selection-background-color: {colors['primary']};
            }}
        """)
        self.period_combo.currentTextChanged.connect(self._on_period_change)
        filter_layout.addWidget(self.period_combo)

        # Date range label
        self.date_range_label = QLabel("")
        self.date_range_label.setStyleSheet(f"color: {colors['primary']}; font-size: 9pt; font-weight: bold;")
        filter_layout.addWidget(self.date_range_label)

        filter_layout.addStretch()

        layout.addWidget(filter_frame)

    def _create_metric_cards(self, layout):
        """Create clickable metric cards row"""
        cards_frame = QFrame()
        cards_frame.setStyleSheet("""
            background-color: transparent;
        """)
        cards_layout = QHBoxLayout(cards_frame)
        cards_layout.setContentsMargins(0, 0, 0, 0)
        cards_layout.setSpacing(20)

        # Metric definitions with colors
        metrics = [
            ('total_customers', 'Total Customers', '👥', '#3B82F6'),
            ('total_services', 'Total Services', '🔧', '#10B981'),
            ('total_revenue', 'Total Revenue', '💰', '#8B5CF6'),
            ('amc_contracts', 'Active AMC', '📋', '#06b6d4'),
            ('online_requests', 'Online Requests', '🌐', '#F59E0B'),
            ('today_services', "Today's Services", '📅', '#F59E0B')
        ]

        for key, label, icon, color in metrics:
            card = MetricCard(label, "0", icon, color)
            card.clicked.connect(self._on_card_clicked)
            cards_layout.addWidget(card)
            self.metric_cards[key] = card

        layout.addWidget(cards_frame)

    def _create_analytics_section(self, layout):
        """Create advanced analytics section - modern UI"""
        colors = self.theme_manager.get_colors()
        
        analytics_frame = QFrame()
        analytics_frame.setStyleSheet(f"""
            QFrame#analyticsMainFrame {{
                background-color: {colors['card_bg']};
                border: 2px solid {colors['primary']};
                border-radius: 15px;
            }}
        """)
        analytics_frame.setObjectName("analyticsMainFrame")

        analytics_layout = QVBoxLayout(analytics_frame)
        analytics_layout.setContentsMargins(20, 20, 20, 20)
        analytics_layout.setSpacing(15)

        # Modern header
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame#headerFrame {{
                background-color: {colors['hover']};
                border: 2px solid {colors['border']};
                border-radius: 12px;
            }}
        """)
        header_frame.setObjectName("headerFrame")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 15, 20, 15)

        # Title with icon
        title_label = QLabel("📊 Advanced Analytics Dashboard")
        title_label.setStyleSheet(f"""
            font-size: 18pt;
            font-weight: bold;
            color: {colors['fg']};
            background: transparent;
        """)
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        # Subtitle
        subtitle_label = QLabel("Real-time business insights")
        subtitle_label.setStyleSheet(f"""
            font-size: 10pt;
            color: {colors['muted']};
            font-style: italic;
            background: transparent;
        """)
        header_layout.addWidget(subtitle_label)

        analytics_layout.addWidget(header_frame)

        # Modern tabs
        self.analytics_tabs = QTabWidget()
        self.analytics_tabs.setStyleSheet("""
            QTabWidget::pane {
                background-color: #2c3e50;
                border: 2px solid #34495e;
                border-radius: 12px;
            }
            QTabBar::tab {
                background-color: #34495e;
                color: #bdc3c7;
                padding: 12px 25px;
                border: 1px solid transparent;
                border-bottom: 3px solid transparent;
                font-weight: 600;
                font-size: 10pt;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                margin-right: 3px;
                min-width: 130px;
            }
            QTabBar::tab:selected {
                background-color: #2c3e50;
                color: #3498db;
                border-bottom: 3px solid #3498db;
                border-top: 1px solid #3498db;
                border-left: 1px solid #3498db;
                border-right: 1px solid #3498db;
            }
            QTabBar::tab:hover:!selected {
                background-color: #3d566e;
                color: #3498db;
                border-bottom: 3px solid #3498db;
            }
        """)

        # Tabs
        revenue_tab = self._create_revenue_trend_tab()
        self.analytics_tabs.addTab(revenue_tab, "📈 Revenue Trend")

        services_tab = self._create_top_services_tab()
        self.analytics_tabs.addTab(services_tab, "🔧 Top Services")

        comparison_tab = self._create_monthly_comparison_tab()
        self.analytics_tabs.addTab(comparison_tab, "📅 Monthly Comparison")

        alerts_tab = self._create_payment_alerts_tab()
        self.analytics_tabs.addTab(alerts_tab, "⚠️ Payment Alerts")

        analytics_layout.addWidget(self.analytics_tabs)
        layout.addWidget(analytics_frame)

    def _create_revenue_trend_tab(self):
        """Create revenue trend chart tab - compact"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        # Compact header
        header = QLabel("📈 Revenue Trend - Last 30 Days")
        header.setStyleSheet("font-size: 12pt; font-weight: bold; color: white;")
        layout.addWidget(header)

        # Revenue chart frame
        self.revenue_chart_frame = QFrame()
        self.revenue_chart_frame.setStyleSheet("background-color: #1e293b; border-radius: 6px;")
        chart_layout = QVBoxLayout(self.revenue_chart_frame)
        chart_layout.setContentsMargins(10, 10, 10, 10)

        # Revenue data label
        self.revenue_chart_label = QLabel("Loading revenue data...")
        self.revenue_chart_label.setStyleSheet("color: #94a3b8; font-size: 9pt;")
        self.revenue_chart_label.setWordWrap(True)
        chart_layout.addWidget(self.revenue_chart_label)

        layout.addWidget(self.revenue_chart_frame)

        # Revenue stats
        self.revenue_stats_label = QLabel()
        self.revenue_stats_label.setStyleSheet("color: #22d3ee; font-size: 9pt; font-weight: bold;")
        layout.addWidget(self.revenue_stats_label)

        return tab

    def _create_top_services_tab(self):
        """Create top services table tab - compact"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        # Compact header
        header = QLabel("🔧 Top Services by Revenue - This Month")
        header.setStyleSheet("font-size: 12pt; font-weight: bold; color: white;")
        layout.addWidget(header)

        # Compact table
        self.top_services_table = QTableWidget()
        self.top_services_table.setColumnCount(4)
        self.top_services_table.setHorizontalHeaderLabels(['Service Name', 'Price', 'Times Sold', 'Total Revenue'])
        self.top_services_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.top_services_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.top_services_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.top_services_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.top_services_table.setAlternatingRowColors(True)
        self.top_services_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.top_services_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.top_services_table.verticalHeader().setVisible(False)
        self.top_services_table.setMinimumHeight(200)
        self.top_services_table.setMaximumHeight(300)
        self.top_services_table.setStyleSheet("""
            QTableWidget {
                background-color: #1e293b;
                color: white;
                border: 1px solid #334155;
                border-radius: 6px;
                gridline-color: #334155;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #22d3ee;
            }
            QHeaderView::section {
                background-color: #334155;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
                font-size: 9pt;
            }
        """)
        layout.addWidget(self.top_services_table)
        return tab

    def _create_retention_tab(self):
        """Create customer retention tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)

        # Header
        header = QLabel("Customer Retention Analysis")
        header.setStyleSheet("font-size: 14pt; font-weight: bold; color: white;")
        layout.addWidget(header)

        # Retention metrics
        metrics_frame = QFrame()
        metrics_frame.setStyleSheet("background-color: #334155; border-radius: 8px;")
        metrics_layout = QHBoxLayout(metrics_frame)
        metrics_layout.setContentsMargins(20, 20, 20, 20)
        metrics_layout.setSpacing(30)

        # Retention Rate Card
        retention_card = self._create_metric_mini_card("Retention Rate", "0%", "👥", "#22d3ee")
        self.retention_rate_label = retention_card.findChild(QLabel)
        metrics_layout.addWidget(retention_card)

        # Previous Customers Card
        prev_card = self._create_metric_mini_card("Previous Customers", "0", "📊", "#3B82F6")
        self.prev_customers_label = prev_card.findChild(QLabel)
        metrics_layout.addWidget(prev_card)

        # Current Customers Card
        curr_card = self._create_metric_mini_card("Current Customers", "0", "📈", "#10B981")
        self.curr_customers_label = curr_card.findChild(QLabel)
        metrics_layout.addWidget(curr_card)

        # Repeat Customers Card
        repeat_card = self._create_metric_mini_card("Repeat Customers", "0", "🔄", "#F59E0B")
        self.repeat_customers_label = repeat_card.findChild(QLabel)
        metrics_layout.addWidget(repeat_card)

        layout.addWidget(metrics_frame)

        # Insights
        self.retention_insight_label = QLabel()
        self.retention_insight_label.setStyleSheet("color: #94a3b8; font-size: 10pt;")
        self.retention_insight_label.setWordWrap(True)
        layout.addWidget(self.retention_insight_label)

        layout.addStretch()
        return tab

    def _create_monthly_comparison_tab(self):
        """Create monthly comparison tab - compact"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        # Compact header
        header = QLabel("📅 This Month vs Previous Month")
        header.setStyleSheet("font-size: 12pt; font-weight: bold; color: white;")
        layout.addWidget(header)

        # Compact comparison cards
        comparison_frame = QFrame()
        comparison_frame.setStyleSheet("background-color: #334155; border-radius: 6px;")
        comparison_layout = QHBoxLayout(comparison_frame)
        comparison_layout.setContentsMargins(15, 15, 15, 15)
        comparison_layout.setSpacing(15)

        # Current Month Card
        curr_month_card = self._create_month_card("Current Month", "₹0", "📅", "#22d3ee")
        self.curr_month_revenue_label = curr_month_card.findChild(QLabel)
        comparison_layout.addWidget(curr_month_card)

        # Previous Month Card
        prev_month_card = self._create_month_card("Previous Month", "₹0", "📅", "#3B82F6")
        self.prev_month_revenue_label = prev_month_card.findChild(QLabel)
        comparison_layout.addWidget(prev_month_card)

        # Growth Card
        growth_card = self._create_month_card("Growth", "0%", "📈", "#10B981")
        self.growth_label = growth_card.findChild(QLabel)
        comparison_layout.addWidget(growth_card)

        layout.addWidget(comparison_frame)

        # Compact comparison table
        self.comparison_table = QTableWidget()
        self.comparison_table.setColumnCount(3)
        self.comparison_table.setHorizontalHeaderLabels(['Metric', 'Current Month', 'Previous Month'])
        self.comparison_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.comparison_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.comparison_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.comparison_table.setAlternatingRowColors(True)
        self.comparison_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.comparison_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.comparison_table.verticalHeader().setVisible(False)
        self.comparison_table.setMinimumHeight(120)
        self.comparison_table.setMaximumHeight(180)
        self.comparison_table.setStyleSheet("""
            QTableWidget {
                background-color: #1e293b;
                color: white;
                border: 1px solid #334155;
                border-radius: 6px;
                gridline-color: #334155;
            }
            QHeaderView::section {
                background-color: #334155;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
                font-size: 9pt;
            }
        """)
        layout.addWidget(self.comparison_table)
        return tab

    def _create_payment_alerts_tab(self):
        """Create payment alerts tab - compact"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        # Compact header
        header = QLabel("⚠️ Payment Pending Alerts")
        header.setStyleSheet("font-size: 12pt; font-weight: bold; color: #F59E0B;")
        layout.addWidget(header)

        self.alert_count_label = QLabel()
        self.alert_count_label.setStyleSheet("font-size: 9pt; color: #94a3b8;")
        layout.addWidget(self.alert_count_label)

        # Compact alerts table
        self.alerts_table = QTableWidget()
        self.alerts_table.setColumnCount(6)
        self.alerts_table.setHorizontalHeaderLabels(['Customer', 'Mobile', 'Invoice', 'Amount Due', 'Days', 'Status'])
        self.alerts_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.alerts_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.alerts_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.alerts_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.alerts_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.alerts_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        self.alerts_table.setAlternatingRowColors(True)
        self.alerts_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.alerts_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.alerts_table.verticalHeader().setVisible(False)
        self.alerts_table.setMinimumHeight(200)
        self.alerts_table.setMaximumHeight(280)
        self.alerts_table.setStyleSheet("""
            QTableWidget {
                background-color: #1e293b;
                color: white;
                border: 1px solid #334155;
                border-radius: 6px;
                gridline-color: #334155;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #334155;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
                font-size: 9pt;
            }
        """)
        layout.addWidget(self.alerts_table)

        # Compact action button
        remind_btn = QPushButton("📱 Send WhatsApp Reminder")
        remind_btn.setObjectName("successButton")
        remind_btn.setFixedHeight(35)
        remind_btn.clicked.connect(self._send_whatsapp_reminder)
        layout.addWidget(remind_btn)
        return tab

    def _create_main_content(self, layout):
        """Create main content area - REMOVED duplicate sections
        All analytics data is now shown only in the Advanced Analytics tabs above
        """
        # REMOVED: Duplicate Revenue Summary and Top Services cards
        # These were duplicating data already shown in Analytics tabs
        pass

    def _create_info_card(self, title):
        """Create an info card"""
        card = QFrame()
        card.setStyleSheet("""
            background-color: #334155;
            border-radius: 8px;
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 14pt;
            font-weight: bold;
            color: white;
        """)
        layout.addWidget(title_label)

        # Separator
        separator = QFrame()
        separator.setFixedHeight(1)
        separator.setStyleSheet("background-color: #475569;")
        layout.addWidget(separator)

        return card

    def _create_pending_payments(self, layout):
        """Create pending payments table"""
        # Title
        title_label = QLabel("⏳ Pending Payments")
        title_label.setStyleSheet("""
            font-size: 16pt;
            font-weight: bold;
            color: white;
        """)
        layout.addWidget(title_label)

        # Table card
        table_card = self._create_info_card("")
        table_layout = QVBoxLayout(table_card)

        # Table
        self.pending_table = QTableWidget()
        self.pending_table.setColumnCount(4)
        self.pending_table.setHorizontalHeaderLabels(['Customer Name', 'Amount Due', 'Date', 'Invoice No'])
        self.pending_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.pending_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.pending_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.pending_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.pending_table.setAlternatingRowColors(True)
        self.pending_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.pending_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.pending_table.verticalHeader().setVisible(False)
        self.pending_table.setMinimumHeight(200)

        table_layout.addWidget(self.pending_table)
        layout.addWidget(table_card)

    def _create_metric_mini_card(self, title, value, icon, color):
        """Create a mini metric card for analytics tabs"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame#metricMiniCard {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1e293b,
                    stop:1 #0f172a);
                border: 3px solid {color};
                border-radius: 16px;
            }}
            QFrame#metricMiniCard:hover {{
                border: 3px solid #ffffff;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #334155,
                    stop:1 #1e293b);
            }}
        """)
        card.setObjectName("metricMiniCard")
        card.setMinimumSize(200, 150)
        card.setMaximumHeight(160)
        card.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Top row: Icon + Value
        top_layout = QHBoxLayout()
        top_layout.setSpacing(15)
        
        # Icon with animated background
        icon_frame = QFrame()
        icon_frame.setFixedSize(60, 60)
        icon_frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {color}40,
                    stop:1 {color}20);
                border-radius: 30px;
                border: 3px solid {color};
            }}
        """)
        icon_layout = QVBoxLayout(icon_frame)
        icon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: 26pt; color: {color};")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_layout.addWidget(icon_label)
        top_layout.addWidget(icon_frame)
        
        # Value (right side)
        value_label = QLabel(str(value))
        value_label.setObjectName("metricValue")
        value_label.setStyleSheet(f"""
            font-size: 26pt;
            font-weight: bold;
            color: {color};
        """)
        value_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        top_layout.addWidget(value_label)
        top_layout.setStretch(1, 1)
        
        layout.addLayout(top_layout)

        # Title (bottom)
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #94a3b8; font-size: 10pt; font-weight: 600;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setWordWrap(True)
        layout.addWidget(title_label)

        return card

    def _create_month_card(self, title, value, icon, color):
        """Create a month comparison card"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame#monthCard {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1e293b,
                    stop:1 #0f172a);
                border: 3px solid {color};
                border-radius: 16px;
            }}
            QFrame#monthCard:hover {{
                border: 3px solid #ffffff;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #334155,
                    stop:1 #1e293b);
            }}
        """)
        card.setObjectName("monthCard")
        card.setMinimumSize(220, 170)
        card.setMaximumHeight(180)
        card.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Icon with background
        icon_frame = QFrame()
        icon_frame.setFixedSize(55, 55)
        icon_frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {color}40,
                    stop:1 {color}20);
                border-radius: 28px;
                border: 3px solid {color};
            }}
        """)
        icon_layout = QVBoxLayout(icon_frame)
        icon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: 22pt; color: {color};")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_layout.addWidget(icon_label)
        layout.addWidget(icon_frame)
        layout.setAlignment(icon_frame, Qt.AlignmentFlag.AlignHCenter)

        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #94a3b8; font-size: 10pt; font-weight: 600;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Value
        value_label = QLabel(str(value))
        value_label.setObjectName("monthValue")
        value_label.setStyleSheet(f"""
            font-size: 24pt;
            font-weight: bold;
            color: {color};
        """)
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(value_label)

        return card

    def _on_card_clicked(self, metric_name):
        """Handle metric card click - show detailed view"""
        # Get metric data
        metric_data = {}
        if hasattr(self, 'loaded_data'):
            metric_data = self.loaded_data
        
        # Handle AMC card click - navigate to AMC section
        if metric_name == 'amc_contracts':
            # Navigate to AMC section
            self._navigate_to_amc()
            return

        # Create and show detail dialog for other metrics (pass current period)
        dialog = DetailViewDialog(self, metric_name, metric_data, self.period)
        dialog.exec_()
    
    def _navigate_to_amc(self):
        """Navigate to AMC section"""
        try:
            # Find parent window and show AMC
            parent = self.parentWidget()
            while parent:
                if hasattr(parent, '_show_amc'):
                    parent._show_amc()
                    return
                parent = parent.parentWidget()
            
            # Fallback - try to find main window
            from PySide6.QtWidgets import QApplication
            for widget in QApplication.topLevelWidgets():
                if hasattr(widget, '_show_amc'):
                    widget._show_amc()
                    return
        except Exception as e:
            print(f"Navigation error: {e}")

    def load_dashboard_data(self):
        """Load dashboard data from database"""
        self.run_in_thread(
            self._load_data_thread,
            self._update_ui
        )

    def _load_data_thread(self):
        """Load data in background thread"""
        from database.db_connection import DatabaseContext

        # Calculate date range
        today = datetime.now().date()

        if self.period == 'today':
            start_date = today
            end_date = today
            range_text = today.strftime('%d %b, %Y')
        elif self.period == 'this_week':
            start_date = today - timedelta(days=today.weekday())
            end_date = today
            range_text = f"{start_date.strftime('%d %b')} - {today.strftime('%d %b, %Y')}"
        elif self.period == 'this_month':
            start_date = today.replace(day=1)
            end_date = today
            range_text = today.strftime('%B %Y')
        else:  # this_year
            start_date = today.replace(month=1, day=1)
            end_date = today
            range_text = str(today.year)

        with DatabaseContext() as db:
            # Total customers
            result = db.execute_query(
                "SELECT COUNT(*) as count FROM customers WHERE is_active = TRUE",
                fetch_one=True
            )
            total_customers = result['count'] if result else 0

            # Total services for period
            query = """
                SELECT COUNT(*) as count FROM invoices
                WHERE is_active = TRUE AND DATE(created_at) BETWEEN %s AND %s
            """
            result = db.execute_query(query, (start_date, end_date), fetch_one=True)
            total_services = result['count'] if result else 0

            # Total revenue for period
            query = """
                SELECT COALESCE(SUM(total_amount), 0) as revenue FROM invoices
                WHERE is_active = TRUE AND DATE(created_at) BETWEEN %s AND %s
            """
            result = db.execute_query(query, (start_date, end_date), fetch_one=True)
            total_revenue = result['revenue'] if result else 0

            # Today's services
            query = """
                SELECT COUNT(*) as count FROM invoices
                WHERE is_active = TRUE AND DATE(created_at) = CURDATE()
            """
            result = db.execute_query(query, fetch_one=True)
            today_services = result['count'] if result else 0

            # Pending payments
            query = """
                SELECT c.name as customer_name, i.balance_amount,
                       DATE(i.created_at) as invoice_date, i.invoice_number
                FROM invoices i
                JOIN customers c ON i.customer_id = c.id
                WHERE i.is_active = TRUE AND i.balance_amount > 0
                ORDER BY i.created_at DESC
                LIMIT 10
            """
            pending_payments = db.execute_query(query, fetch_all=True)

            # Revenue summary
            query = """
                SELECT DATE(created_at) as date, COUNT(*) as count,
                       SUM(total_amount) as total,
                       SUM(advance_payment) as paid_amount
                FROM invoices
                WHERE is_active = TRUE AND DATE(created_at) BETWEEN %s AND %s
                GROUP BY DATE(created_at)
                ORDER BY date DESC
                LIMIT 5
            """
            recent_invoices = db.execute_query(query, (start_date, end_date), fetch_all=True)

            # Service summary
            query = """
                SELECT s.service_name, COUNT(*) as count
                FROM invoice_items ii
                JOIN services s ON ii.service_id = s.id
                JOIN invoices i ON ii.invoice_id = i.id
                WHERE i.is_active = TRUE AND DATE(i.created_at) BETWEEN %s AND %s
                GROUP BY s.service_name
                ORDER BY count DESC
                LIMIT 5
            """
            top_services = db.execute_query(query, (start_date, end_date), fetch_all=True)

            # AMC Statistics
            amc_query = """
                SELECT COUNT(*) as count FROM amc_contracts
                WHERE amc_status = 'Active' AND is_active = TRUE
            """
            result = db.execute_query(amc_query, fetch_one=True)
            amc_active = result['count'] if result else 0

            # Online Requests Count
            online_requests_query = """
                SELECT
                    (SELECT COUNT(*) FROM contact_messages WHERE status = 'Pending') +
                    (SELECT COUNT(*) FROM service_requests WHERE request_status = 'Pending') as total
            """
            result = db.execute_query(online_requests_query, fetch_one=True)
            online_requests = result['total'] if result else 0

            return {
                'total_customers': total_customers,
                'total_services': total_services,
                'total_revenue': total_revenue,
                'today_services': today_services,
                'amc_contracts': amc_active,
                'online_requests': online_requests,
                'range_text': range_text,
                'pending_payments': pending_payments,
                'recent_invoices': recent_invoices,
                'top_services': top_services
            }

    def _update_ui(self, data):
        """Update UI with loaded data"""
        # Store data for detail views
        self.loaded_data = data

        # Initialize auto-refresh counters
        self.last_online_count = data.get('online_requests', 0)
        self.last_invoice_count = data.get('total_services', 0)
        self.last_revenue_count = data.get('total_revenue', 0)

        # Update date range
        self.date_range_label.setText(f"({data['range_text']})")

        # Update metric cards
        if 'total_customers' in self.metric_cards:
            self.metric_cards['total_customers'].set_value(str(data['total_customers']))
        if 'total_services' in self.metric_cards:
            self.metric_cards['total_services'].set_value(str(data['total_services']))
        if 'total_revenue' in self.metric_cards:
            self.metric_cards['total_revenue'].set_value(f"₹{data['total_revenue']:,.0f}")
        if 'amc_contracts' in self.metric_cards:
            self.metric_cards['amc_contracts'].set_value(str(data['amc_contracts']))
        if 'online_requests' in self.metric_cards:
            self.metric_cards['online_requests'].set_value(str(data['online_requests']))
        if 'today_services' in self.metric_cards:
            self.metric_cards['today_services'].set_value(str(data['today_services']))

        # REMOVED: Revenue and Services label updates
        # These were duplicate sections - data is now only shown in Analytics tabs above

        # Update pending payments table - REMOVED (Duplicate - already in Analytics Payment Alerts tab)
        # self.pending_table.setRowCount(0)
        # for payment in data['pending_payments']:
        #     row = self.pending_table.rowCount()
        #     self.pending_table.insertRow(row)
        #     self.pending_table.setItem(row, 0, QTableWidgetItem(payment['customer_name'] or 'N/A'))
        #     self.pending_table.setItem(row, 1, QTableWidgetItem(f"₹{payment['balance_amount']:,.2f}"))
        #     self.pending_table.setItem(row, 2, QTableWidgetItem(payment['invoice_date'].strftime('%d-%m-%Y')))
        #     self.pending_table.setItem(row, 3, QTableWidgetItem(payment['invoice_number'] or 'N/A'))

        # Activity label - REMOVED (Duplicate data)
        # Previously showed: Latest invoice, Amount, Count
        # This data is already in Revenue Trend tab

    def _on_period_change(self, text):
        """Handle period filter change"""
        period_map = {
            'Today': 'today',
            'This Week': 'this_week',
            'This Month': 'this_month',
            'This Year': 'this_year'
        }
        self.period = period_map.get(text, 'today')
        self.load_dashboard_data()
        self.load_analytics_data()

    def load_analytics_data(self):
        """Load analytics data for all tabs"""
        self.run_in_thread(
            self._load_analytics_thread,
            self._update_analytics_ui
        )

    def _load_analytics_thread(self):
        """Load analytics data in background thread"""
        from database.db_connection import DatabaseContext
        
        with DatabaseContext() as db:
            from controllers.dashboard_controller import DashboardController
            controller = DashboardController(db)
            
            # Get all analytics data (excluding customer retention)
            analytics_data = {
                'revenue_trend': controller.get_revenue_trend(days=30),
                'top_services': controller.get_top_services(limit=10, period='monthly'),
                'monthly_comparison': controller.get_monthly_comparison(),
                'payment_alerts': controller.get_payment_pending_alerts(limit=10)
            }
            
            return analytics_data

    def _update_analytics_ui(self, data):
        """Update analytics UI with loaded data"""
        try:
            # Update Revenue Trend Tab
            self._update_revenue_trend(data['revenue_trend'])
            
            # Update Top Services Tab
            self._update_top_services(data['top_services'])
            
            # Update Monthly Comparison Tab
            self._update_monthly_comparison(data['monthly_comparison'])
            
            # Update Payment Alerts Tab
            self._update_payment_alerts(data['payment_alerts'])
            
        except Exception as e:
            print(f"Error updating analytics UI: {e}")

    def _update_revenue_trend(self, trend_data):
        """Update revenue trend tab"""
        if not trend_data:
            self.revenue_chart_label.setText("No revenue data available")
            self.revenue_stats_label.setText("")
            return
        
        # Calculate totals
        total_revenue = sum(item['daily_revenue'] for item in trend_data)
        total_invoices = sum(item['invoice_count'] for item in trend_data)
        avg_daily = total_revenue / len(trend_data) if trend_data else 0
        
        # Find best day
        best_day = max(trend_data, key=lambda x: x['daily_revenue']) if trend_data else None
        
        # Display data
        chart_text = f"📊 Last 30 Days Revenue Summary:\n\n"
        chart_text += f"• Total Revenue: ₹{total_revenue:,.2f}\n"
        chart_text += f"• Total Invoices: {total_invoices}\n"
        chart_text += f"• Average Daily: ₹{avg_daily:,.2f}\n"
        
        if best_day:
            chart_text += f"• Best Day: {best_day['date']} (₹{best_day['daily_revenue']:,.2f})"
        
        self.revenue_chart_label.setText(chart_text)
        self.revenue_stats_label.setText(f"📈 Showing data for last 30 days")

    def _update_top_services(self, services_data):
        """Update top services table"""
        self.top_services_table.setRowCount(0)
        
        if not services_data:
            return
        
        for service in services_data:
            row = self.top_services_table.rowCount()
            self.top_services_table.insertRow(row)
            
            self.top_services_table.setItem(row, 0, QTableWidgetItem(service['service_name'] or 'N/A'))
            self.top_services_table.setItem(row, 1, QTableWidgetItem(f"₹{service['service_price']:,.2f}"))
            self.top_services_table.setItem(row, 2, QTableWidgetItem(str(service['times_sold'])))
            self.top_services_table.setItem(row, 3, QTableWidgetItem(f"₹{service['total_revenue']:,.2f}"))

    def _update_retention(self, retention_data):
        """Update customer retention tab"""
        if not retention_data:
            return
        
        rate = retention_data.get('retention_rate', 0)
        prev = retention_data.get('previous_customers', 0)
        curr = retention_data.get('current_customers', 0)
        repeat = retention_data.get('repeat_customers', 0)
        
        # Update labels
        if self.retention_rate_label:
            self.retention_rate_label.setText(f"{rate}%")
        
        if self.prev_customers_label:
            self.prev_customers_label.setText(str(prev))
        
        if self.curr_customers_label:
            self.curr_customers_label.setText(str(curr))
        
        if self.repeat_customers_label:
            self.repeat_customers_label.setText(str(repeat))
        
        # Add insights
        if rate >= 70:
            insight = "✅ Excellent! You have a very high customer retention rate. This indicates strong customer satisfaction and loyalty."
        elif rate >= 50:
            insight = "👍 Good retention rate. Consider implementing loyalty programs to improve it further."
        elif rate >= 30:
            insight = "⚠️ Average retention. Focus on customer follow-ups and service quality to improve retention."
        else:
            insight = "❗ Low retention rate. Immediate attention needed. Consider customer feedback surveys and service improvements."
        
        self.retention_insight_label.setText(insight)

    def _update_monthly_comparison(self, comparison_data):
        """Update monthly comparison tab"""
        if not comparison_data:
            return
        
        curr = comparison_data.get('current_month', {})
        prev = comparison_data.get('previous_month', {})
        rev_growth = comparison_data.get('revenue_growth', 0)
        count_growth = comparison_data.get('count_growth', 0)
        
        # Update cards
        if self.curr_month_revenue_label:
            self.curr_month_revenue_label.setText(f"₹{curr.get('revenue', 0):,.0f}")
        
        if self.prev_month_revenue_label:
            self.prev_month_revenue_label.setText(f"₹{prev.get('revenue', 0):,.0f}")
        
        if self.growth_label:
            if rev_growth >= 0:
                self.growth_label.setText(f"+{rev_growth}%")
                self.growth_label.setStyleSheet("font-size: 20pt; font-weight: bold; color: #10B981;")
            else:
                self.growth_label.setText(f"{rev_growth}%")
                self.growth_label.setStyleSheet("font-size: 20pt; font-weight: bold; color: #F59E0B;")
        
        # Update comparison table
        self.comparison_table.setRowCount(0)
        
        metrics = [
            ('Total Revenue', f"₹{curr.get('revenue', 0):,.2f}", f"₹{prev.get('revenue', 0):,.2f}"),
            ('Invoices Count', str(curr.get('invoice_count', 0)), str(prev.get('invoice_count', 0))),
            ('Amount Collected', f"₹{curr.get('collected', 0):,.2f}", f"₹{prev.get('collected', 0):,.2f}"),
            ('Amount Pending', f"₹{curr.get('pending', 0):,.2f}", f"₹{prev.get('pending', 0):,.2f}")
        ]
        
        for metric_name, curr_val, prev_val in metrics:
            row = self.comparison_table.rowCount()
            self.comparison_table.insertRow(row)
            self.comparison_table.setItem(row, 0, QTableWidgetItem(metric_name))
            self.comparison_table.setItem(row, 1, QTableWidgetItem(curr_val))
            self.comparison_table.setItem(row, 2, QTableWidgetItem(prev_val))

    def _update_payment_alerts(self, alerts_data):
        """Update payment alerts tab"""
        if not alerts_data:
            self.alerts_table.setRowCount(0)
            self.alert_count_label.setText("(0 pending)")
            return
        
        self.alerts_table.setRowCount(len(alerts_data))
        self.alert_count_label.setText(f"({len(alerts_data)} pending)")
        
        for i, alert in enumerate(alerts_data):
            self.alerts_table.setItem(i, 0, QTableWidgetItem(alert['customer_name'] or 'N/A'))
            self.alerts_table.setItem(i, 1, QTableWidgetItem(alert['customer_mobile'] or 'N/A'))
            self.alerts_table.setItem(i, 2, QTableWidgetItem(alert['invoice_number'] or 'N/A'))
            self.alerts_table.setItem(i, 3, QTableWidgetItem(f"₹{alert['balance_amount']:,.2f}"))
            self.alerts_table.setItem(i, 4, QTableWidgetItem(f"{alert['days_pending']} days"))
            
            # Status based on days pending
            days = alert['days_pending']
            if days > 60:
                status = "🔴 Critical"
            elif days > 30:
                status = "🟠 Urgent"
            else:
                status = "🟡 Normal"

            self.alerts_table.setItem(i, 5, QTableWidgetItem(status))

    def _send_whatsapp_reminder(self):
        """🆕 Send WhatsApp reminder for pending payments - FREE integration"""
        # Get selected row
        selected_rows = self.alerts_table.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(
                self,
                "No Selection",
                "Please select a customer from the table to send WhatsApp reminder."
            )
            return
        
        # Get customer data from selected row
        row = selected_rows[0].row()
        customer_name = self.alerts_table.item(row, 0).text()
        mobile = self.alerts_table.item(row, 1).text()
        invoice_number = self.alerts_table.item(row, 2).text()
        balance_amount = self.alerts_table.item(row, 3).text()
        
        # Ask for confirmation
        reply = QMessageBox.question(
            self,
            "Send Payment Reminder",
            f"📱 Kya aap {customer_name} ko payment reminder bhejna chahte hain?\n\n"
            f"Mobile: {mobile}\n"
            f"Invoice: {invoice_number}\n"
            f"Due Amount: {balance_amount}",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
        
        if reply == QMessageBox.Yes:
            try:
                from utils.whatsapp_helper import WhatsAppHelper
                from utils.whatsapp_messages import format_message
                from datetime import datetime
                
                # Format payment reminder message
                message = format_message(
                    'payment_reminder',
                    customer_name=customer_name,
                    invoice_number=invoice_number,
                    balance_amount=balance_amount.replace('₹', '').replace(',', ''),
                    invoice_date=datetime.now().strftime('%d-%m-%Y')
                )
                
                # Send WhatsApp message
                WhatsAppHelper.send_message(mobile, message)
                
                self.show_success_message("✅ Payment reminder bheja gaya!")
                
            except Exception as e:
                self.show_error_message(f"WhatsApp error: {str(e)}")
                print(f"WhatsApp reminder error: {str(e)}")

    def refresh_data(self):
        """Refresh dashboard data"""
        self.load_dashboard_data()
