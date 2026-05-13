"""
Invoice View - PySide6 Invoice Creation and Management
Professional invoice creation with IMPROVED UI/UX
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea,
    QSizePolicy, QTabWidget, QComboBox, QDoubleSpinBox, QSpinBox,
    QTextEdit, QFormLayout, QMessageBox, QDateEdit, QDialog,
    QDialogButtonBox, QCheckBox, QGridLayout, QAbstractItemView, QGroupBox,
    QSplitter
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QColor, QBrush
from datetime import datetime
from decimal import Decimal

from utils.unified_theme import UnifiedTheme
from views.base_window import BaseView


class InvoiceView(BaseView):
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
        self._connect_event_bus()

    def _connect_event_bus(self):
        try:
            from utils.event_bus import get_event_bus
            self.event_bus = get_event_bus()
            self.event_bus.master_data_updated.connect(self._on_master_data_updated)
            print("[INVOICE_VIEW] Event bus connected")
        except Exception as e:
            print(f"[INVOICE_VIEW] Event bus error: {e}")

    def _on_master_data_updated(self, data_type):
        self.load_master_data()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        title_label = QLabel("CREATE NEW INVOICE")
        title_label.setStyleSheet("font-size: 18pt; font-weight: bold; color: #0891b2; padding: 5px 0px;")
        main_layout.addWidget(title_label)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { 
                border: 2px solid #0891b2; 
                border-radius: 8px; 
                background-color: white; 
                top: -1px;
            }
            QTabBar::tab { 
                background-color: #f1f5f9; 
                color: #475569; 
                padding: 12px 30px; 
                margin-right: 5px; 
                border-top-left-radius: 8px; 
                border-top-right-radius: 8px; 
                border: 1px solid #cbd5e1;
                border-bottom: none;
                font-weight: bold; 
                font-size: 11pt; 
            }
            QTabBar::tab:selected { 
                background-color: #0891b2; 
                color: white; 
                border: 2px solid #0891b2;
                border-bottom: 2px solid white;
                margin-bottom: -1px;
            }
            QTabBar::tab:hover:!selected { 
                background-color: #e2e8f0; 
                color: #0891b2;
            }
        """)

        self.tab1 = self._create_customer_tab()
        self.tabs.addTab(self.tab1, "1. Customer Details")

        self.tab2 = self._create_services_tab()
        self.tabs.addTab(self.tab2, "2. Services & Parts")

        self.tab3 = self._create_payment_tab()
        self.tabs.addTab(self.tab3, "3. Payment & Summary")

        main_layout.addWidget(self.tabs)
        self._create_action_buttons(main_layout)

    def _create_customer_tab(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { background-color: #f8fafc; border: none; }")

        main_widget = QWidget()
        main_widget.setStyleSheet("QWidget { background-color: #f8fafc; }")
        
        grid = QGridLayout(main_widget)
        grid.setSpacing(20)
        grid.setContentsMargins(20, 20, 20, 20)

        # Common label style for light background
        lbl_style = "font-weight: 600; color: #1e293b; font-size: 10pt;"

        # Customer Section
        cust_group = QGroupBox("👤 CUSTOMER INFORMATION")
        cust_group.setStyleSheet("""
            QGroupBox {
                background-color: #ffffff;
                border: 2px solid #0891b2;
                border-radius: 10px;
                margin-top: 15px;
                padding-top: 20px;
                font-size: 12pt;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
                color: #0891b2;
            }
        """)
        cust_layout = QGridLayout(cust_group)
        cust_layout.setSpacing(12)

        self.customer_name_input = self._create_input("Customer Name *")
        self.customer_mobile_input = self._create_input("Mobile *")
        self.customer_email_input = self._create_input("Email (Optional)")
        self.customer_landmark_input = self._create_input("Landmark")

        cust_layout.addWidget(self.customer_name_input['label'], 1, 0)
        cust_layout.addWidget(self.customer_name_input['input'], 1, 1)
        cust_layout.addWidget(self.customer_mobile_input['label'], 2, 0)
        cust_layout.addWidget(self.customer_mobile_input['input'], 2, 1)
        cust_layout.addWidget(self.customer_email_input['label'], 3, 0)
        cust_layout.addWidget(self.customer_email_input['input'], 3, 1)
        cust_layout.addWidget(self.customer_landmark_input['label'], 4, 0)
        cust_layout.addWidget(self.customer_landmark_input['input'], 4, 1)

        addr_label = QLabel("Address:")
        addr_label.setStyleSheet(lbl_style)
        self.customer_address_input = QTextEdit()
        self.customer_address_input.setPlaceholderText("Full Address")
        self.customer_address_input.setMaximumHeight(60)
        self._style_input(self.customer_address_input)
        cust_layout.addWidget(addr_label, 5, 0)
        cust_layout.addWidget(self.customer_address_input, 5, 1)

        grid.addWidget(cust_group, 0, 0)

        # AC Section
        ac_group = QGroupBox("❄️ AC DETAILS")
        ac_group.setStyleSheet("""
            QGroupBox {
                background-color: #ffffff;
                border: 2px solid #059669;
                border-radius: 10px;
                margin-top: 15px;
                padding-top: 20px;
                font-size: 12pt;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
                color: #059669;
            }
        """)
        ac_layout = QGridLayout(ac_group)
        ac_layout.setSpacing(12)

        self.ac_brand_combo = QComboBox()
        self.ac_brand_combo.addItem("Select Brand", "")
        self._style_combo(self.ac_brand_combo)
        brand_lbl = QLabel("Brand:")
        brand_lbl.setStyleSheet(lbl_style)
        ac_layout.addWidget(brand_lbl, 1, 0)
        ac_layout.addWidget(self.ac_brand_combo, 1, 1)

        type_lbl = QLabel("Type:")
        type_lbl.setStyleSheet(lbl_style)
        self.ac_type_combo = QComboBox()
        self.ac_type_combo.addItems(["Split", "Window", "Cassette", "Tower", "Other"])
        self._style_combo(self.ac_type_combo)
        ac_layout.addWidget(type_lbl, 2, 0)
        ac_layout.addWidget(self.ac_type_combo, 2, 1)

        cap_lbl = QLabel("Capacity:")
        cap_lbl.setStyleSheet(lbl_style)
        self.ac_ton_combo = QComboBox()
        self.ac_ton_combo.addItems(["1.0", "1.5", "2.0", "Other"])
        self._style_combo(self.ac_ton_combo)
        ac_layout.addWidget(cap_lbl, 3, 0)
        ac_layout.addWidget(self.ac_ton_combo, 3, 1)

        star_lbl = QLabel("Star Rating:")
        star_lbl.setStyleSheet(lbl_style)
        self.ac_star_combo = QComboBox()
        self.ac_star_combo.addItems(["3 Star", "5 Star", "2 Star", "Other"])
        self._style_combo(self.ac_star_combo)
        ac_layout.addWidget(star_lbl, 4, 0)
        ac_layout.addWidget(self.ac_star_combo, 4, 1)

        inv_lbl = QLabel("Inverter:")
        inv_lbl.setStyleSheet(lbl_style)
        self.ac_inverter_combo = QComboBox()
        self.ac_inverter_combo.addItems(["Inverter", "Non-Inverter", "Not Specified"])
        self._style_combo(self.ac_inverter_combo)
        ac_layout.addWidget(inv_lbl, 5, 0)
        ac_layout.addWidget(self.ac_inverter_combo, 5, 1)

        date_lbl = QLabel("Service Date:")
        date_lbl.setStyleSheet(lbl_style)
        self.service_date_input = QDateEdit()
        self.service_date_input.setDate(QDate.currentDate())
        self.service_date_input.setCalendarPopup(True)
        self.service_date_input.setDisplayFormat("dd-MM-yyyy")
        self._style_combo(self.service_date_input)
        ac_layout.addWidget(date_lbl, 6, 0)
        ac_layout.addWidget(self.service_date_input, 6, 1)

        grid.addWidget(ac_group, 0, 1)

        # Complaint
        comp_group = QGroupBox("📝 CUSTOMER COMPLAINT / ISSUE")
        comp_group.setStyleSheet("""
            QGroupBox {
                background-color: #fffbeb;
                border: 2px solid #d97706;
                border-radius: 10px;
                margin-top: 15px;
                padding-top: 20px;
                font-size: 11pt;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
                color: #d97706;
            }
        """)
        comp_layout = QVBoxLayout(comp_group)
        
        self.complaint_input = QTextEdit()
        self.complaint_input.setPlaceholderText("Describe the issue...")
        self.complaint_input.setMaximumHeight(50)
        self._style_input(self.complaint_input)
        comp_layout.addWidget(self.complaint_input)

        grid.addWidget(comp_group, 1, 0, 1, 2)

        # Navigation
        nav_frame = QFrame()
        nav_frame.setStyleSheet("background: transparent;")
        nav_layout = QHBoxLayout(nav_frame)
        nav_layout.addStretch()
        next_btn = QPushButton("Next: Services & Parts →")
        next_btn.setCursor(Qt.PointingHandCursor)
        next_btn.setMinimumHeight(45)
        next_btn.setMinimumWidth(200)
        next_btn.setStyleSheet("""
            QPushButton { 
                background-color: #0891b2; 
                color: white; 
                border: none; 
                padding: 10px 30px; 
                font-size: 11pt; 
                font-weight: bold; 
                border-radius: 8px; 
            } 
            QPushButton:hover { background-color: #0e7490; }
        """)
        next_btn.clicked.connect(self._go_to_services_tab)
        nav_layout.addWidget(next_btn)
        grid.addWidget(nav_frame, 2, 0, 1, 2)

        scroll.setWidget(main_widget)
        return scroll

    def _create_input(self, placeholder):
        label = QLabel(placeholder.replace("*", "") + ":")
        label.setStyleSheet("font-weight: 600; color: #1e293b; font-size: 10pt;")
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        self._style_input(input_field)
        return {'label': label, 'input': input_field}

    def _style_input(self, widget):
        widget.setStyleSheet("""
            QLineEdit, QTextEdit { 
                background-color: #ffffff; 
                color: #000000; 
                border: 1px solid #cbd5e1; 
                padding: 10px 12px; 
                border-radius: 6px; 
                min-height: 25px; 
                font-size: 10pt; 
            } 
            QLineEdit:focus, QTextEdit:focus { 
                border: 2px solid #0891b2; 
                background-color: #f0f9ff;
            }
        """)

    def _style_combo(self, combo):
        combo.setStyleSheet("""
            QComboBox, QDateEdit { 
                background-color: #ffffff; 
                color: #000000; 
                border: 1px solid #cbd5e1; 
                padding: 8px 12px; 
                border-radius: 6px; 
                min-height: 25px;
            } 
            QComboBox::drop-down, QDateEdit::drop-down { 
                background-color: #f1f5f9; 
                width: 30px; 
                border-left: 1px solid #cbd5e1;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
            } 
            QComboBox QAbstractItemView { 
                background-color: #ffffff; 
                color: #000000;
                selection-background-color: #0891b2; 
                selection-color: #ffffff;
                outline: none;
            }
            QComboBox::item {
                color: #000000;
                background-color: #ffffff;
                padding: 8px;
            }
            QComboBox::item:selected {
                background-color: #0891b2;
                color: #ffffff;
            }
        """)

    def _create_services_tab(self):
        main_widget = QWidget()
        main_widget.setStyleSheet("QWidget { background-color: #f8fafc; }")
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self._create_services_section())
        splitter.addWidget(self._create_parts_section())
        splitter.setSizes([500, 500])
        layout.addWidget(splitter, 1)

        nav_layout = QHBoxLayout()
        nav_layout.addStretch()
        back_btn = QPushButton("Back: Customer")
        back_btn.setStyleSheet("QPushButton { background-color: #6B7280; color: white; border: none; padding: 12px 25px; font-size: 11pt; font-weight: bold; border-radius: 6px; }")
        back_btn.clicked.connect(lambda: self.tabs.setCurrentIndex(0))
        next_btn = QPushButton("Next: Payment")
        next_btn.setStyleSheet("QPushButton { background-color: #0891b2; color: white; border: none; padding: 12px 25px; font-size: 11pt; font-weight: bold; border-radius: 6px; }")
        next_btn.clicked.connect(self._go_to_payment_tab)
        nav_layout.addWidget(back_btn)
        nav_layout.addWidget(next_btn)
        layout.addLayout(nav_layout)

        return main_widget

    def _create_services_section(self):
        frame = QFrame()
        frame.setStyleSheet("QFrame { background-color: #ecfdf5; border: 2px solid #059669; border-radius: 12px; padding: 15px; }")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)

        title = QLabel("SERVICES")
        title.setStyleSheet("font-size: 16pt; font-weight: bold; color: #065f46; padding-bottom: 5px; border-bottom: 3px solid #059669;")
        layout.addWidget(title)

        # Better organized controls
        ctrl_card = QFrame()
        ctrl_card.setStyleSheet("QFrame { background: white; border-radius: 8px; border: 1px solid #d1fae5; padding: 10px; }")
        ctrl_layout = QGridLayout(ctrl_card)
        ctrl_layout.setSpacing(10)
        
        # Row 1: Service Selection
        lbl_svc = QLabel("Select Service:")
        lbl_svc.setStyleSheet("font-weight: bold; color: #065f46;")
        ctrl_layout.addWidget(lbl_svc, 0, 0)
        self.service_combo = QComboBox()
        self.service_combo.addItem("-- Select Service --", "")
        self._style_combo(self.service_combo)
        self.service_combo.setMinimumWidth(250)
        ctrl_layout.addWidget(self.service_combo, 0, 1, 1, 3)
        
        # Row 2: Qty, Rate
        lbl_qty = QLabel("Qty:")
        lbl_qty.setStyleSheet("font-weight: bold; color: #065f46;")
        ctrl_layout.addWidget(lbl_qty, 1, 0)
        self.service_qty_spin = QSpinBox()
        self.service_qty_spin.setRange(1, 100)
        self.service_qty_spin.setStyleSheet("QSpinBox { background: white; color: black; border: 2px solid #059669; padding: 8px; border-radius: 5px; font-weight: bold; }")
        ctrl_layout.addWidget(self.service_qty_spin, 1, 1)
        
        lbl_rate = QLabel("Rate:")
        lbl_rate.setStyleSheet("font-weight: bold; color: #065f46;")
        ctrl_layout.addWidget(lbl_rate, 1, 2)
        self.service_rate_spin = QDoubleSpinBox()
        self.service_rate_spin.setRange(0, 99999)
        self.service_rate_spin.setPrefix("Rs ")
        self.service_rate_spin.setDecimals(0)
        self.service_rate_spin.setStyleSheet("QDoubleSpinBox { background: white; color: black; border: 2px solid #059669; padding: 8px; border-radius: 5px; font-weight: bold; }")
        ctrl_layout.addWidget(self.service_rate_spin, 1, 3)
        
        add_btn = QPushButton("+ ADD SERVICE")
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.setStyleSheet("""
            QPushButton { 
                background-color: #059669; 
                color: white; 
                border: none; 
                padding: 10px 20px; 
                font-weight: bold; 
                border-radius: 6px; 
                min-width: 120px;
            } 
            QPushButton:hover { background-color: #047857; }
        """)
        add_btn.clicked.connect(self._add_service)
        ctrl_layout.addWidget(add_btn, 2, 0, 1, 4)
        
        layout.addWidget(ctrl_card)

        self.services_table = self._create_table(['#', 'Service', 'Qty', 'Rate', 'Amount', ''])
        layout.addWidget(self.services_table, 1)
        return frame

    def _create_parts_section(self):
        frame = QFrame()
        frame.setStyleSheet("QFrame { background-color: #fff7ed; border: 2px solid #ea580c; border-radius: 12px; padding: 15px; }")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)

        title = QLabel("PARTS")
        title.setStyleSheet("font-size: 16pt; font-weight: bold; color: #9a3412; padding-bottom: 5px; border-bottom: 3px solid #ea580c;")
        layout.addWidget(title)

        # Better organized controls
        ctrl_card = QFrame()
        ctrl_card.setStyleSheet("QFrame { background: white; border-radius: 8px; border: 1px solid #ffedd5; padding: 10px; }")
        ctrl_layout = QGridLayout(ctrl_card)
        ctrl_layout.setSpacing(10)

        # Row 1: Part Selection
        lbl_prt = QLabel("Select Part:")
        lbl_prt.setStyleSheet("font-weight: bold; color: #9a3412;")
        ctrl_layout.addWidget(lbl_prt, 0, 0)
        self.part_combo = QComboBox()
        self.part_combo.addItem("-- Select Part --", "")
        self._style_combo(self.part_combo)
        self.part_combo.setMinimumWidth(250)
        ctrl_layout.addWidget(self.part_combo, 0, 1, 1, 3)
        
        # Row 2: Qty and Rate
        lbl_pqty = QLabel("Qty:")
        lbl_pqty.setStyleSheet("font-weight: bold; color: #9a3412;")
        ctrl_layout.addWidget(lbl_pqty, 1, 0)
        self.part_qty_spin = QSpinBox()
        self.part_qty_spin.setRange(1, 100)
        self.part_qty_spin.setStyleSheet("QSpinBox { background: white; color: black; border: 2px solid #ea580c; padding: 8px; border-radius: 5px; font-weight: bold; }")
        ctrl_layout.addWidget(self.part_qty_spin, 1, 1)
        
        lbl_prate = QLabel("Rate:")
        lbl_prate.setStyleSheet("font-weight: bold; color: #9a3412;")
        ctrl_layout.addWidget(lbl_prate, 1, 2)
        self.part_rate_spin = QDoubleSpinBox()
        self.part_rate_spin.setRange(0, 99999)
        self.part_rate_spin.setPrefix("Rs ")
        self.part_rate_spin.setDecimals(0)
        self.part_rate_spin.setStyleSheet("QDoubleSpinBox { background: white; color: black; border: 2px solid #ea580c; padding: 8px; border-radius: 5px; font-weight: bold; }")
        ctrl_layout.addWidget(self.part_rate_spin, 1, 3)
        
        add_btn = QPushButton("+ ADD PART")
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.setStyleSheet("""
            QPushButton { 
                background-color: #ea580c; 
                color: white; 
                border: none; 
                padding: 10px 20px; 
                font-weight: bold; 
                border-radius: 6px; 
                min-width: 120px;
            } 
            QPushButton:hover { background-color: #c2410c; }
        """)
        add_btn.clicked.connect(self._add_part)
        ctrl_layout.addWidget(add_btn, 2, 0, 1, 4)
        
        layout.addWidget(ctrl_card)

        self.parts_table = self._create_table(['#', 'Part', 'Qty', 'Rate', 'Amount', ''])
        layout.addWidget(self.parts_table, 1)
        return frame

    def _create_table(self, headers):
        table = QTableWidget()
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setStyleSheet("""
            QTableWidget { 
                background-color: #ffffff; 
                border: 1px solid #cbd5e1; 
                border-radius: 8px; 
            } 
            QHeaderView::section { 
                background-color: #0f172a; 
                color: white; 
                padding: 12px; 
                border: none; 
                font-weight: bold; 
                font-size: 10pt;
            } 
            QTableWidget::item { 
                padding: 10px; 
                color: #000000; 
                border-bottom: 1px solid #f1f5f9;
            } 
            QTableWidget::item:selected { 
                background-color: #e2e8f0; 
                color: #0891b2; 
                font-weight: bold;
            }
        """)
        
        # Adjust column stretching
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        # Set specific widths for small columns
        table.setColumnWidth(0, 50)  # #
        table.setColumnWidth(2, 60)  # Qty
        table.setColumnWidth(3, 100) # Rate
        table.setColumnWidth(4, 120) # Amount
        table.setColumnWidth(5, 110) # Action button (Delete)
        
        # Make the Name column (index 1) stretch to fill the rest of the space
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        
        return table

    def _create_payment_tab(self):
        main_widget = QWidget()
        main_widget.setStyleSheet("QWidget { background-color: #f1f5f9; }")
        layout = QGridLayout(main_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(25, 20, 25, 20)

        # Left Card: CALCULATOR
        left_card = QFrame()
        left_card.setStyleSheet("QFrame { background-color: #ffffff; border-radius: 15px; border: 2px solid #e2e8f0; }")
        left_layout = QVBoxLayout(left_card)
        left_layout.setContentsMargins(25, 25, 25, 25)
        left_layout.setSpacing(15)

        header = QLabel("PAYMENT CALCULATOR")
        header.setStyleSheet("font-size: 16pt; font-weight: bold; color: #0891b2; padding-bottom: 10px; border-bottom: 2px solid #0891b2;")
        left_layout.addWidget(header)

        # Calculator Grid for better alignment
        calc_grid = QGridLayout()
        calc_grid.setSpacing(15)
        
        # Subtotal
        sub_label = QLabel("Subtotal:")
        sub_label.setStyleSheet("font-size: 12pt; font-weight: bold; color: #64748b;")
        self.subtotal_label = QLabel("Rs 0")
        self.subtotal_label.setStyleSheet("font-size: 16pt; font-weight: bold; color: #0f172a;")
        calc_grid.addWidget(sub_label, 0, 0)
        calc_grid.addWidget(self.subtotal_label, 0, 1, Qt.AlignRight)

        # GST Row
        gst_row = QHBoxLayout()
        self.gst_checkbox = QCheckBox("GST")
        self.gst_checkbox.setStyleSheet("font-weight: bold; color: #0ea5e9;")
        self.gst_checkbox.stateChanged.connect(self._calculate_totals)
        gst_row.addWidget(self.gst_checkbox)
        self.gst_rate_combo = QComboBox()
        self.gst_rate_combo.addItems(["5%", "12%", "18%", "28%"])
        self.gst_rate_combo.setCurrentIndex(2)
        self.gst_rate_combo.setEnabled(False)
        self.gst_rate_combo.currentIndexChanged.connect(self._calculate_totals)
        self._style_combo(self.gst_rate_combo)
        gst_row.addWidget(self.gst_rate_combo)
        calc_grid.addLayout(gst_row, 1, 0)
        
        self.gst_amount_label = QLabel("Rs 0")
        self.gst_amount_label.setStyleSheet("font-size: 12pt; font-weight: bold; color: #0ea5e9;")
        calc_grid.addWidget(self.gst_amount_label, 1, 1, Qt.AlignRight)

        # Discount Row
        disc_row = QHBoxLayout()
        self.discount_checkbox = QCheckBox("Discount")
        self.discount_checkbox.setStyleSheet("font-weight: bold; color: #22c55e;")
        self.discount_checkbox.stateChanged.connect(self._calculate_totals)
        disc_row.addWidget(self.discount_checkbox)
        self.discount_type_combo = QComboBox()
        self.discount_type_combo.addItems(["%", "Rs"])
        self.discount_type_combo.setEnabled(False)
        self._style_combo(self.discount_type_combo)
        disc_row.addWidget(self.discount_type_combo)
        self.discount_input = QDoubleSpinBox()
        self.discount_input.setRange(0, 10000)
        self.discount_input.setEnabled(False)
        self.discount_input.valueChanged.connect(self._calculate_totals)
        self.discount_input.setStyleSheet("background: white; color: black; border: 1px solid #22c55e; padding: 5px; border-radius: 4px;")
        disc_row.addWidget(self.discount_input)
        calc_grid.addLayout(disc_row, 2, 0)
        
        self.discount_amount_label = QLabel("Rs 0")
        self.discount_amount_label.setStyleSheet("font-size: 12pt; font-weight: bold; color: #22c55e;")
        calc_grid.addWidget(self.discount_amount_label, 2, 1, Qt.AlignRight)

        # Total Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        sep.setStyleSheet("background-color: #cbd5e1;")
        calc_grid.addWidget(sep, 3, 0, 1, 2)

        # Grand Total
        total_label = QLabel("GRAND TOTAL:")
        total_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #0891b2;")
        self.total_amount_label = QLabel("Rs 0")
        self.total_amount_label.setStyleSheet("font-size: 24pt; font-weight: bold; color: #0891b2;")
        calc_grid.addWidget(total_label, 4, 0)
        calc_grid.addWidget(self.total_amount_label, 4, 1, Qt.AlignRight)

        # Advance
        adv_label = QLabel("Advance Paid:")
        adv_label.setStyleSheet("font-size: 12pt; font-weight: bold; color: #10b981;")
        self.advance_input = QDoubleSpinBox()
        self.advance_input.setRange(0, 999999)
        self.advance_input.setPrefix("Rs ")
        self.advance_input.setDecimals(0)
        self.advance_input.setMinimumHeight(45)
        self.advance_input.valueChanged.connect(self._calculate_balance)
        self.advance_input.setStyleSheet("QDoubleSpinBox { background: #f0fdf4; color: #065f46; border: 2px solid #10b981; padding: 5px 10px; border-radius: 8px; font-size: 14pt; font-weight: bold; }")
        calc_grid.addWidget(adv_label, 5, 0)
        calc_grid.addWidget(self.advance_input, 5, 1, Qt.AlignRight)

        # Balance
        bal_label = QLabel("BALANCE DUE:")
        bal_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #ef4444;")
        self.balance_label = QLabel("Rs 0")
        self.balance_label.setStyleSheet("font-size: 20pt; font-weight: bold; color: #ef4444;")
        calc_grid.addWidget(bal_label, 6, 0)
        calc_grid.addWidget(self.balance_label, 6, 1, Qt.AlignRight)

        left_layout.addLayout(calc_grid)
        
        # Payment Details Box
        pay_group = QGroupBox("PAYMENT DETAILS")
        pay_group.setStyleSheet("""
            QGroupBox { 
                font-weight: bold; 
                color: #475569; 
                border: 2px solid #e2e8f0; 
                border-radius: 10px; 
                margin-top: 20px; 
                padding-top: 20px; 
            }
            QGroupBox::title { subcontrol-origin: margin; left: 15px; padding: 0 5px; }
            QLabel { color: #475569; font-weight: bold; }
        """)
        pay_layout = QGridLayout(pay_group)
        pay_layout.setSpacing(10)
        
        self.technician_combo = QComboBox()
        self.technician_combo.addItem("-- Select Tech --", "")
        self._style_combo(self.technician_combo)
        pay_layout.addWidget(QLabel("Technician:"), 0, 0)
        pay_layout.addWidget(self.technician_combo, 0, 1)

        self.payment_mode_combo = QComboBox()
        self.payment_mode_combo.addItems(["Cash", "Card", "UPI", "Bank Transfer", "Cheque"])
        self._style_combo(self.payment_mode_combo)
        pay_layout.addWidget(QLabel("Payment Mode:"), 1, 0)
        pay_layout.addWidget(self.payment_mode_combo, 1, 1)

        self.payment_status_combo = QComboBox()
        self.payment_status_combo.addItems(["Paid", "Partial", "Pending"])
        self._style_combo(self.payment_status_combo)
        pay_layout.addWidget(QLabel("Status:"), 2, 0)
        pay_layout.addWidget(self.payment_status_combo, 2, 1)
        
        left_layout.addWidget(pay_group)
        left_layout.addStretch()
        layout.addWidget(left_card, 0, 0)

        # Right Card: INVOICE PREVIEW
        right_card = QFrame()
        right_card.setStyleSheet("QFrame { background-color: #ffffff; border-radius: 15px; border: 2px solid #64748b; }")
        right_layout = QVBoxLayout(right_card)
        right_layout.setContentsMargins(25, 25, 25, 25)
        right_layout.setSpacing(15)

        sum_header = QLabel("INVOICE PREVIEW")
        sum_header.setStyleSheet("font-size: 16pt; font-weight: bold; color: #475569; padding-bottom: 10px; border-bottom: 2px solid #64748b;")
        right_layout.addWidget(sum_header)

        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        self.summary_text.setStyleSheet("""
            QTextEdit { 
                background-color: #f8fafc; 
                color: #000000;
                border: 1px solid #cbd5e1; 
                border-radius: 8px; 
                font-family: 'Segoe UI', Arial; 
                font-size: 11pt; 
                padding: 15px; 
            }
        """)
        right_layout.addWidget(self.summary_text, 1)

        lbl_notes = QLabel("Internal Notes:")
        lbl_notes.setStyleSheet("color: #475569; font-weight: bold;")
        right_layout.addWidget(lbl_notes)
        
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Add any special instructions or internal notes here...")
        self.notes_input.setMaximumHeight(80)
        self.notes_input.setStyleSheet("QTextEdit { background-color: #ffffff; color: black; border: 1px solid #cbd5e1; border-radius: 8px; padding: 10px; }")
        right_layout.addWidget(self.notes_input)

        layout.addWidget(right_card, 0, 1)

        # Action Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        back_btn = QPushButton("← Back to Services")
        back_btn.setFixedSize(200, 50)
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet("""
            QPushButton { 
                background-color: #ffffff; 
                color: #64748b; 
                border: 2px solid #64748b; 
                font-size: 12pt; 
                font-weight: bold; 
                border-radius: 10px; 
            } 
            QPushButton:hover { background-color: #f1f5f9; }
        """)
        back_btn.clicked.connect(lambda: self.tabs.setCurrentIndex(1))
        
        save_btn = QPushButton("SAVE & GENERATE INVOICE")
        save_btn.setFixedSize(280, 50)
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.setStyleSheet("""
            QPushButton { 
                background-color: #10b981; 
                color: white; 
                border: none; 
                font-size: 12pt; 
                font-weight: bold; 
                border-radius: 10px; 
            } 
            QPushButton:hover { background-color: #059669; }
        """)
        save_btn.clicked.connect(self._save_invoice)
        self.save_invoice_btn = save_btn
        
        btn_layout.addWidget(back_btn)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout, 1, 0, 1, 2)

        return main_widget

    def _create_action_buttons(self, layout):
        info = QLabel("Tip: Fill details in order: Customer -> Services -> Payment")
        info.setStyleSheet("color: #64748b; font-size: 10pt; padding: 8px; background: #f1f5f9; border-radius: 4px;")
        layout.addWidget(info)

    def load_master_data(self):
        self.run_in_thread(self._load_master_data_thread, self._update_master_data)

    def _load_master_data_thread(self):
        from database.db_connection import DatabaseContext
        with DatabaseContext() as db:
            services = db.execute_query("SELECT id, service_name, default_rate FROM services WHERE is_active = TRUE", fetch_all=True)
            parts = db.execute_query("SELECT id, part_name, default_rate FROM parts WHERE is_active = TRUE", fetch_all=True)
            brands = db.execute_query("SELECT id, brand_name FROM ac_brands WHERE is_active = TRUE", fetch_all=True)
            technicians = db.execute_query("SELECT id, name FROM technicians WHERE is_active = TRUE", fetch_all=True)
            return {'services': services, 'parts': parts, 'brands': brands, 'technicians': technicians}

    def _update_master_data(self, data):
        self.services_list = data['services'] or []
        self.parts_list = data['parts'] or []
        self.ac_brands_list = data['brands'] or []
        self.technicians_list = data['technicians'] or []

        for s in self.services_list:
            self.service_combo.addItem(f"{s['service_name']} - Rs {s['default_rate']}", s['id'])
        for p in self.parts_list:
            self.part_combo.addItem(f"{p['part_name']} - Rs {p['default_rate']}", p['id'])
        for b in self.ac_brands_list:
            self.ac_brand_combo.addItem(b['brand_name'], b['id'])
        for t in self.technicians_list:
            self.technician_combo.addItem(t['name'], t['id'])

    def _add_service(self):
        sid = self.service_combo.currentData()
        if not sid:
            self.show_warning_message("Select a service")
            return
        svc = next((s for s in self.services_list if s['id'] == sid), None)
        if not svc: return
        
        qty = self.service_qty_spin.value()
        rate = self.service_rate_spin.value() or svc['default_rate']
        amt = qty * rate
        
        row = self.services_table.rowCount()
        self.services_table.insertRow(row)
        self.services_table.setItem(row, 0, QTableWidgetItem(str(row+1)))
        self.services_table.setItem(row, 1, QTableWidgetItem(svc['service_name']))
        self.services_table.setItem(row, 2, QTableWidgetItem(str(qty)))
        self.services_table.setItem(row, 3, QTableWidgetItem(f"Rs {rate}"))
        self.services_table.setItem(row, 4, QTableWidgetItem(f"Rs {amt}"))
        
        btn = QPushButton("Delete")
        btn.setMinimumWidth(80)
        btn.setMinimumHeight(30)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setToolTip("Remove Item")
        btn.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 9pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """)

        # Create a container widget to hold and center the button
        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.addWidget(btn)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setAlignment(Qt.AlignCenter)

        btn.clicked.connect(lambda: self._delete_row(self.services_table, row, 'service'))
        self.services_table.setCellWidget(row, 5, container)
        self.services_table.setRowHeight(row, 45)

        self.invoice_items.append({'type': 'service', 'item_id': sid, 'name': svc['service_name'], 'qty': qty, 'rate': rate, 'amount': amt})
        self._update_summary()

    def _add_part(self):
        pid = self.part_combo.currentData()
        if not pid:
            self.show_warning_message("Select a part")
            return
        prt = next((p for p in self.parts_list if p['id'] == pid), None)
        if not prt: return
        
        qty = self.part_qty_spin.value()
        rate = self.part_rate_spin.value() or prt['default_rate']
        amt = qty * rate
        
        row = self.parts_table.rowCount()
        self.parts_table.insertRow(row)
        self.parts_table.setItem(row, 0, QTableWidgetItem(str(row+1)))
        self.parts_table.setItem(row, 1, QTableWidgetItem(prt['part_name']))
        self.parts_table.setItem(row, 2, QTableWidgetItem(str(qty)))
        self.parts_table.setItem(row, 3, QTableWidgetItem(f"Rs {rate}"))
        self.parts_table.setItem(row, 4, QTableWidgetItem(f"Rs {amt}"))
        
        btn = QPushButton("Delete")
        btn.setMinimumWidth(80)
        btn.setMinimumHeight(30)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setToolTip("Remove Item")
        btn.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 9pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """)

        # Create a container widget to hold and center the button
        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.addWidget(btn)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setAlignment(Qt.AlignCenter)

        btn.clicked.connect(lambda: self._delete_row(self.parts_table, row, 'part'))
        self.parts_table.setCellWidget(row, 5, container)
        self.parts_table.setRowHeight(row, 45)

        self.invoice_items.append({'type': 'part', 'item_id': pid, 'name': prt['part_name'], 'qty': qty, 'rate': rate, 'amount': amt})
        self._update_summary()

    def _delete_row(self, table, row, itype):
        table.removeRow(row)
        self.invoice_items = [i for i in self.invoice_items if not (i.get('row') == row and i.get('type') == itype)]
        self._update_summary()

    def _update_summary(self):
        import math
        subtotal = sum(item['amount'] for item in self.invoice_items)
        self.subtotal_label.setText(f"Rs {subtotal:,.0f}")
        
        gst = Decimal('0')
        if self.gst_checkbox.isChecked():
            rate = Decimal(self.gst_rate_combo.currentText().replace('%',''))
            gst = subtotal * (rate / 100)
        self.gst_amount_label.setText(f"Rs {gst:,.0f}")
        
        disc = Decimal('0')
        if self.discount_checkbox.isChecked():
            val = Decimal(str(self.discount_input.value()))
            if self.discount_type_combo.currentText() == "%":
                disc = subtotal * (val / 100)
            else:
                disc = val
        self.discount_amount_label.setText(f"Rs {disc:,.0f}")
        
        total = subtotal - disc + gst
        rounded = int(math.floor(float(total)))
        self.total_amount_label.setText(f"Rs {rounded:,}")
        self._calculate_balance()

    def _calculate_totals(self):
        self.gst_rate_combo.setEnabled(self.gst_checkbox.isChecked())
        self.discount_type_combo.setEnabled(self.discount_checkbox.isChecked())
        self.discount_input.setEnabled(self.discount_checkbox.isChecked())
        self._update_summary()

    def _calculate_balance(self):
        total_text = self.total_amount_label.text().replace("Rs ", "").replace(",", "")
        total = Decimal(total_text) if total_text else Decimal('0')
        advance = Decimal(str(self.advance_input.value()))
        balance = total - advance
        self.balance_label.setText(f"Rs {balance:,.0f}")
        if balance <= 0:
            self.balance_label.setStyleSheet("font-size: 24pt; font-weight: bold; color: #10b981;")
            self.payment_status_combo.setCurrentText('Paid')
        elif advance > 0:
            self.balance_label.setStyleSheet("font-size: 24pt; font-weight: bold; color: #f59e0b;")
            self.payment_status_combo.setCurrentText('Partial')
        else:
            self.balance_label.setStyleSheet("font-size: 24pt; font-weight: bold; color: #ef4444;")
        self._update_summary_text()

    def _update_summary_text(self):
        subtotal = sum(item['amount'] for item in self.invoice_items)
        total_text = self.total_amount_label.text().replace("Rs ", "").replace(",", "")
        total = Decimal(total_text) if total_text else Decimal('0')
        advance = Decimal(str(self.advance_input.value()))
        balance = total - advance
        
        html = f"""
        <div style='font-family: Arial, sans-serif; color: #1e293b;'>
            <h2 style='color: #0891b2; margin-bottom: 10px;'>ANSH AIRCOOL</h2>
            <hr style='border: 1px solid #cbd5e1;'>
            <table width='100%' style='border-collapse: collapse; margin-top: 10px;'>
                <tr style='background-color: #f1f5f9; font-weight: bold; color: #1e293b;'>
                    <th align='left' style='padding: 5px;'>Item Description</th>
                    <th align='right' style='padding: 5px;'>Amount</th>
                </tr>
        """
        
        for i in self.invoice_items:
            html += f"""
                <tr style='color: #334155;'>
                    <td style='padding: 5px; border-bottom: 1px solid #e2e8f0;'>
                        {i['name']} <small>(x{i['qty']})</small>
                    </td>
                    <td align='right' style='padding: 5px; border-bottom: 1px solid #e2e8f0;'>
                        Rs {i['amount']:,}
                    </td>
                </tr>
            """
            
        html += f"""
            </table>
            <div style='margin-top: 20px; text-align: right; color: #1e293b;'>
                <p><b>Subtotal:</b> Rs {subtotal:,}</p>
        """
        
        if self.gst_checkbox.isChecked():
            html += f"<p style='color: #0ea5e9;'><b>GST ({self.gst_rate_combo.currentText()}):</b> {self.gst_amount_label.text()}</p>"
        
        if self.discount_checkbox.isChecked():
            html += f"<p style='color: #22c55e;'><b>Discount:</b> {self.discount_amount_label.text()}</p>"
            
        html += f"""
                <h3 style='color: #0891b2; border-top: 2px solid #0891b2; padding-top: 10px;'>
                    TOTAL: Rs {total:,}
                </h3>
                <p style='color: #10b981;'><b>Advance:</b> Rs {advance:,}</p>
                <h3 style='color: #ef4444;'>BALANCE: Rs {balance:,}</h3>
            </div>
            <div style='margin-top: 20px; font-size: 10pt; color: #64748b;'>
                <p>Customer: {self.customer_name_input['input'].text()}</p>
                <p>Date: {datetime.now().strftime('%d-%m-%Y')}</p>
            </div>
        </div>
        """
        self.summary_text.setHtml(html)

    def _go_to_services_tab(self):
        if not self.customer_name_input['input'].text().strip():
            self.show_warning_message("Customer name required")
            return
        if not self.customer_mobile_input['input'].text().strip():
            self.show_warning_message("Mobile required")
            return
        self.tabs.setCurrentIndex(1)

    def _go_to_payment_tab(self):
        if not self.invoice_items:
            self.show_warning_message("Add services/parts")
            return
        self.tabs.setCurrentIndex(2)

    def _save_invoice(self):
        try:
            mobile = self.customer_mobile_input['input'].text().strip().replace('+91','').replace(' ','')
            if len(mobile) != 10:
                self.show_warning_message("Valid 10-digit mobile required")
                return
            if not self.invoice_items:
                self.show_warning_message("Add services/parts first")
                return

            from database.db_connection import DatabaseContext
            import math
            
            with DatabaseContext() as db:
                # Get or create customer
                existing = db.execute_query("SELECT id FROM customers WHERE mobile = %s AND is_active = TRUE", (mobile,), fetch_one=True)
                if existing:
                    cust_id = existing['id']
                    db.execute_query("UPDATE customers SET name = %s, address = %s, updated_at = NOW() WHERE id = %s", 
                        (self.customer_name_input['input'].text().strip(), self.customer_address_input.toPlainText().strip(), cust_id))
                else:
                    cust_id = db.execute_query("INSERT INTO customers (name, mobile, address, landmark, is_active) VALUES (%s, %s, %s, %s, TRUE)",
                        (self.customer_name_input['input'].text().strip(), mobile, self.customer_address_input.toPlainText().strip(), 
                         self.customer_landmark_input['input'].text().strip()))

                # Calculate totals
                subtotal = sum(item['amount'] for item in self.invoice_items)
                gst = Decimal('0')
                if self.gst_checkbox.isChecked():
                    gst = subtotal * Decimal(self.gst_rate_combo.currentText().replace('%','')) / 100
                disc = Decimal('0')
                if self.discount_checkbox.isChecked():
                    val = Decimal(str(self.discount_input.value()))
                    if self.discount_type_combo.currentText() == "%":
                        disc = subtotal * val / 100
                    else:
                        disc = val
                total = subtotal - disc + gst
                rounded = int(math.floor(float(total)))
                advance = Decimal(str(self.advance_input.value()))
                balance = rounded - advance

                # Generate professional invoice number
                from utils.formatters import Formatters
                inv_num = Formatters.generate_invoice_number(db)
                
                tech_id = self.technician_combo.currentData() if self.technician_combo.currentData() else None
                brand_id = self.ac_brand_combo.currentData() if self.ac_brand_combo.currentData() else None
                
                inv_id = db.execute_query("""
                    INSERT INTO invoices (invoice_number, customer_id, ac_brand_id, ac_type, ton_capacity, star_rating, inverter_type,
                    technician_id, subtotal, gst_percentage, gst_amount, total_amount, advance_payment, balance_amount,
                    payment_mode, payment_status, notes, is_active, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE, NOW())
                """, (inv_num, cust_id, brand_id, self.ac_type_combo.currentText(), self.ac_ton_combo.currentText(),
                      self.ac_star_combo.currentText(), self.ac_inverter_combo.currentText(), tech_id,
                      float(subtotal), float(gst > 0 and float(gst)/float(subtotal)*100 or 0), float(gst), float(rounded),
                      float(advance), float(balance), self.payment_mode_combo.currentText(), 
                      self.payment_status_combo.currentText(), self.notes_input.toPlainText().strip()))

                # Items
                for item in self.invoice_items:
                    db.execute_query("""
                        INSERT INTO invoice_items (invoice_id, item_type, service_id, part_id, quantity, rate, amount)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (inv_id, item['type'], item['item_id'] if item['type']=='service' else None,
                          item['item_id'] if item['type']=='part' else None, item['qty'], item['rate'], item['amount']))

                self.show_success_message(f"Invoice saved! ID: {inv_id}")
                self._clear_form()
        except Exception as e:
            self.show_error_message(f"Error: {str(e)}")
            import traceback
            traceback.print_exc()

    def _clear_form(self):
        self.customer_name_input['input'].clear()
        self.customer_mobile_input['input'].clear()
        self.customer_email_input['input'].clear()
        self.customer_landmark_input['input'].clear()
        self.customer_address_input.clear()
        self.services_table.setRowCount(0)
        self.parts_table.setRowCount(0)
        self.invoice_items = []
        self.subtotal_label.setText("Rs 0")
        self.gst_amount_label.setText("Rs 0")
        self.discount_amount_label.setText("Rs 0")
        self.total_amount_label.setText("Rs 0")
        self.balance_label.setText("Rs 0")
        self.advance_input.setValue(0)
        self.tabs.setCurrentIndex(0)

    def refresh_data(self):
        self.invoice_items = []
        self.services_table.setRowCount(0)
        self.parts_table.setRowCount(0)
        self.service_combo.clear()
        self.service_combo.addItem("-- Select --", "")
        self.part_combo.clear()
        self.part_combo.addItem("-- Select --", "")
        self.ac_brand_combo.clear()
        self.ac_brand_combo.addItem("Select Brand", "")
        self.technician_combo.clear()
        self.technician_combo.addItem("-- Select --", "")
        self.load_master_data()
