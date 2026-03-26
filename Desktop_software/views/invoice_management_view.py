"""
Invoice Management View - List, Edit, Download Invoices
Professional invoice management with search, filter, and actions
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea,
    QSizePolicy, QComboBox, QDateEdit, QMenu, QMessageBox, QFileDialog,
    QDialog, QDialogButtonBox, QFormLayout, QTextEdit
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QBrush, QColor
from datetime import datetime, timedelta

from utils.unified_theme import UnifiedTheme
from views.base_window import BaseView


class InvoiceManagementView(BaseView):
    """Invoice management view with list, edit, and download features"""

    def __init__(self):
        super().__init__()
        self.theme_manager = UnifiedTheme()
        self.invoice_list = []
        self.selected_invoice_id = None

        self._setup_ui()
        self.load_invoices()

    def update_theme_colors(self):
        """Update theme colors for proper dark theme support"""
        colors = self.theme_manager.get_colors()
        
        # Apply QPalette colors to this widget
        self.theme_manager.apply_palette(self)
        
        # Apply stylesheet
        self.setStyleSheet(self.theme_manager.get_main_stylesheet())
        
        # Apply theme directly to table widget for proper alternating colors
        if hasattr(self, 'invoice_table'):
            self.theme_manager.apply_table_theme(self.invoice_table)
        
        # Force refresh
        self.load_invoices()

    def _setup_ui(self):
        """Setup invoice management UI - THEME SUPPORT"""
        colors = self.theme_manager.get_colors()
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Header
        title_label = QLabel("INVOICE MANAGEMENT")
        title_label.setObjectName("headingLabel")
        title_label.setStyleSheet(f"""
            font-size: 20pt;
            font-weight: bold;
            color: {colors['fg']};
        """)
        main_layout.addWidget(title_label)

        subtitle_label = QLabel("View, Edit, Download and Manage Invoices")
        subtitle_label.setObjectName("subheadingLabel")
        subtitle_label.setStyleSheet(f"""
            font-size: 10pt;
            color: {colors['muted']};
        """)
        main_layout.addWidget(subtitle_label)

        # Search and Filters
        self._create_filters(main_layout)

        # Invoice Table
        self._create_invoice_table(main_layout)

        # Action Buttons
        self._create_action_buttons(main_layout)

    def _create_filters(self, layout):
        """Create search and filter controls - THEME SUPPORT"""
        colors = self.theme_manager.get_colors()
        
        filter_frame = QFrame()
        filter_frame.setObjectName("cardFrame")
        filter_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {colors['card_bg']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
            }}
        """)
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(15, 15, 15, 15)
        filter_layout.setSpacing(10)

        # Search
        search_label = QLabel("🔍 Search:")
        search_label.setStyleSheet(f"font-weight: bold; color: {colors['fg']};")
        filter_layout.addWidget(search_label)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by Invoice No, Customer Name, or Mobile...")
        self.search_input.setMinimumWidth(300)
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {colors['bg']};
                color: {colors['fg']};
                border: 1px solid {colors['border']};
                border-radius: 6px;
                padding: 8px 12px;
            }}
            QLineEdit:focus {{
                border: 2px solid {colors['primary']};
            }}
        """)
        self.search_input.textChanged.connect(self.load_invoices)
        filter_layout.addWidget(self.search_input)

        # Date Filter
        from_label = QLabel("From:")
        from_label.setStyleSheet(f"font-weight: bold; color: {colors['fg']};")
        filter_layout.addWidget(from_label)
        
        self.from_date = QDateEdit()
        self.from_date.setDate(QDate.currentDate().addMonths(-1))
        self.from_date.setCalendarPopup(True)
        self.from_date.setDisplayFormat("dd-MM-yyyy")
        self.from_date.setStyleSheet(f"""
            QDateEdit {{
                background-color: {colors['bg']};
                color: {colors['fg']};
                border: 1px solid {colors['border']};
                border-radius: 6px;
                padding: 8px 12px;
            }}
            QDateEdit::drop-down {{
                border: none;
                width: 30px;
            }}
        """)
        self.from_date.dateChanged.connect(self.load_invoices)
        filter_layout.addWidget(self.from_date)

        to_label = QLabel("To:")
        to_label.setStyleSheet(f"font-weight: bold; color: {colors['fg']};")
        filter_layout.addWidget(to_label)
        
        self.to_date = QDateEdit()
        self.to_date.setDate(QDate.currentDate())
        self.to_date.setCalendarPopup(True)
        self.to_date.setDisplayFormat("dd-MM-yyyy")
        self.to_date.setStyleSheet(f"""
            QDateEdit {{
                background-color: {colors['bg']};
                color: {colors['fg']};
                border: 1px solid {colors['border']};
                border-radius: 6px;
                padding: 8px 12px;
            }}
            QDateEdit::drop-down {{
                border: none;
                width: 30px;
            }}
        """)
        self.to_date.dateChanged.connect(self.load_invoices)
        filter_layout.addWidget(self.to_date)

        # Status Filter
        self.status_combo = QComboBox()
        self.status_combo.addItems(["All Status", "Paid", "Partial", "Pending"])
        self.status_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {colors['bg']};
                color: {colors['fg']};
                border: 1px solid {colors['border']};
                border-radius: 6px;
                padding: 8px 12px;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {colors['bg']};
                color: {colors['fg']};
                border: 1px solid {colors['border']};
                selection-background-color: {colors['primary']};
            }}
        """)
        self.status_combo.currentTextChanged.connect(self.load_invoices)
        filter_layout.addWidget(self.status_combo)

        filter_layout.addStretch()
        layout.addWidget(filter_frame)

    def _create_invoice_table(self, layout):
        """Create invoice table"""
        self.invoice_table = QTableWidget()
        self.invoice_table.setColumnCount(9)
        self.invoice_table.setHorizontalHeaderLabels([
            'ID', 'Invoice No', 'Customer', 'Mobile', 'Amount', 'Advance', 'Balance', 'Status', 'Date'
        ])
        self.invoice_table.setShowGrid(True)
        self.invoice_table.setAlternatingRowColors(True)
        self.invoice_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.invoice_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.invoice_table.verticalHeader().setVisible(False)
        self.invoice_table.verticalHeader().setDefaultSectionSize(40)

        # Column widths
        header = self.invoice_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(8, QHeaderView.ResizeToContents)

        # Style table - THEME SUPPORT (using global theme, minimal local overrides)
        colors = self.theme_manager.get_colors()

        self.invoice_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {colors['card_bg']};
                color: {colors['fg']};
                border: 1px solid {colors['border']};
                border-radius: 6px;
                gridline-color: {colors['border']};
                alternate-background-color: {colors['alt_row']};
            }}
            QTableWidget::item {{
                padding: 8px;
                border: 1px solid {colors['border']};
                color: {colors['fg']};
            }}
            QTableWidget::item:hover {{
                background-color: {colors['hover']};
                color: {colors['fg']};
            }}
            QTableWidget::item:selected {{
                background-color: {colors['primary']};
                color: {colors['bg']};
            }}
            QTableWidget::item:alternate {{
                background-color: {colors['alt_row']};
                color: {colors['fg']};
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

        # Double click to edit
        self.invoice_table.cellDoubleClicked.connect(self.edit_selected_invoice)

        # Context menu
        self.invoice_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.invoice_table.customContextMenuRequested.connect(self.show_context_menu)

        layout.addWidget(self.invoice_table)

        # Status label - THEME SUPPORT
        colors = self.theme_manager.get_colors()
        
        self.status_label = QLabel("No invoices found")
        self.status_label.setStyleSheet(f"color: {colors['muted']}; font-size: 10pt;")
        layout.addWidget(self.status_label)

    def _create_action_buttons(self, layout):
        """Create action buttons - Professional (No Emojis)"""
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        # Edit button
        edit_btn = QPushButton("Edit Invoice")
        edit_btn.setObjectName("primaryButton")
        edit_btn.setStyleSheet("padding: 10px 20px; font-size: 11pt;")
        edit_btn.clicked.connect(self.edit_selected_invoice)
        btn_layout.addWidget(edit_btn)

        # Download button
        download_btn = QPushButton("Download Invoice")
        download_btn.setObjectName("successButton")
        download_btn.setStyleSheet("padding: 10px 20px; font-size: 11pt;")
        download_btn.clicked.connect(self.download_selected_invoice)
        btn_layout.addWidget(download_btn)

        # WhatsApp Share button
        whatsapp_btn = QPushButton("Share on WhatsApp")
        whatsapp_green = "#25D366"
        whatsapp_dark = "#128C7E"
        whatsapp_darker = "#075E54"
        whatsapp_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {whatsapp_green};
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 11pt;
                font-weight: bold;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {whatsapp_dark};
            }}
            QPushButton:pressed {{
                background-color: {whatsapp_darker};
            }}
        """)
        whatsapp_btn.clicked.connect(self.share_invoice_whatsapp)
        btn_layout.addWidget(whatsapp_btn)

        # Delete button
        delete_btn = QPushButton("Delete Invoice")
        delete_btn.setObjectName("dangerButton")
        delete_btn.setStyleSheet("padding: 10px 20px; font-size: 11pt;")
        delete_btn.clicked.connect(self.delete_selected_invoice)
        btn_layout.addWidget(delete_btn)

        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setObjectName("secondaryButton")
        refresh_btn.setStyleSheet("padding: 10px 20px; font-size: 11pt;")
        refresh_btn.clicked.connect(self.load_invoices)
        btn_layout.addWidget(refresh_btn)

        layout.addLayout(btn_layout)

    def load_invoices(self):
        """Load invoices from database"""
        try:
            from database.db_connection import DatabaseContext

            with DatabaseContext() as db:
                # Build query
                query = """
                    SELECT 
                        i.id, i.invoice_number, 
                        c.name as customer_name, c.mobile,
                        i.total_amount, i.advance_payment, i.balance_amount,
                        i.payment_status, DATE(i.created_at) as invoice_date
                    FROM invoices i
                    JOIN customers c ON i.customer_id = c.id
                    WHERE i.is_active = TRUE
                """

                params = []

                # Search filter
                search_term = self.search_input.text().strip()
                if search_term:
                    query += " AND (i.invoice_number LIKE %s OR c.name LIKE %s OR c.mobile LIKE %s)"
                    params.extend([f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"])

                # Date filter
                from_date = self.from_date.date().toString("yyyy-MM-dd")
                to_date = self.to_date.date().toString("yyyy-MM-dd")
                query += " AND DATE(i.created_at) BETWEEN %s AND %s"
                params.extend([from_date, to_date])

                # Status filter
                status = self.status_combo.currentText()
                if status != "All Status":
                    query += " AND i.payment_status = %s"
                    params.append(status)

                query += " ORDER BY i.created_at DESC"

                # Execute query
                results = db.execute_query(query, params, fetch_all=True)
                self.invoice_list = results if results else []

                # Update table
                self.invoice_table.setRowCount(0)
                for invoice in self.invoice_list:
                    row = self.invoice_table.rowCount()
                    self.invoice_table.insertRow(row)

                    # Status color
                    status_color = "#10b981" if invoice['payment_status'] == 'Paid' else \
                                   "#f59e0b" if invoice['payment_status'] == 'Partial' else "#ef4444"

                    items = [
                        str(invoice['id']),
                        invoice['invoice_number'],
                        invoice['customer_name'],
                        invoice['mobile'],
                        f"₹{invoice['total_amount']:,.0f}",
                        f"₹{invoice['advance_payment']:,.0f}",
                        f"₹{invoice['balance_amount']:,.0f}",
                        invoice['payment_status'],
                        invoice['invoice_date'].strftime("%d-%m-%Y")
                    ]

                    for col, text in enumerate(items):
                        item = QTableWidgetItem(text)
                        item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                        if col == 7:  # Status column
                            # Professional subtle colors (theme-aware)
                            if text == 'Paid':
                                bg_color = "#d1fae5"  # Light green
                                fg_color = "#065f46"  # Dark green text
                            elif text == 'Partial':
                                bg_color = "#fef3c7"  # Light amber
                                fg_color = "#92400e"  # Dark amber text
                            else:  # Pending
                                bg_color = "#fee2e2"  # Light red
                                fg_color = "#991b1b"  # Dark red text

                            item.setBackground(QBrush(QColor(f"{bg_color}")))
                            item.setForeground(QBrush(QColor(f"{fg_color}")))
                        self.invoice_table.setItem(row, col, item)

                self.status_label.setText(f"Showing {len(self.invoice_list)} invoices")

        except Exception as e:
            self.show_error_message(f"Error loading invoices: {str(e)}")
            print(f"Error: {str(e)}")

    def show_context_menu(self, pos):
        """Show context menu on right-click - Professional (No Emojis)"""
        menu = QMenu(self)
        menu.addAction("Edit Invoice", self.edit_selected_invoice)
        menu.addAction("Download Invoice", self.download_selected_invoice)
        menu.addAction("Share on WhatsApp", self.share_invoice_whatsapp)
        menu.addSeparator()
        menu.addAction("Delete Invoice", self.delete_selected_invoice)
        menu.exec(self.invoice_table.viewport().mapToGlobal(pos))

    def get_selected_invoice(self):
        """Get selected invoice data"""
        selected_rows = self.invoice_table.selectionModel().selectedRows()
        if not selected_rows:
            self.show_warning_message("Please select an invoice first")
            return None

        row = selected_rows[0].row()
        invoice_id = int(self.invoice_table.item(row, 0).text())

        # Find invoice in list
        for invoice in self.invoice_list:
            if invoice['id'] == invoice_id:
                return invoice

        return None

    def edit_selected_invoice(self):
        """Edit selected invoice"""
        invoice = self.get_selected_invoice()
        if not invoice:
            return

        # Open invoice in edit mode
        try:
            from database.db_connection import DatabaseContext
            from views.edit_invoice_dialog import EditInvoiceDialog

            # Get full invoice data
            with DatabaseContext() as db:
                query = """
                    SELECT i.*, c.name, c.mobile, c.email, c.address, c.landmark,
                           ab.brand_name, i.ac_type, i.star_rating, i.ton_capacity,
                           i.inverter_type, i.payment_mode, i.payment_status, i.notes,
                           i.advance_payment, i.gst_percentage,
                           t.name as technician_name
                    FROM invoices i
                    JOIN customers c ON i.customer_id = c.id
                    LEFT JOIN ac_brands ab ON i.ac_brand_id = ab.id
                    LEFT JOIN technicians t ON i.technician_id = t.id
                    WHERE i.id = %s
                """
                invoice_data = db.execute_query(query, (invoice['id'],), fetch_one=True)

                if invoice_data:
                    # Open edit dialog
                    dialog = EditInvoiceDialog(self, invoice_data)
                    
                    if dialog.exec():
                        # Save changes to database
                        self._save_edited_invoice(invoice_data['id'], dialog)
                    
        except Exception as e:
            self.show_error_message(f"Error opening invoice: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def _save_edited_invoice(self, invoice_id, dialog):
        """Save edited invoice to database"""
        try:
            from database.db_connection import DatabaseContext
            from decimal import Decimal

            with DatabaseContext() as db:
                # Start transaction
                db.connection.autocommit = False
                try:
                    # Get customer_id first (don't rely on mobile)
                    customer_query = """
                        SELECT id FROM customers WHERE mobile = %s LIMIT 1
                    """
                    customer_result = db.execute_query(customer_query, (dialog.customer_mobile_input.text().strip(),), fetch_one=True)
                    
                    if not customer_result:
                        raise Exception("Customer not found with this mobile number")
                    
                    customer_id = customer_result['id']

                    # Calculate totals from items
                    subtotal = sum(item['amount'] for item in dialog.invoice_items)
                    subtotal_decimal = Decimal(str(subtotal))

                    # Calculate GST
                    gst_amount = Decimal('0.00')
                    if dialog.gst_checkbox.isChecked():
                        gst_rate_text = dialog.gst_rate_combo.currentText()
                        gst_rate = Decimal(gst_rate_text.replace('%', ''))
                        gst_amount = subtotal_decimal * (gst_rate / Decimal('100'))

                    # Calculate total and balance
                    total = subtotal_decimal + gst_amount
                    advance = Decimal(str(dialog.advance_input.value()))
                    balance = total - advance

                    # Parse GST rate
                    gst_rate_str = dialog.gst_rate_combo.currentText().replace('%', '')
                    gst_rate = float(gst_rate_str) if dialog.gst_checkbox.isChecked() else 0.0

                    # Update invoice
                    query = """
                        UPDATE invoices SET
                            customer_id = %s,
                            ac_brand_id = (SELECT id FROM ac_brands WHERE brand_name = %s LIMIT 1),
                            ac_type = %s,
                            star_rating = %s,
                            ton_capacity = %s,
                            inverter_type = %s,
                            payment_mode = %s,
                            payment_status = %s,
                            notes = %s,
                            advance_payment = %s,
                            gst_percentage = %s,
                            gst_amount = %s,
                            subtotal = %s,
                            total_amount = %s,
                            balance_amount = %s,
                            updated_at = NOW()
                        WHERE id = %s
                    """

                    db.execute_query(query, (
                        customer_id,
                        dialog.ac_brand_combo.currentText(),
                        dialog.ac_type_combo.currentText(),
                        dialog.ac_star_combo.currentText(),
                        dialog.ac_ton_combo.currentText(),
                        dialog.ac_inverter_combo.currentText(),
                        dialog.payment_mode_combo.currentText(),
                        dialog.payment_status_combo.currentText(),
                        dialog.notes_input.toPlainText().strip(),
                        float(dialog.advance_input.value()),
                        gst_rate,
                        float(gst_amount),
                        float(subtotal_decimal),
                        float(total),
                        float(balance),
                        invoice_id
                    ))

                    # Update customer details using customer_id (not mobile)
                    customer_update_query = """
                        UPDATE customers SET
                            name = %s,
                            mobile = %s,
                            email = %s,
                            address = %s,
                            landmark = %s,
                            updated_at = NOW()
                        WHERE id = %s
                    """
                    db.execute_query(customer_update_query, (
                        dialog.customer_name_input.text().strip(),
                        dialog.customer_mobile_input.text().strip(),
                        dialog.customer_email_input.text().strip(),
                        dialog.customer_address_input.toPlainText().strip(),
                        dialog.customer_landmark_input.text().strip(),
                        customer_id
                    ))

                    # Delete old invoice items
                    db.execute_query("DELETE FROM invoice_items WHERE invoice_id = %s", (invoice_id,))

                    # Insert new invoice items
                    for item in dialog.invoice_items:
                        insert_query = """
                            INSERT INTO invoice_items (invoice_id, service_id, part_id, quantity, rate, amount)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """
                        db.execute_query(insert_query, (
                            invoice_id,
                            item.get('service_id'),
                            item.get('part_id'),
                            item['quantity'],
                            item['rate'],
                            item['amount']
                        ))

                    # Commit transaction
                    db.connection.commit()
                    self.show_success_message("Invoice updated successfully!")
                    self.load_invoices()  # Refresh list

                except Exception as e:
                    # Rollback on error
                    db.connection.rollback()
                    raise e

        except Exception as e:
            self.show_error_message(f"Error saving changes: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def show_invoice_details(self, invoice):
        """Show complete invoice details in a dialog - Professional Layout"""
        try:
            from database.db_connection import DatabaseContext

            with DatabaseContext() as db:
                # Get complete invoice data
                query = """
                    SELECT i.*, c.name as customer_name, c.mobile, c.email, c.address, c.landmark,
                           ab.brand_name as ac_brand, i.ac_type, i.star_rating, i.ton_capacity as ac_capacity,
                           i.inverter_type, t.name as technician_name, t.mobile as technician_mobile
                    FROM invoices i
                    JOIN customers c ON i.customer_id = c.id
                    LEFT JOIN ac_brands ab ON i.ac_brand_id = ab.id
                    LEFT JOIN technicians t ON i.technician_id = t.id
                    WHERE i.id = %s
                """
                invoice_data = db.execute_query(query, (invoice['id'],), fetch_one=True)

                # Get invoice items
                items_query = """
                    SELECT ii.*, s.service_name, p.part_name
                    FROM invoice_items ii
                    LEFT JOIN services s ON ii.service_id = s.id
                    LEFT JOIN parts p ON ii.part_id = p.id
                    WHERE ii.invoice_id = %s
                """
                items = db.execute_query(items_query, (invoice['id'],), fetch_all=True)

            dialog = QDialog(self)
            dialog.setWindowTitle(f"Invoice Details - {invoice['invoice_number']}")
            dialog.setMinimumSize(700, 600)

            layout = QVBoxLayout(dialog)
            layout.setSpacing(15)

            # Title
            title = QLabel(f"Invoice: {invoice['invoice_number']}")
            title.setStyleSheet("font-size: 18pt; font-weight: bold; color: #1e293b;")
            layout.addWidget(title)

            # Scroll area for content
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setStyleSheet("border: none; background: transparent;")

            content_widget = QWidget()
            content_layout = QVBoxLayout(content_widget)
            content_layout.setSpacing(12)

            # Customer Details
            customer_group = QLabel("<b>CUSTOMER DETAILS</b>")
            customer_group.setStyleSheet("font-size: 11pt; font-weight: bold; background: #f0f0f0; padding: 5px;")
            content_layout.addWidget(customer_group)

            customer_details = f"""
            <table style="width: 100%; font-size: 9pt;">
                <tr><td style="width: 100px;"><b>Name:</b></td><td>{invoice_data.get('customer_name', 'N/A')}</td></tr>
                <tr><td><b>Mobile:</b></td><td>{invoice_data.get('mobile', 'N/A')}</td></tr>
                <tr><td><b>Email:</b></td><td>{invoice_data.get('email', 'N/A') or 'N/A'}</td></tr>
                <tr><td><b>Address:</b></td><td>{invoice_data.get('address', 'N/A') or 'N/A'}</td></tr>
            </table>
            """
            content_layout.addWidget(QLabel(customer_details))

            # Service & AC Details
            service_group = QLabel("<b>SERVICE & AC DETAILS</b>")
            service_group.setStyleSheet("font-size: 11pt; font-weight: bold; background: #f0f0f0; padding: 5px;")
            content_layout.addWidget(service_group)

            service_details = f"""
            <table style="width: 100%; font-size: 9pt;">
                <tr><td style="width: 120px;"><b>Technician:</b></td><td>{invoice_data.get('technician_name', 'N/A')} ({invoice_data.get('technician_mobile', 'N/A')})</td></tr>
                <tr><td><b>AC Brand:</b></td><td>{invoice_data.get('ac_brand', 'N/A') or 'N/A'}</td></tr>
                <tr><td><b>AC Type:</b></td><td>{invoice_data.get('ac_type', 'N/A')}</td></tr>
                <tr><td><b>Capacity:</b></td><td>{invoice_data.get('ac_capacity', 'N/A')}</td></tr>
                <tr><td><b>Inverter:</b></td><td>{invoice_data.get('inverter_type', 'N/A')}</td></tr>
            </table>
            """
            content_layout.addWidget(QLabel(service_details))

            # Items
            items_group = QLabel("<b>ITEMS</b>")
            items_group.setStyleSheet("font-size: 11pt; font-weight: bold; background: #f0f0f0; padding: 5px;")
            content_layout.addWidget(items_group)

            if items:
                items_text = """
                <table style="width: 100%; font-size: 9pt; border-collapse: collapse;">
                    <tr style="background: #e0e0e0;">
                        <td style="padding: 5px; border: 1px solid #ccc;"><b>Type</b></td>
                        <td style="padding: 5px; border: 1px solid #ccc;"><b>Name</b></td>
                        <td style="padding: 5px; border: 1px solid #ccc;"><b>Qty</b></td>
                        <td style="padding: 5px; border: 1px solid #ccc;"><b>Rate</b></td>
                        <td style="padding: 5px; border: 1px solid #ccc;"><b>Amount</b></td>
                    </tr>
                """
                for item in items:
                    item_type = item.get('item_type', 'N/A')
                    item_name = item.get('service_name') or item.get('part_name') or 'N/A'
                    qty = item.get('quantity', 0)
                    rate = float(item.get('rate', 0))
                    amount = float(item.get('amount', 0))
                    items_text += f"""
                    <tr>
                        <td style="padding: 5px; border: 1px solid #ccc;">{item_type}</td>
                        <td style="padding: 5px; border: 1px solid #ccc;">{item_name}</td>
                        <td style="padding: 5px; border: 1px solid #ccc;">{qty}</td>
                        <td style="padding: 5px; border: 1px solid #ccc;">Rs. {rate:,.2f}</td>
                        <td style="padding: 5px; border: 1px solid #ccc;">Rs. {amount:,.2f}</td>
                    </tr>
                    """
                items_text += "</table>"
                content_layout.addWidget(QLabel(items_text))
            else:
                content_layout.addWidget(QLabel("No items"))

            # Payment Summary
            payment_group = QLabel("<b>PAYMENT SUMMARY</b>")
            payment_group.setStyleSheet("font-size: 11pt; font-weight: bold; background: #f0f0f0; padding: 5px;")
            content_layout.addWidget(payment_group)

            total = float(invoice_data.get('total_amount', 0))
            advance = float(invoice_data.get('advance_payment', 0))
            balance = float(invoice_data.get('balance_amount', 0))

            payment_details = f"""
            <table style="width: 100%; font-size: 9pt;">
                <tr><td style="width: 120px;"><b>Total Amount:</b></td><td style="text-align: right;"><b>Rs. {total:,.2f}</b></td></tr>
                <tr><td><b>Advance Paid:</b></td><td style="text-align: right;">Rs. {advance:,.2f}</td></tr>
                <tr><td><b>Balance Due:</b></td><td style="text-align: right; color: #d97706;"><b>Rs. {balance:,.2f}</b></td></tr>
                <tr><td><b>Payment Status:</b></td><td>{invoice_data.get('payment_status', 'N/A')}</td></tr>
                <tr><td><b>Payment Mode:</b></td><td>{invoice_data.get('payment_mode', 'N/A')}</td></tr>
            </table>
            """
            content_layout.addWidget(QLabel(payment_details))

            # Notes
            notes = invoice_data.get('notes', '')
            if notes:
                notes_group = QLabel("<b>NOTES</b>")
                notes_group.setStyleSheet("font-size: 11pt; font-weight: bold; background: #f0f0f0; padding: 5px;")
                content_layout.addWidget(notes_group)
                content_layout.addWidget(QLabel(notes))

            scroll.setWidget(content_widget)
            layout.addWidget(scroll)

            # Buttons
            btn_box = QDialogButtonBox()
            btn_box.setStandardButtons(QDialogButtonBox.Ok)
            btn_box.setStyleSheet("padding: 10px;")
            btn_box.accepted.connect(dialog.accept)
            layout.addWidget(btn_box)

            dialog.exec()

        except Exception as e:
            self.show_error_message(f"Error showing invoice details: {str(e)}")
            import traceback
            traceback.print_exc()

    def download_selected_invoice(self):
        """Download selected invoice as PDF"""
        invoice = self.get_selected_invoice()
        if not invoice:
            return

        # Create filename with customer name and invoice number
        customer_name = invoice.get('customer_name', 'Customer')
        invoice_number = invoice['invoice_number']
        # Sanitize filename - replace invalid characters with underscore
        safe_customer_name = "".join(c if c.isalnum() or c in ' -_' else '_' for c in customer_name)
        safe_filename = f"{safe_customer_name}_{invoice_number}.pdf"

        # Ask for save location
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Invoice",
            safe_filename,
            "PDF Files (*.pdf);;Text Files (*.txt)"
        )

        if file_path:
            try:
                if file_path.endswith('.txt'):
                    # Save as text
                    self.save_invoice_as_text(invoice, file_path)
                else:
                    # Save as PDF (simplified version)
                    self.save_invoice_as_pdf(invoice, file_path)

                self.show_success_message(f"Invoice saved to: {file_path}")

            except Exception as e:
                self.show_error_message(f"Error saving invoice: {str(e)}")
    
    def save_invoice_as_text(self, invoice, file_path):
        """Save invoice as text file"""
        from database.db_connection import DatabaseContext
        
        with DatabaseContext() as db:
            # Get invoice items
            items_query = """
                SELECT ii.*, s.service_name, p.part_name
                FROM invoice_items ii
                LEFT JOIN services s ON ii.service_id = s.id
                LEFT JOIN parts p ON ii.part_id = p.id
                WHERE ii.invoice_id = %s
            """
            items = db.execute_query(items_query, (invoice['id'],), fetch_all=True)
            
            # Write to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write(f"INVOICE - {invoice['invoice_number']}\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"Customer: {invoice['customer_name']}\n")
                f.write(f"Mobile: {invoice['mobile']}\n")
                f.write(f"Date: {invoice['invoice_date'].strftime('%d-%m-%Y')}\n\n")
                f.write("-" * 60 + "\n")
                f.write("ITEMS:\n")
                f.write("-" * 60 + "\n")
                
                if items:
                    for item in items:
                        item_name = item['service_name'] or item['part_name'] or 'N/A'
                        f.write(f"  {item_name}\n")
                        f.write(f"    Qty: {item['quantity']} x ₹{item['rate']:,.2f} = ₹{item['amount']:,.2f}\n")
                
                f.write("\n" + "-" * 60 + "\n")
                f.write(f"Total Amount:  ₹{invoice['total_amount']:,.2f}\n")
                f.write(f"Advance Paid:  ₹{invoice['advance_payment']:,.2f}\n")
                f.write(f"BALANCE DUE:   ₹{invoice['balance_amount']:,.2f}\n")
                f.write(f"Payment Status: {invoice['payment_status']}\n")
                f.write("\n" + "=" * 60 + "\n")
                f.write("Thank you for your business!\n")
                f.write("Ansh Air Cool - Premium AC Services\n")
                f.write("📞 9918331262\n")
    
    def save_invoice_as_pdf(self, invoice, file_path):
        """Save invoice as professional PDF using PDFGenerator"""
        from utils.pdf_generator import PDFGenerator
        from database.db_connection import DatabaseContext
        import os

        with DatabaseContext() as db:
            # Get complete invoice data with ALL required fields
            query = """
                SELECT i.*, c.name as customer_name, c.mobile as customer_mobile,
                       c.email as customer_email, c.address as customer_address, c.landmark,
                       ab.brand_name as ac_brand, i.ac_type, i.star_rating, i.ton_capacity as ac_capacity,
                       i.inverter_type, i.technician_id, i.payment_mode,
                       i.subtotal, i.gst_percentage as cgst_rate, i.gst_amount,
                       i.total_amount, i.advance_payment, i.balance_amount,
                       i.payment_status, i.notes, i.created_at, i.updated_at
                FROM invoices i
                JOIN customers c ON i.customer_id = c.id
                LEFT JOIN ac_brands ab ON i.ac_brand_id = ab.id
                WHERE i.id = %s
            """
            invoice_data = db.execute_query(query, (invoice['id'],), fetch_one=True)
            
            if not invoice_data:
                raise Exception("Invoice data not found")

            # Get invoice items
            items_query = """
                SELECT ii.*, s.service_name, p.part_name
                FROM invoice_items ii
                LEFT JOIN services s ON ii.service_id = s.id
                LEFT JOIN parts p ON ii.part_id = p.id
                WHERE ii.invoice_id = %s
            """
            items = db.execute_query(items_query, (invoice['id'],), fetch_all=True)

            # Get shop data
            shop_query = """
                SELECT shop_name, address, phone, email, '' as footer_message
                FROM shop_details LIMIT 1
            """
            shop_data = db.execute_query(shop_query, fetch_one=True)
            
            if not shop_data:
                shop_data = {
                    'shop_name': 'ANSH AIR COOL',
                    'address': 'Shop Address Not Provided',
                    'phone': 'N/A',
                    'email': 'N/A',
                    'footer_message': 'Thank you for your business!'
                }
            
            # Map 'phone' to 'mobile' for PDF generator compatibility
            if shop_data:
                shop_data['mobile'] = shop_data.get('phone') or 'N/A'

            # Get technician name and mobile
            technician_name = 'N/A'
            technician_mobile = 'N/A'
            if invoice_data.get('technician_id'):
                tech_query = "SELECT name, mobile FROM technicians WHERE id = %s"
                tech_result = db.execute_query(tech_query, (invoice_data['technician_id'],), fetch_one=True)
                if tech_result:
                    technician_name = tech_result['name'] or 'N/A'
                    technician_mobile = tech_result['mobile'] or 'N/A'

            # Prepare invoice data for PDF generator - FIXED MAPPING
            pdf_invoice_data = {
                # Invoice Basics
                'invoice_no': invoice_data['invoice_number'],
                'invoice_date': invoice_data['created_at'].strftime('%d-%m-%Y') if invoice_data.get('created_at') else datetime.now().strftime('%d-%m-%Y'),
                'due_date': invoice_data['updated_at'].strftime('%d-%m-%Y') if invoice_data.get('updated_at') else 'N/A',
                'invoice_type': 'Regular',  # Default, can be extended for AMC/Installation

                # Payment Details - CRITICAL: Map correctly from database
                'payment_mode': invoice_data.get('payment_mode', 'N/A'),
                'payment_status': invoice_data.get('payment_status', 'Pending'),

                # Customer Details
                'customer_name': invoice_data.get('customer_name', 'N/A'),
                'customer_address': invoice_data.get('customer_address') or 'N/A',
                'customer_mobile': invoice_data.get('customer_mobile', 'N/A'),
                'customer_email': invoice_data.get('customer_email') or 'N/A',
                'landmark': invoice_data.get('landmark') or '',

                # AC Details - Map from database fields
                'ac_brand': invoice_data.get('ac_brand') or 'N/A',
                'ac_type': invoice_data.get('ac_type') or 'N/A',
                'ac_ton': invoice_data.get('ac_capacity') or 'N/A',
                'ac_star': invoice_data.get('star_rating') or 'N/A',
                'ac_inverter': invoice_data.get('inverter_type') or 'N/A',
                'ac_gas': 'N/A',  # Not stored in database currently
                'ac_serial': 'N/A',  # Not stored in database currently

                # Service Details
                'technician_name': technician_name,
                'technician_mobile': technician_mobile,
                'service_date': invoice_data['created_at'].strftime('%d-%m-%Y') if invoice_data.get('created_at') else 'N/A',
                'service_type': 'AC Service',

                # Items with GST (HSN removed as requested)
                'items': [
                    {
                        'service_name': item.get('service_name'),
                        'part_name': item.get('part_name'),
                        'description': item.get('service_name') or item.get('part_name') or 'N/A',
                        'quantity': item.get('quantity', 1),
                        'rate': float(item.get('rate', 0)),
                        'gst_percent': float(invoice_data.get('gst_percentage', 18)),
                        'amount': float(item.get('amount', 0))
                    }
                    for item in items
                ] if items else [],

                # Payment Summary - CRITICAL: Map correctly
                'subtotal': float(invoice_data.get('subtotal', 0)),
                'cgst_rate': float(invoice_data.get('gst_percentage', 9)),
                'cgst_amount': float(invoice_data.get('gst_amount', 0)),
                'sgst_rate': float(invoice_data.get('gst_percentage', 9)),  # Same as CGST
                'sgst_amount': float(invoice_data.get('gst_amount', 0)),  # Same as CGST
                'igst_amount': 0,  # Not applicable currently
                'total': float(invoice_data.get('total_amount', 0)),
                'amount_paid': float(invoice_data.get('advance_payment', 0)),  # Map advance_payment -> amount_paid
                'balance_due': float(invoice_data.get('balance_amount', 0)),

                # Notes
                'notes': invoice_data.get('notes') or 'Thank you for your business!'
            }

            # Generate professional PDF
            pdf_generator = PDFGenerator()
            
            # Ensure exports directory exists
            os.makedirs(os.path.dirname(file_path) if os.path.dirname(file_path) else '.', exist_ok=True)
            
            pdf_generator.generate_invoice(pdf_invoice_data, shop_data, file_path)

    def share_invoice_whatsapp(self):
        """🆕 Share invoice PDF via WhatsApp - PDF Download + WhatsApp Text"""
        invoice = self.get_selected_invoice()
        if not invoice:
            return

        try:
            from database.db_connection import DatabaseContext
            from utils.whatsapp_helper import WhatsAppHelper
            from utils.whatsapp_messages import format_message
            from utils.pdf_invoice_generator import PDFInvoiceGenerator
            from PySide6.QtWidgets import QMessageBox
            import webbrowser
            import os

            with DatabaseContext() as db:
                # Get complete invoice data
                query = """
                    SELECT i.*, c.name as customer_name, c.mobile as customer_mobile,
                           c.address as customer_address,
                           i.total_amount, i.advance_payment, i.balance_amount,
                           i.payment_mode, i.payment_status, DATE(i.created_at) as invoice_date
                    FROM invoices i
                    JOIN customers c ON i.customer_id = c.id
                    WHERE i.id = %s
                """
                invoice_data = db.execute_query(query, (invoice['id'],), fetch_one=True)

                if not invoice_data:
                    self.show_error_message("Invoice data not found")
                    return

                # Get invoice items
                items_query = """
                    SELECT ii.*, s.service_name
                    FROM invoice_items ii
                    LEFT JOIN services s ON ii.service_id = s.id
                    WHERE ii.invoice_id = %s AND ii.item_type = 'service'
                """
                items = db.execute_query(items_query, (invoice['id'],), fetch_all=True)

                # Generate PDF
                print("\n📄 Generating PDF invoice...")
                
                pdf_data = {
                    'invoice_number': invoice_data['invoice_number'],
                    'invoice_date': invoice_data['invoice_date'].strftime('%d-%m-%Y') if invoice_data['invoice_date'] else 'N/A',
                    'customer_name': invoice_data['customer_name'],
                    'customer_mobile': invoice_data['customer_mobile'],
                    'customer_address': invoice_data['customer_address'] or 'N/A',
                    'items': [{'description': item['service_name'] or 'Service', 'quantity': 1, 'rate': item['rate'], 'amount': item['amount']} for item in items],
                    'subtotal': invoice_data['total_amount'],
                    'gst_amount': 0,
                    'gst_percentage': 0,
                    'discount_amount': 0,
                    'total_amount': invoice_data['total_amount'],
                    'paid_amount': invoice_data['advance_payment'],
                    'balance_amount': invoice_data['balance_amount'],
                    'payment_mode': invoice_data['payment_mode'],
                    'payment_status': invoice_data['payment_status']
                }

                # Generate PDF
                generator = PDFInvoiceGenerator()
                pdf_path = generator.generate_invoice(pdf_data)
                
                print(f"✅ PDF generated: {pdf_path}")
                
                # Show options to user
                msg_box = QMessageBox(self)
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setWindowTitle("Send Invoice to Customer")
                msg_box.setText(
                    f"✅ Invoice PDF Ready!\n\n"
                    f"📄 File: {os.path.basename(pdf_path)}\n"
                    f"💾 Location: {pdf_path}\n\n"
                    f"Kaise bhejna hai?"
                )
                
                # Add buttons
                whatsapp_btn = msg_box.addButton("📱 WhatsApp + PDF", QMessageBox.ActionRole)
                download_btn = msg_box.addButton("💾 Download PDF", QMessageBox.ActionRole)
                cancel_btn = msg_box.addButton("Cancel", QMessageBox.RejectRole)
                
                msg_box.setDefaultButton(whatsapp_btn)
                msg_box.exec()
                
                clicked_button = msg_box.clickedButton()
                
                if clicked_button == whatsapp_btn:
                    # WhatsApp + PDF Download
                    self._send_whatsapp_with_pdf(invoice_data, pdf_path)
                    
                elif clicked_button == download_btn:
                    # Download Only
                    self.show_success_message(f"PDF downloaded!\n\nLocation:\n{pdf_path}")
                    # Open file location
                    os.startfile(os.path.dirname(pdf_path))

        except Exception as e:
            self.show_error_message(f"Error: {str(e)}")
            print(f"WhatsApp share error: {str(e)}")
            import traceback
            traceback.print_exc()

    def _send_whatsapp_with_pdf(self, invoice_data, pdf_path):
        """Send WhatsApp message and open PDF location for manual attach"""
        try:
            from utils.whatsapp_messages import format_message
            import webbrowser
            import os
            from PySide6.QtWidgets import QMessageBox
            from PySide6.QtGui import QClipboard
            from PySide6.QtWidgets import QApplication

            # Format WhatsApp message
            message = format_message(
                'invoice_share',
                customer_name=invoice_data['customer_name'],
                invoice_number=invoice_data['invoice_number'],
                total_amount=f"{invoice_data['total_amount']:,.2f}",
                paid_amount=f"{invoice_data['advance_payment']:,.2f}",
                balance_amount=f"{invoice_data['balance_amount']:,.2f}",
                invoice_date=invoice_data['invoice_date'].strftime('%d-%m-%Y') if invoice_data['invoice_date'] else 'N/A'
            )

            # Copy PDF path to clipboard
            clipboard = QApplication.clipboard()
            clipboard.setText(pdf_path)

            # Show instructions
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle("Send PDF via WhatsApp")
            msg_box.setText(
                "✅ PDF Invoice Ready!\n\n"
                "📱 WhatsApp open ho raha hai...\n\n"
                "📎 PDF Attach Kaise Karein:\n"
                "1. WhatsApp Web mein 📎 (Attach) icon par click karein\n"
                "2. 'Document' select karein\n"
                "3. Ctrl+V dabakar path paste karein ya browse karein\n"
                "4. PDF select karein aur Send karein\n\n"
                "📋 PDF path clipboard mein copy ho gaya hai!"
            )
            msg_box.setInformativeText(
                f"📄 PDF: {os.path.basename(pdf_path)}\n"
                f"📍 Customer: {invoice_data['customer_name']}\n"
                f"📱 Mobile: {invoice_data['customer_mobile']}"
            )
            msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg_box.setDefaultButton(QMessageBox.Ok)
            
            reply = msg_box.exec()
            
            if reply == QMessageBox.Ok:
                # Open WhatsApp with message
                WhatsAppHelper.send_message(invoice_data['customer_mobile'], message)
                
                # Open PDF folder
                os.startfile(os.path.dirname(pdf_path))
                
                self.show_success_message("✅ WhatsApp open ho gaya!\n📄 PDF folder bhi open ho gaya!\nAttach karke SEND karein!")

        except Exception as e:
            self.show_error_message(f"Error: {str(e)}")
            print(f"WhatsApp send error: {str(e)}")

    def delete_selected_invoice(self):
        """Delete selected invoice"""
        invoice = self.get_selected_invoice()
        if not invoice:
            return

        reply = QMessageBox.question(
            self,
            'Delete Invoice',
            f"Are you sure you want to delete invoice {invoice['invoice_number']}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                from database.db_connection import DatabaseContext

                with DatabaseContext() as db:
                    # Soft delete
                    query = "UPDATE invoices SET is_active = FALSE WHERE id = %s"
                    db.execute_query(query, (invoice['id'],))

                    self.show_success_message("Invoice deleted successfully")
                    self.load_invoices()

            except Exception as e:
                self.show_error_message(f"Error deleting invoice: {str(e)}")

    def refresh_data(self):
        """Refresh invoice list"""
        self.load_invoices()
