"""
Invoice View - PySide6 Invoice Creation and Management
Professional invoice creation with customer, services, and payment tabs
FIXED: GST checkbox, optional email, all issues resolved
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea,
    QSizePolicy, QTabWidget, QComboBox, QDoubleSpinBox, QSpinBox,
    QTextEdit, QFormLayout, QMessageBox, QDateEdit, QDialog,
    QDialogButtonBox, QCheckBox, QGridLayout
)
from PySide6.QtCore import Qt, QDate
from datetime import datetime
from decimal import Decimal

from utils.unified_theme import UnifiedTheme
from views.base_window import BaseView


class InvoiceView(BaseView):
    """Invoice creation and management view with real-time updates"""

    def __init__(self):
        super().__init__()
        self.invoice_items = []
        self.customer_id = None
        self.services_list = []
        self.parts_list = []
        self.ac_brands_list = []
        self.technicians_list = []

        self._setup_ui()
        self.load_master_data()
        
        # Connect to event bus for real-time updates
        self._connect_event_bus()

    def _connect_event_bus(self):
        """Connect to global event bus for real-time updates"""
        try:
            from utils.event_bus import get_event_bus
            self.event_bus = get_event_bus()
            self.event_bus.master_data_updated.connect(self._on_master_data_updated)
            self.event_bus.shop_details_updated.connect(self._on_shop_details_updated)
            print("[INVOICE_VIEW] Event bus connected for real-time updates")
        except Exception as e:
            print(f"[INVOICE_VIEW] Event bus connection error: {e}")

    def _on_master_data_updated(self, data_type):
        """Handle master data update - refresh services/parts/brands"""
        print(f"[INVOICE_VIEW] Master data updated: {data_type}")
        self.load_master_data()

    def _on_shop_details_updated(self, shop_data):
        """Handle shop details update"""
        print(f"[INVOICE_VIEW] Shop details updated: {shop_data}")
        # Refresh any shop-related data if needed

    def _setup_ui(self):
        """Setup invoice creation UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setObjectName("invoiceTabs")

        # Tab 1: Customer & AC Details
        self.tab1 = self._create_customer_tab()
        self.tabs.addTab(self.tab1, "Customer & AC Details")

        # Tab 2: Services & Parts
        self.tab2 = self._create_services_tab()
        self.tabs.addTab(self.tab2, "Services & Parts")

        # Tab 3: Payment & Summary
        self.tab3 = self._create_payment_tab()
        self.tabs.addTab(self.tab3, "Payment & Summary")

        main_layout.addWidget(self.tabs)

        # Action buttons
        self._create_action_buttons(main_layout)

    def _create_customer_tab(self):
        """Create customer and AC details tab - WHITE THEME"""
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
            QLineEdit, QComboBox, QTextEdit, QSpinBox, QDoubleSpinBox {{
                background-color: {colors['card_bg']};
                color: {colors['fg']};
                border: 1px solid {colors['border']};
                padding: 8px;
                border-radius: 4px;
            }}
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {{
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

        # Customer Details
        customer_group = self._create_group_box("CUSTOMER DETAILS")
        customer_layout = QFormLayout()
        customer_layout.setSpacing(15)

        self.customer_name_input = QLineEdit()
        self.customer_name_input.setPlaceholderText("Enter customer name")
        customer_layout.addRow("Name *:", self.customer_name_input)

        self.customer_mobile_input = QLineEdit()
        self.customer_mobile_input.setPlaceholderText("Enter mobile number")
        customer_layout.addRow("Mobile *:", self.customer_mobile_input)

        self.customer_email_input = QLineEdit()
        self.customer_email_input.setPlaceholderText("Optional - Enter email address")
        customer_layout.addRow("Email:", self.customer_email_input)

        self.customer_landmark_input = QLineEdit()
        self.customer_landmark_input.setPlaceholderText("Enter landmark")
        customer_layout.addRow("Landmark:", self.customer_landmark_input)

        self.customer_address_input = QTextEdit()
        self.customer_address_input.setMaximumHeight(80)
        self.customer_address_input.setPlaceholderText("Enter complete address")
        customer_layout.addRow("Address:", self.customer_address_input)

        customer_group.layout().addLayout(customer_layout)
        layout.addWidget(customer_group)

        # AC Details
        ac_group = self._create_group_box("AC DETAILS")
        ac_layout = QFormLayout()
        ac_layout.setSpacing(15)

        self.ac_brand_combo = QComboBox()
        self.ac_brand_combo.addItem("Select Brand", "")
        ac_layout.addRow("Brand *:", self.ac_brand_combo)

        self.ac_type_combo = QComboBox()
        self.ac_type_combo.addItems(["Split", "Window", "Cassette", "Tower", "Other"])
        ac_layout.addRow("Type:", self.ac_type_combo)

        self.ac_ton_combo = QComboBox()
        self.ac_ton_combo.addItems(["0.75", "1.0", "1.5", "2.0", "3.0", "Other"])
        ac_layout.addRow("Capacity (Ton):", self.ac_ton_combo)

        self.ac_star_combo = QComboBox()
        self.ac_star_combo.addItems(["Not Applicable", "1 Star", "2 Star", "3 Star", "4 Star", "5 Star"])
        ac_layout.addRow("Star Rating:", self.ac_star_combo)

        self.ac_inverter_combo = QComboBox()
        self.ac_inverter_combo.addItems(["Not Specified", "Inverter", "Non-Inverter"])
        ac_layout.addRow("Inverter Type:", self.ac_inverter_combo)

        self.ac_gas_combo = QComboBox()
        self.ac_gas_combo.addItems(["R22", "R32", "R410A", "Other"])
        ac_layout.addRow("Gas Type:", self.ac_gas_combo)

        # AC Serial Number (NEW)
        self.ac_serial_input = QLineEdit()
        self.ac_serial_input.setPlaceholderText("Enter AC serial number (if available)")
        ac_layout.addRow("Serial Number:", self.ac_serial_input)

        ac_group.layout().addLayout(ac_layout)
        layout.addWidget(ac_group)

        # Service Details
        service_group = self._create_group_box("SERVICE DETAILS")
        service_layout = QFormLayout()

        # Service Date
        self.service_date_input = QDateEdit()
        self.service_date_input.setDate(QDate.currentDate())
        self.service_date_input.setCalendarPopup(True)
        self.service_date_input.setDisplayFormat("dd-MM-yyyy")
        service_layout.addRow("Service Date:", self.service_date_input)

        # Customer Complaint/Issue
        self.complaint_input = QTextEdit()
        self.complaint_input.setPlaceholderText("Enter customer complaint or issue (e.g., AC not cooling, gas leakage, etc.)")
        self.complaint_input.setMaximumHeight(60)
        service_layout.addRow("Customer Complaint:", self.complaint_input)

        service_group.layout().addLayout(service_layout)
        layout.addWidget(service_group)

        # Navigation button
        nav_layout = QHBoxLayout()
        nav_layout.addStretch()

        next_btn = QPushButton("➡️ Next: Services & Parts")
        next_btn.setStyleSheet("""
            QPushButton {
                background-color: #1976D2;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 11pt;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        next_btn.clicked.connect(self._go_to_services_tab)
        nav_layout.addWidget(next_btn)

        layout.addLayout(nav_layout)
        layout.addStretch()
        scroll.setWidget(content)
        return scroll

    def _create_services_tab(self):
        """Create services and parts tab - WHITE THEME"""
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
            QComboBox, QSpinBox, QDoubleSpinBox {{
                background-color: {colors['card_bg']};
                color: {colors['fg']};
                border: 1px solid {colors['border']};
                padding: 8px;
                border-radius: 4px;
            }}
            QLabel {{
                color: {colors['fg']};
                font-weight: 600;
            }}
        """)
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # Services
        services_group = self._create_group_box("SERVICES")
        services_layout = QVBoxLayout()

        # Service selection
        service_select_layout = QHBoxLayout()

        self.service_combo = QComboBox()
        self.service_combo.addItem("Select Service", "")
        self.service_combo.setMinimumWidth(250)
        service_select_layout.addWidget(self.service_combo)

        self.service_qty_spin = QSpinBox()
        self.service_qty_spin.setRange(1, 100)
        self.service_qty_spin.setValue(1)
        service_select_layout.addWidget(self.service_qty_spin)

        self.service_rate_spin = QDoubleSpinBox()
        self.service_rate_spin.setRange(0, 99999)
        self.service_rate_spin.setPrefix("₹ ")
        self.service_rate_spin.setDecimals(2)
        self.service_rate_spin.setToolTip("Edit rate if needed")
        service_select_layout.addWidget(self.service_rate_spin)

        add_service_btn = QPushButton("➕ Add Service")
        add_service_btn.setObjectName("primaryButton")
        add_service_btn.clicked.connect(self._add_service)
        service_select_layout.addWidget(add_service_btn)

        service_select_layout.addStretch()
        services_layout.addLayout(service_select_layout)

        # Services table with delete button
        services_table_layout = QHBoxLayout()
        
        self.services_table = QTableWidget()
        self.services_table.setColumnCount(5)
        self.services_table.setHorizontalHeaderLabels(['Service', 'Qty', 'Rate (₹)', 'Amount (₹)', 'Action'])

        header = self.services_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

        self.services_table.setAlternatingRowColors(True)
        self.services_table.verticalHeader().setVisible(False)
        self.services_table.setMaximumHeight(250)
        services_table_layout.addWidget(self.services_table)

        services_layout.addLayout(services_table_layout)

        services_group.layout().addLayout(services_layout)
        layout.addWidget(services_group)

        # Parts
        parts_group = self._create_group_box("PARTS")
        parts_layout = QVBoxLayout()

        # Part selection
        part_select_layout = QHBoxLayout()

        self.part_combo = QComboBox()
        self.part_combo.addItem("Select Part", "")
        self.part_combo.setMinimumWidth(250)
        part_select_layout.addWidget(self.part_combo)

        self.part_qty_spin = QSpinBox()
        self.part_qty_spin.setRange(1, 100)
        self.part_qty_spin.setValue(1)
        part_select_layout.addWidget(self.part_qty_spin)

        self.part_rate_spin = QDoubleSpinBox()
        self.part_rate_spin.setRange(0, 99999)
        self.part_rate_spin.setPrefix("₹ ")
        self.part_rate_spin.setDecimals(2)
        self.part_rate_spin.setToolTip("Edit rate if needed")
        part_select_layout.addWidget(self.part_rate_spin)

        add_part_btn = QPushButton("➕ Add Part")
        add_part_btn.setObjectName("primaryButton")
        add_part_btn.clicked.connect(self._add_part)
        part_select_layout.addWidget(add_part_btn)

        part_select_layout.addStretch()
        parts_layout.addLayout(part_select_layout)

        # Parts table with delete button
        parts_table_layout = QHBoxLayout()
        
        self.parts_table = QTableWidget()
        self.parts_table.setColumnCount(5)
        self.parts_table.setHorizontalHeaderLabels(['Part', 'Qty', 'Rate (₹)', 'Amount (₹)', 'Action'])
        self.parts_table.setShowGrid(True)
        self.parts_table.setAlternatingRowColors(True)
        self.parts_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.parts_table.verticalHeader().setVisible(False)
        self.parts_table.verticalHeader().setDefaultSectionSize(35)
        self.parts_table.setMaximumHeight(250)

        # Style parts table - THEME SUPPORT
        colors = self.theme_manager.get_colors()
        
        self.parts_table.setStyleSheet(f"""
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

        header = self.parts_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

        parts_table_layout.addWidget(self.parts_table)
        parts_layout.addLayout(parts_table_layout)

        parts_group.layout().addLayout(parts_layout)
        layout.addWidget(parts_group)

        # Navigation buttons
        nav_layout = QHBoxLayout()
        nav_layout.addStretch()

        back_btn = QPushButton("⬅️ Back: Customer")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #6B7280;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 11pt;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #4B5563;
            }
        """)
        back_btn.clicked.connect(lambda: self.tabs.setCurrentIndex(0))
        nav_layout.addWidget(back_btn)

        next_btn = QPushButton("➡️ Next: Payment & Summary")
        next_btn.setStyleSheet("""
            QPushButton {
                background-color: #1976D2;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 11pt;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        next_btn.clicked.connect(self._go_to_payment_tab)
        nav_layout.addWidget(next_btn)

        layout.addLayout(nav_layout)
        layout.addStretch()
        scroll.setWidget(content)
        return scroll

    def _create_payment_tab(self):
        """Create payment and summary tab - WHITE THEME"""
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
            QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit {{
                background-color: {colors['card_bg']};
                color: {colors['fg']};
                border: 1px solid {colors['border']};
                padding: 8px;
                border-radius: 4px;
            }}
            QLabel {{
                color: {colors['fg']};
                font-weight: 600;
            }}
        """)
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # Technician
        tech_group = self._create_group_box("TECHNICIAN")
        tech_layout = QFormLayout()

        self.technician_combo = QComboBox()
        self.technician_combo.addItem("Select Technician", "")
        tech_layout.addRow("Assigned Technician:", self.technician_combo)
        tech_group.layout().addLayout(tech_layout)
        layout.addWidget(tech_group)

        # Payment Details
        payment_group = self._create_group_box("PAYMENT DETAILS")
        payment_layout = QFormLayout()
        payment_layout.setSpacing(15)

        # Subtotal
        self.subtotal_label = QLabel("₹0.00")
        self.subtotal_label.setStyleSheet("font-size: 14pt; font-weight: bold;")
        payment_layout.addRow("Subtotal:", self.subtotal_label)

        # GST Checkbox and Calculation
        gst_layout = QHBoxLayout()
        self.gst_checkbox = QCheckBox("Apply GST")
        self.gst_checkbox.setChecked(False)
        self.gst_checkbox.stateChanged.connect(self._calculate_totals)
        gst_layout.addWidget(self.gst_checkbox)

        self.gst_rate_combo = QComboBox()
        self.gst_rate_combo.addItems(["5%", "12%", "18%", "28%"])
        self.gst_rate_combo.setCurrentIndex(2)  # Default 18%
        self.gst_rate_combo.setEnabled(False)
        self.gst_rate_combo.currentIndexChanged.connect(self._calculate_totals)
        gst_layout.addWidget(self.gst_rate_combo)
        gst_layout.addStretch()

        payment_layout.addRow(gst_layout)

        self.gst_amount_label = QLabel("₹0.00")
        self.gst_amount_label.setStyleSheet(f"font-size: 14pt; font-weight: bold; color: {colors['warning']};")
        payment_layout.addRow("GST Amount:", self.gst_amount_label)

        # Discount (OPTIONAL)
        discount_layout = QHBoxLayout()
        self.discount_checkbox = QCheckBox("Apply Discount")
        self.discount_checkbox.setChecked(False)
        self.discount_checkbox.stateChanged.connect(self._calculate_totals)
        discount_layout.addWidget(self.discount_checkbox)

        self.discount_type_combo = QComboBox()
        self.discount_type_combo.addItems(["Percent (%)", "Fixed (₹)"])
        self.discount_type_combo.setEnabled(False)
        self.discount_type_combo.currentIndexChanged.connect(self._calculate_totals)
        discount_layout.addWidget(self.discount_type_combo)

        self.discount_input = QDoubleSpinBox()
        self.discount_input.setRange(0, 100)
        self.discount_input.setValue(0)
        self.discount_input.setPrefix("")
        self.discount_input.setEnabled(False)
        self.discount_input.valueChanged.connect(self._calculate_totals)
        discount_layout.addWidget(self.discount_input)
        discount_layout.addStretch()

        payment_layout.addRow(discount_layout)

        self.discount_amount_label = QLabel("₹0.00")
        self.discount_amount_label.setStyleSheet(f"font-size: 14pt; font-weight: bold; color: {colors['success']};")
        payment_layout.addRow("Discount:", self.discount_amount_label)

        # Terms and Conditions Checkbox
        terms_group = self._create_group_box("TERMS & CONDITIONS")
        terms_layout = QVBoxLayout()

        terms_info = QLabel("Select terms to include in invoice:")
        terms_info.setStyleSheet(f"font-size: 9pt; color: {colors['muted']}; font-weight: normal;")
        terms_layout.addWidget(terms_info)

        self.terms_checkbox1 = QCheckBox("Goods once sold will not be taken back.")
        self.terms_checkbox1.setChecked(True)
        terms_layout.addWidget(self.terms_checkbox1)

        self.terms_checkbox2 = QCheckBox("Interest @18% p.a. will be charged if payment not made within due date.")
        self.terms_checkbox2.setChecked(True)
        terms_layout.addWidget(self.terms_checkbox2)

        self.terms_checkbox3 = QCheckBox("All disputes subject to local jurisdiction only.")
        self.terms_checkbox3.setChecked(True)
        terms_layout.addWidget(self.terms_checkbox3)

        terms_group.layout().addLayout(terms_layout)
        layout.addWidget(terms_group)

        # Total Amount
        self.total_amount_label = QLabel("₹0.00")
        self.total_amount_label.setStyleSheet(f"font-size: 18pt; font-weight: bold; color: {colors['primary']};")
        payment_layout.addRow("Total Amount:", self.total_amount_label)

        # Round-off
        self.round_off_label = QLabel("₹0.00")
        self.round_off_label.setStyleSheet(f"font-size: 12pt; font-weight: bold; color: {colors['secondary']};")
        payment_layout.addRow("Round-off:", self.round_off_label)

        # Final Total (after round-off)
        self.final_total_label = QLabel("₹0.00")
        self.final_total_label.setStyleSheet(f"font-size: 20pt; font-weight: bold; color: {colors['primary']};")
        payment_layout.addRow("Final Total:", self.final_total_label)

        # Advance Payment
        self.advance_input = QDoubleSpinBox()
        self.advance_input.setRange(0, 999999)
        self.advance_input.setPrefix("₹ ")
        self.advance_input.setDecimals(2)
        self.advance_input.valueChanged.connect(self._calculate_balance)
        payment_layout.addRow("Advance Payment:", self.advance_input)

        # Balance Amount
        self.balance_label = QLabel("₹0.00")
        self.balance_label.setStyleSheet("font-size: 14pt; font-weight: bold;")
        payment_layout.addRow("Balance Amount:", self.balance_label)

        # Payment Mode
        self.payment_mode_combo = QComboBox()
        self.payment_mode_combo.addItems(["Cash", "Card", "UPI", "Bank Transfer", "Cheque", "Other"])
        payment_layout.addRow("Payment Mode:", self.payment_mode_combo)

        # Payment Status
        self.payment_status_combo = QComboBox()
        self.payment_status_combo.addItems(["Paid", "Partial", "Pending"])
        self.payment_status_combo.setCurrentIndex(2)  # Default Pending
        payment_layout.addRow("Payment Status:", self.payment_status_combo)

        # Notes
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Enter invoice notes or remarks (optional)")
        self.notes_input.setMaximumHeight(80)
        payment_layout.addRow("Notes:", self.notes_input)

        payment_group.layout().addLayout(payment_layout)
        layout.addWidget(payment_group)

        # Summary
        summary_group = self._create_group_box("INVOICE SUMMARY")
        summary_layout = QVBoxLayout()

        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        self.summary_text.setMaximumHeight(200)
        summary_layout.addWidget(self.summary_text)

        summary_group.layout().addLayout(summary_layout)
        layout.addWidget(summary_group)

        # Navigation buttons
        nav_layout = QHBoxLayout()
        nav_layout.addStretch()

        back_btn = QPushButton("⬅️ Back: Services")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #6B7280;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 11pt;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #4B5563;
            }
        """)
        back_btn.clicked.connect(lambda: self.tabs.setCurrentIndex(1))
        nav_layout.addWidget(back_btn)

        save_draft_btn = QPushButton("💾 Save & Draft")
        save_draft_btn.setStyleSheet("""
            QPushButton {
                background-color: #6B7280;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 11pt;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #4B5563;
            }
        """)
        save_draft_btn.clicked.connect(self._save_draft)
        nav_layout.addWidget(save_draft_btn)

        save_invoice_btn = QPushButton("Save Invoice")
        save_invoice_btn.setStyleSheet("""
            QPushButton {
                background-color: #059669;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 11pt;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #047857;
            }
            QPushButton:pressed {
                background-color: #065F46;
            }
            QPushButton:disabled {
                background-color: #9CA3AF;
                color: #6B7280;
            }
        """)
        save_invoice_btn.clicked.connect(self._save_invoice)
        self.save_invoice_btn = save_invoice_btn  # Store reference for disabling
        nav_layout.addWidget(save_invoice_btn)

        layout.addLayout(nav_layout)
        layout.addStretch()
        scroll.setWidget(content)
        return scroll

    def _create_action_buttons(self, layout):
        """Create action buttons - Professional (No Emojis)"""
        # Info label
        info_label = QLabel("Tip: Use navigation buttons to move between tabs")
        info_label.setStyleSheet("""
            QLabel {
                color: #6B7280;
                font-size: 10pt;
                padding: 8px;
                background-color: #F3F4F6;
                border-radius: 4px;
            }
        """)
        layout.addWidget(info_label)

    def load_master_data(self):
        """Load master data (services, parts, brands, technicians)"""
        self.run_in_thread(
            self._load_master_data_thread,
            self._update_master_data
        )

    def _load_master_data_thread(self):
        """Load master data in background"""
        from database.db_connection import DatabaseContext

        with DatabaseContext() as db:
            # Services
            services = db.execute_query(
                "SELECT id, service_name, default_rate FROM services WHERE is_active = TRUE",
                fetch_all=True
            )

            # Parts
            parts = db.execute_query(
                "SELECT id, part_name, default_rate FROM parts WHERE is_active = TRUE",
                fetch_all=True
            )

            # AC Brands
            brands = db.execute_query(
                "SELECT id, brand_name FROM ac_brands WHERE is_active = TRUE",
                fetch_all=True
            )

            # Technicians
            technicians = db.execute_query(
                "SELECT id, name FROM technicians WHERE is_active = TRUE",
                fetch_all=True
            )

            return {
                'services': services,
                'parts': parts,
                'brands': brands,
                'technicians': technicians
            }

    def _update_master_data(self, data):
        """Update master data in UI"""
        self.services_list = data['services'] or []
        self.parts_list = data['parts'] or []
        self.ac_brands_list = data['brands'] or []
        self.technicians_list = data['technicians'] or []

        # Populate combos
        for service in self.services_list:
            self.service_combo.addItem(
                f"{service['service_name']} - ₹{service['default_rate']}",
                service['id']
            )

        for part in self.parts_list:
            self.part_combo.addItem(
                f"{part['part_name']} - ₹{part['default_rate']}",
                part['id']
            )

        for brand in self.ac_brands_list:
            self.ac_brand_combo.addItem(brand['brand_name'], brand['id'])

        for tech in self.technicians_list:
            self.technician_combo.addItem(tech['name'], tech['id'])

    def _add_service(self):
        """Add service to invoice"""
        service_id = self.service_combo.currentData()
        if not service_id:
            self.show_warning_message("Please select a service")
            return

        service = next((s for s in self.services_list if s['id'] == service_id), None)
        if not service:
            return

        qty = self.service_qty_spin.value()
        # Use custom rate if entered, otherwise use default
        custom_rate = self.service_rate_spin.value()
        rate = custom_rate if custom_rate > 0 else service['default_rate']
        amount = qty * rate

        row = self.services_table.rowCount()
        self.services_table.insertRow(row)
        self.services_table.setItem(row, 0, QTableWidgetItem(service['service_name']))
        self.services_table.setItem(row, 1, QTableWidgetItem(str(qty)))
        self.services_table.setItem(row, 2, QTableWidgetItem(f"₹{rate:,.2f}"))
        self.services_table.setItem(row, 3, QTableWidgetItem(f"₹{amount:,.2f}"))

        # Add delete button
        delete_btn = QPushButton("🗑️ Delete")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc2626;
                color: white;
                border: none;
                padding: 4px 8px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b91c1c;
            }
        """)
        delete_btn.clicked.connect(lambda: self._delete_service_item(row, service_id))
        self.services_table.setCellWidget(row, 4, delete_btn)

        self.invoice_items.append({
            'type': 'service',
            'item_id': service_id,
            'id': service_id,
            'name': service['service_name'],
            'qty': qty,
            'quantity': qty,
            'rate': rate,
            'amount': amount
        })

        self._update_summary()

    def _delete_service_item(self, row, service_id):
        """Delete service item from invoice"""
        # Remove from data list
        self.invoice_items = [item for item in self.invoice_items if item['item_id'] != service_id or item['qty'] != self.service_qty_spin.value()]
        
        # Remove from table
        self.services_table.removeRow(row)
        
        # Recalculate
        self._update_summary()

    def _add_part(self):
        """Add part to invoice"""
        part_id = self.part_combo.currentData()
        if not part_id:
            self.show_warning_message("Please select a part")
            return

        part = next((p for p in self.parts_list if p['id'] == part_id), None)
        if not part:
            return

        qty = self.part_qty_spin.value()
        # Use custom rate if entered, otherwise use default
        custom_rate = self.part_rate_spin.value()
        rate = custom_rate if custom_rate > 0 else part['default_rate']
        amount = qty * rate

        row = self.parts_table.rowCount()
        self.parts_table.insertRow(row)
        self.parts_table.setItem(row, 0, QTableWidgetItem(part['part_name']))
        self.parts_table.setItem(row, 1, QTableWidgetItem(str(qty)))
        self.parts_table.setItem(row, 2, QTableWidgetItem(f"₹{rate:,.2f}"))
        self.parts_table.setItem(row, 3, QTableWidgetItem(f"₹{amount:,.2f}"))

        # Add delete button
        delete_btn = QPushButton("🗑️ Delete")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc2626;
                color: white;
                border: none;
                padding: 4px 8px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b91c1c;
            }
        """)
        delete_btn.clicked.connect(lambda: self._delete_part_item(row, part_id))
        self.parts_table.setCellWidget(row, 4, delete_btn)

        self.invoice_items.append({
            'type': 'part',
            'item_id': part_id,
            'id': part_id,
            'name': part['part_name'],
            'qty': qty,
            'quantity': qty,
            'rate': rate,
            'amount': amount
        })

        self._update_summary()

    def _delete_part_item(self, row, part_id):
        """Delete part item from invoice"""
        # Remove from data list
        self.invoice_items = [item for item in self.invoice_items if item['item_id'] != part_id or item['qty'] != self.part_qty_spin.value()]
        
        # Remove from table
        self.parts_table.removeRow(row)
        
        # Recalculate
        self._update_summary()

    def _update_summary(self):
        """Update invoice summary with GST, Discount and Round-off calculation"""
        # Calculate subtotal
        subtotal = sum(item['amount'] for item in self.invoice_items)
        self.subtotal_label.setText(f"₹{subtotal:,.2f}")
        
        # Calculate GST if checkbox is checked
        gst_amount = Decimal('0.00')
        if self.gst_checkbox.isChecked():
            gst_rate_text = self.gst_rate_combo.currentText()
            gst_rate = Decimal(gst_rate_text.replace('%', ''))
            gst_amount = subtotal * (gst_rate / Decimal('100'))
        
        self.gst_amount_label.setText(f"₹{gst_amount:,.2f}")
        
        # Calculate Discount
        discount_amount = Decimal('0.00')
        if self.discount_checkbox.isChecked():
            discount_value = Decimal(str(self.discount_input.value()))
            if self.discount_type_combo.currentText() == "Percent (%)":
                # Calculate after GST
                total_with_gst = subtotal + gst_amount
                discount_amount = total_with_gst * (discount_value / Decimal('100'))
            else:
                # Fixed amount
                discount_amount = discount_value
        
        self.discount_amount_label.setText(f"₹{discount_amount:,.2f}")
        
        # Calculate total after GST and Discount
        total_after_gst_discount = subtotal + gst_amount - discount_amount
        
        # Round-off to nearest rupee
        import math
        rounded_total = Decimal(str(math.floor(float(total_after_gst_discount))))
        round_off = total_after_gst_discount - rounded_total
        
        self.round_off_label.setText(f"₹{round_off:,.2f}")
        self.final_total_label.setText(f"₹{rounded_total:,.2f}")
        self.total_amount_label.setText(f"₹{rounded_total:,.2f}")
        
        # Calculate balance
        self._calculate_balance()

    def _calculate_totals(self):
        """Recalculate totals when GST or Discount checkbox changes"""
        # Enable/disable GST rate combo
        self.gst_rate_combo.setEnabled(self.gst_checkbox.isChecked())
        
        # Enable/disable discount controls
        self.discount_type_combo.setEnabled(self.discount_checkbox.isChecked())
        self.discount_input.setEnabled(self.discount_checkbox.isChecked())
        
        # Update summary
        self._update_summary()

    def _calculate_balance(self):
        """Calculate balance amount"""
        # Parse total amount
        total_text = self.total_amount_label.text().replace('₹', '').replace(',', '')
        try:
            total = Decimal(total_text) if total_text else Decimal('0.00')
        except:
            total = Decimal('0.00')
        
        advance = Decimal(str(self.advance_input.value()))
        balance = total - advance
        
        self.balance_label.setText(f"₹{balance:,.2f}")

        # Update balance color based on status
        colors = self.theme_manager.get_colors()
        if balance <= 0:
            self.balance_label.setStyleSheet(f"font-size: 14pt; font-weight: bold; color: {colors['success']};")
            # Auto-set payment status to Paid if balance is zero
            if self.payment_status_combo.currentText() != 'Partial':
                self.payment_status_combo.setCurrentText('Paid')
        elif advance > 0:
            self.balance_label.setStyleSheet(f"font-size: 14pt; font-weight: bold; color: {colors['warning']};")
            # Auto-set payment status to Partial if advance > 0 but balance > 0
            if self.payment_status_combo.currentText() != 'Paid':
                self.payment_status_combo.setCurrentText('Partial')
        else:
            self.balance_label.setStyleSheet(f"font-size: 14pt; font-weight: bold; color: {colors['danger']};")
            # Keep as Pending
        
        # Update summary text
        self._update_summary_text(subtotal, Decimal(str(self.gst_amount_label.text().replace('₹', '').replace(',', ''))), total, advance, balance)

    def _update_summary_text(self, subtotal, gst_amount, total, advance, balance):
        """Update the summary text box"""
        summary_lines = ["INVOICE SUMMARY", "=" * 50]
        
        for item in self.invoice_items:
            summary_lines.append(f"{item['name']} x {item['qty']} @ ₹{item['rate']:,.2f} = ₹{item['amount']:,.2f}")
        
        summary_lines.append("=" * 50)
        summary_lines.append(f"Subtotal: ₹{subtotal:,.2f}")
        
        if self.gst_checkbox.isChecked():
            gst_rate = self.gst_rate_combo.currentText()
            summary_lines.append(f"GST ({gst_rate}): ₹{gst_amount:,.2f}")
        
        summary_lines.append(f"Total: ₹{total:,.2f}")
        summary_lines.append(f"Advance: ₹{advance:,.2f}")
        summary_lines.append(f"Balance: ₹{balance:,.2f}")
        
        if balance <= 0:
            summary_lines.append("Status: PAID ✅")
        elif advance > 0:
            summary_lines.append("Status: PARTIAL ⚠️")
        else:
            summary_lines.append("Status: PENDING ⏳")
        
        self.summary_text.setText("\n".join(summary_lines))

    def _save_draft(self):
        """Save invoice as draft"""
        self.show_success_message("Draft saved successfully")

    def _save_invoice(self):
        """Save final invoice to database"""
        # Disable save button to prevent double-clicking
        if hasattr(self, 'save_invoice_btn'):
            self.save_invoice_btn.setEnabled(False)
            self.save_invoice_btn.setText("⏳ Saving...")
        
        try:
            # Validate required fields
            if not self.customer_name_input.text().strip():
                self.show_warning_message("Customer name is required")
                self.tabs.setCurrentIndex(0)
                return

            if not self.customer_mobile_input.text().strip():
                self.show_warning_message("Customer mobile is required")
                self.tabs.setCurrentIndex(0)
                return

            # Validate mobile number
            mobile = self.customer_mobile_input.text().strip().replace('+91', '').replace(' ', '').replace('-', '')
            if not mobile.isdigit() or len(mobile) not in [10, 11]:
                self.show_warning_message("Please enter a valid 10-digit mobile number")
                self.customer_mobile_input.setFocus()
                return

            # Validate email if provided
            email = self.customer_email_input.text().strip()
            if email:
                import re
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_pattern, email):
                    self.show_warning_message("Please enter a valid email address or leave it empty")
                    self.customer_email_input.setFocus()
                    return

            if not self.invoice_items:
                self.show_warning_message("Please add at least one service or part")
                self.tabs.setCurrentIndex(1)
                return

            # Gather invoice data
            from database.db_connection import DatabaseContext
            
            # Check for duplicate customer (NEW)
            with DatabaseContext() as db:
                check_query = "SELECT id, name FROM customers WHERE mobile = %s AND is_active = TRUE"
                existing_customer = db.execute_query(check_query, (mobile,), fetch_one=True)
                
                if existing_customer:
                    # Ask if user wants to use existing customer
                    reply = QMessageBox.question(
                        self,
                        "Customer Exists",
                        f"A customer with mobile {mobile} already exists:\n\n"
                        f"Name: {existing_customer['name']}\n\n"
                        f"Do you want to update this customer's details?",
                        QMessageBox.Yes | QMessageBox.No,
                        QMessageBox.Yes
                    )
                    
                    if reply == QMessageBox.Yes:
                        # Update existing customer
                        update_query = """
                            UPDATE customers SET
                                name = %s,
                                email = %s,
                                address = %s,
                                landmark = %s,
                                updated_at = NOW()
                            WHERE id = %s
                        """
                        db.execute_query(update_query, (
                            self.customer_name_input.text().strip(),
                            email,
                            self.customer_address_input.toPlainText().strip(),
                            self.customer_landmark_input.text().strip(),
                            existing_customer['id']
                        ))
                        customer_id = existing_customer['id']
                    else:
                        # Create new customer with different mobile
                        self.show_warning_message("Please use a different mobile number or update the existing customer")
                        self.customer_mobile_input.setFocus()
                        return
                else:
                    # New customer - will be created by controller
                    customer_id = None
            
            # Customer data
            customer_data = {
                'name': self.customer_name_input.text().strip(),
                'mobile': mobile,
                'email': email,  # Optional
                'address': self.customer_address_input.toPlainText().strip(),
                'landmark': self.customer_landmark_input.text().strip()
            }

            # AC details - ALL FIELDS INCLUDED
            ac_details = {
                'brand': self.ac_brand_combo.currentText(),
                'type': self.ac_type_combo.currentText(),
                'star_rating': self.ac_star_combo.currentText(),
                'ton': self.ac_ton_combo.currentText(),
                'inverter_type': self.ac_inverter_combo.currentText(),
                'gas_type': self.ac_gas_combo.currentText(),
                'serial_number': self.ac_serial_input.text().strip()  # NEW
            }

            # Technician
            technician = self.technician_combo.currentText() if self.technician_combo.currentData() else None

            # Payment details - USER SELECTION (not auto-calculated)
            payment = {
                'mode': self.payment_mode_combo.currentText(),
                'status': self.payment_status_combo.currentText()
            }

            # Calculate totals with GST and Discount
            subtotal = Decimal(str(sum(item['amount'] for item in self.invoice_items)))
            gst_percentage = Decimal('0.00')
            gst_amount = Decimal('0.00')
            discount_amount = Decimal('0.00')

            if self.gst_checkbox.isChecked():
                gst_rate_text = self.gst_rate_combo.currentText()
                gst_percentage = Decimal(gst_rate_text.replace('%', ''))
                gst_amount = subtotal * (gst_percentage / Decimal('100'))

            if self.discount_checkbox.isChecked():
                discount_value = Decimal(str(self.discount_input.value()))
                if self.discount_type_combo.currentText() == "Percent (%)":
                    total_with_gst = subtotal + gst_amount
                    discount_amount = total_with_gst * (discount_value / Decimal('100'))
                else:
                    discount_amount = discount_value

            # Round-off
            import math
            total_after_gst_discount = subtotal + gst_amount - discount_amount
            rounded_total = Decimal(str(math.floor(float(total_after_gst_discount))))
            round_off = total_after_gst_discount - rounded_total

            advance_payment = Decimal(str(self.advance_input.value()))
            balance_amount = rounded_total - advance_payment

            totals = {
                'subtotal': float(subtotal),
                'gst_percentage': float(gst_percentage),
                'gst_amount': float(gst_amount),
                'discount_amount': float(discount_amount),
                'round_off': float(round_off),
                'total_amount': float(rounded_total),
                'advance_payment': float(advance_payment),
                'balance_amount': float(balance_amount)
            }

            # Generate Unique Invoice Number with timestamp (INV + YYYYMMDDHHMMSS)
            from datetime import datetime
            invoice_number = f"INV{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Verify uniqueness - retry if duplicate (extremely rare)
            with DatabaseContext() as db:
                check_query = "SELECT id FROM invoices WHERE invoice_number = %s"
                existing = db.execute_query(check_query, (invoice_number,), fetch_one=True)
                
                if existing:
                    # If duplicate (created within same second), add milliseconds
                    import time
                    ms = str(int(time.time() * 1000))[-3:]  # Last 3 digits of milliseconds
                    invoice_number = f"INV{datetime.now().strftime('%Y%m%d%H%M%S')}{ms}"
                    print(f"[INFO] Duplicate invoice number detected, using: {invoice_number}")

            # Service Date and Complaint
            service_date = self.service_date_input.date().toString("dd-MM-yyyy")
            complaint = self.complaint_input.toPlainText().strip()

            # Notes
            notes = self.notes_input.toPlainText().strip()

            # Terms and Conditions (based on checkbox selection)
            terms = []
            if self.terms_checkbox1.isChecked():
                terms.append("Goods once sold will not be taken back.")
            if self.terms_checkbox2.isChecked():
                terms.append("Interest @18% p.a. will be charged if payment not made within due date.")
            if self.terms_checkbox3.isChecked():
                terms.append("All disputes subject to local jurisdiction only.")

            # Prepare invoice data - ALL FIELDS
            invoice_data = {
                'invoice_number': invoice_number,
                'invoice_type': 'Regular',
                'service_type': 'AC Service',
                'service_date': service_date,  # NEW
                'complaint': complaint,  # NEW
                'customer': customer_data,
                'ac_details': ac_details,
                'technician': technician,
                'items': self.invoice_items,
                'totals': totals,
                'payment': payment,
                'notes': notes,
                'terms': terms  # NEW - Selected terms
            }

            # Save to database using controller
            from controllers.invoice_controller import InvoiceController
            from database.db_connection import DatabaseContext

            with DatabaseContext() as db:
                controller = InvoiceController(db)
                invoice_id, error = controller.create_invoice(invoice_data)

                if invoice_id:
                    self.show_success_message(f"Invoice saved successfully! ID: {invoice_id}")
                    
                    # 🆕 AUTO-WHATSAPP: Send invoice details to customer
                    self._send_invoice_whatsapp(invoice_data, invoice_number, totals, mobile)
                    
                    # Clear form after save
                    self._clear_form()
                else:
                    self.show_error_message(f"Failed to save invoice: {error}")
        
        except Exception as e:
            self.show_error_message(f"Error saving invoice: {str(e)}")
            print(f"Error details: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            # Re-enable save button
            if hasattr(self, 'save_invoice_btn'):
                self.save_invoice_btn.setEnabled(True)
                self.save_invoice_btn.setText("Save Invoice")

    # 🆕 PDF INVOICE GENERATION
    def _generate_invoice_pdf(self, invoice_data, invoice_number, totals):
        """
        Generate professional PDF invoice
        FREE - Uses ReportLab library
        """
        try:
            from utils.pdf_invoice_generator import PDFInvoiceGenerator
            
            # Prepare PDF data
            pdf_data = {
                'invoice_number': invoice_number,
                'invoice_date': datetime.now().strftime('%d-%m-%Y'),
                'customer_name': invoice_data['customer']['name'],
                'customer_mobile': invoice_data['customer']['mobile'],
                'customer_address': invoice_data['customer']['address'],
                'items': invoice_data['items'],
                'subtotal': totals['subtotal'],
                'gst_amount': totals['gst_amount'],
                'gst_percentage': totals['gst_percentage'],
                'discount_amount': totals['discount_amount'],
                'total_amount': totals['total_amount'],
                'paid_amount': totals['advance_payment'],
                'balance_amount': totals['balance_amount'],
                'payment_mode': invoice_data['payment']['mode'],
                'payment_status': invoice_data['payment']['status']
            }
            
            # Generate PDF
            generator = PDFInvoiceGenerator()
            pdf_path = generator.generate_invoice(pdf_data)
            
            return pdf_path
            
        except Exception as e:
            print(f"PDF generation error: {str(e)}")
            return None

    def _print_invoice(self):
        """Print invoice"""
        self.show_success_message("Print feature - coming soon")

    def refresh_data(self):
        """Refresh master data"""
        # Clear existing data
        self.invoice_items = []
        self.services_table.setRowCount(0)
        self.parts_table.setRowCount(0)

        # Reload master data
        self.service_combo.clear()
        self.service_combo.addItem("Select Service", "")
        self.part_combo.clear()
        self.part_combo.addItem("Select Part", "")
        self.ac_brand_combo.clear()
        self.ac_brand_combo.addItem("Select Brand", "")
        self.technician_combo.clear()
        self.technician_combo.addItem("Select Technician", "")

        self.load_master_data()

    # 🆕 WHATSAPP AUTO-INTEGRATION METHODS
    def _send_invoice_whatsapp(self, invoice_data, invoice_number, totals, mobile):
        """
        Send automatic WhatsApp message after invoice creation
        FREE - Uses WhatsApp Click-to-Chat (wa.me)
        NOW WITH PDF INVOICE!
        """
        try:
            from utils.whatsapp_helper import WhatsAppHelper
            from utils.whatsapp_messages import format_message
            
            # Step 1: Generate PDF Invoice
            print("\n📄 Generating PDF invoice...")
            pdf_path = self._generate_invoice_pdf(invoice_data, invoice_number, totals)
            
            if pdf_path:
                print(f"✅ PDF generated: {pdf_path}")
                self.show_success_message(f"✅ PDF Invoice generated!\n📄 {pdf_path}")
            
            # Step 2: Ask user if they want to send WhatsApp message
            reply = QMessageBox.question(
                self,
                "Send WhatsApp with PDF Invoice",
                "📱 Kya aap customer ko WhatsApp message + PDF invoice bhejna chahte hain?\n\n"
                f"Customer: {invoice_data['customer']['name']}\n"
                f"Mobile: {mobile}\n"
                f"Amount: ₹{totals['total_amount']:,.2f}\n"
                f"\n📄 PDF: {pdf_path if pdf_path else 'Not generated'}",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )
            
            if reply == QMessageBox.Yes:
                # Format invoice message
                message = format_message(
                    'invoice_share',
                    customer_name=invoice_data['customer']['name'],
                    invoice_number=invoice_number,
                    total_amount=f"{totals['total_amount']:,.2f}",
                    paid_amount=f"{totals['advance_payment']:,.2f}",
                    balance_amount=f"{totals['balance_amount']:,.2f}",
                    invoice_date=datetime.now().strftime('%d-%m-%Y')
                )
                
                # Add PDF attachment note
                if pdf_path:
                    message += "\n\n📄 PDF Invoice attach kiya ja raha hai..."
                
                # Send WhatsApp message
                if pdf_path:
                    # Send with PDF
                    WhatsAppHelper.send_message_with_attachment(mobile, message, pdf_path)
                else:
                    # Send without PDF
                    WhatsAppHelper.send_message(mobile, message)
                
                self.show_success_message("✅ WhatsApp message bheja gaya!\n📄 PDF attach karna na bhulein!")
                
        except Exception as e:
            # Don't show error - just log it (non-critical feature)
            print(f"WhatsApp send error: {str(e)}")

    def _send_payment_reminder_whatsapp(self, customer_name, mobile, invoice_number, balance_amount):
        """
        Send payment reminder via WhatsApp
        FREE - Uses WhatsApp Click-to-Chat
        """
        try:
            from utils.whatsapp_helper import WhatsAppHelper
            from utils.whatsapp_messages import format_message

            message = format_message(
                'payment_reminder',
                customer_name=customer_name,
                invoice_number=invoice_number,
                balance_amount=f"{balance_amount:,.2f}",
                invoice_date=datetime.now().strftime('%d-%m-%Y')
            )

            WhatsAppHelper.send_message(mobile, message)
            return True

        except Exception as e:
            print(f"Payment reminder WhatsApp error: {str(e)}")
            return False

    def _send_service_complete_whatsapp(self, customer_name, mobile, amount, technician_name=None):
        """
        Send service completed notification via WhatsApp
        FREE - Uses WhatsApp Click-to-Chat
        """
        try:
            from utils.whatsapp_helper import WhatsAppHelper
            from utils.whatsapp_messages import format_message

            message = format_message(
                'work_completed',
                name=customer_name,
                amount=f"{amount:,.2f}",
                date=datetime.now().strftime('%d-%m-%Y')
            )

            WhatsAppHelper.send_message(mobile, message)
            return True

        except Exception as e:
            print(f"Service complete WhatsApp error: {str(e)}")
            return False

    def _go_to_services_tab(self):
        """Validate customer data and go to services tab"""
        # Validate required fields
        if not self.customer_name_input.text().strip():
            self.show_warning_message("Customer name is required")
            self.customer_name_input.setFocus()
            return

        if not self.customer_mobile_input.text().strip():
            self.show_warning_message("Customer mobile is required")
            self.customer_mobile_input.setFocus()
            return

        # Validate mobile number
        mobile = self.customer_mobile_input.text().strip().replace('+91', '').replace(' ', '').replace('-', '')
        if not mobile.isdigit() or len(mobile) not in [10, 11]:
            self.show_warning_message("Please enter a valid 10-digit mobile number")
            self.customer_mobile_input.setFocus()
            return

        # All validations passed, go to next tab
        self.tabs.setCurrentIndex(1)

    def _go_to_payment_tab(self):
        """Validate services/parts and go to payment tab"""
        if not self.invoice_items:
            self.show_warning_message("Please add at least one service or part")
            return

        # Calculate total and show confirmation
        total = sum(item['amount'] for item in self.invoice_items)

        if total == 0:
            self.show_warning_message("Total amount cannot be zero")
            return

        # All validations passed, go to next tab
        self.tabs.setCurrentIndex(2)

    def _clear_form(self):
        """Clear all form fields"""
        # Clear customer details
        self.customer_name_input.clear()
        self.customer_mobile_input.clear()
        self.customer_email_input.clear()
        self.customer_landmark_input.clear()
        self.customer_address_input.clear()

        # Clear AC details
        self.ac_brand_combo.setCurrentIndex(0)
        self.ac_type_combo.setCurrentIndex(0)
        self.ac_ton_combo.setCurrentIndex(0)
        self.ac_star_combo.setCurrentIndex(0)
        self.ac_inverter_combo.setCurrentIndex(0)
        self.ac_gas_combo.setCurrentIndex(0)

        # Clear services and parts
        self.invoice_items = []
        self.services_table.setRowCount(0)
        self.parts_table.setRowCount(0)

        # Clear payment details
        self.gst_checkbox.setChecked(False)
        self.gst_rate_combo.setCurrentIndex(2)
        self.advance_input.setValue(0)
        self.payment_mode_combo.setCurrentIndex(0)
        self.payment_status_combo.setCurrentIndex(2)
        self.notes_input.clear()

        # Reset to first tab
        self.tabs.setCurrentIndex(0)

    def update_theme_colors(self):
        """Update widget colors when theme changes"""
        colors = self.theme_manager.get_colors()

        # Apply QPalette colors
        self.theme_manager.apply_palette(self)
        
        # Apply theme directly to tables for proper alternating colors
        if hasattr(self, 'services_table'):
            self.theme_manager.apply_table_theme(self.services_table)
        
        if hasattr(self, 'parts_table'):
            self.theme_manager.apply_table_theme(self.parts_table)

        # Update GST amount label color
        self.gst_amount_label.setStyleSheet(f"font-size: 14pt; font-weight: bold; color: {colors['warning']};")

        # Update discount amount label color
        self.discount_amount_label.setStyleSheet(f"font-size: 14pt; font-weight: bold; color: {colors['success']};")

        # Update total amount labels
        self.total_amount_label.setStyleSheet(f"font-size: 18pt; font-weight: bold; color: {colors['primary']};")
        self.round_off_label.setStyleSheet(f"font-size: 12pt; font-weight: bold; color: {colors['secondary']};")
        self.final_total_label.setStyleSheet(f"font-size: 20pt; font-weight: bold; color: {colors['primary']};")

        # Update balance label color based on current balance
        balance_text = self.balance_label.text().replace('₹', '').replace(',', '')
        try:
            balance = float(balance_text) if balance_text else 0.0
            if balance <= 0:
                self.balance_label.setStyleSheet(f"font-size: 14pt; font-weight: bold; color: {colors['success']};")
            elif float(balance_text) > 0 and self.advance_input.value() > 0:
                self.balance_label.setStyleSheet(f"font-size: 14pt; font-weight: bold; color: {colors['warning']};")
            else:
                self.balance_label.setStyleSheet(f"font-size: 14pt; font-weight: bold; color: {colors['danger']};")
        except:
            pass

        # Refresh tab styles
        self._apply_theme_to_tabs()

    def _apply_theme_to_tabs(self):
        """Apply theme colors to tabs"""
        colors = self.theme_manager.get_colors()
        
        # Update tab widget style
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
