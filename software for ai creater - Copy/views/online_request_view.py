"""
Online Request View - PySide6 Online Request Management
Professional online request management with status tracking
Features: Auto-refresh, Real-time notifications, Sound alerts
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea,
    QSizePolicy, QSplitter, QMessageBox, QFormLayout, QComboBox,
    QTextEdit, QGroupBox, QDateEdit, QDialog, QDialogButtonBox, QFileDialog,
    QGraphicsOpacityEffect, QSpacerItem
)
from PySide6.QtCore import Qt, QDate, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QColor
from datetime import datetime
import os

from utils.unified_theme import UnifiedTheme
from views.base_window import BaseView


class OnlineRequestView(BaseView):
    """Online request management view with auto-refresh and notifications"""

    def __init__(self, db, controller):
        super().__init__()
        self.db = db
        self.controller = controller
        self.selected_message_id = None
        
        # Auto-refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.auto_refresh_check)
        self.refresh_timer.start(30000)  # 30 seconds
        
        # Track last count for new request detection
        self.last_request_count = 0
        self.last_pending_count = 0
        
        # Notification label (for toast)
        self.notification_label = None
        
        # Sound enabled
        self.sound_enabled = True

        self._setup_ui()
        self.load_messages()
        self.update_request_count()

    def update_theme_colors(self):
        """Update theme colors for proper dark theme support"""
        colors = self.theme_manager.get_colors()
        
        # Apply QPalette colors
        self.theme_manager.apply_palette(self)
        
        # Apply stylesheet
        self.setStyleSheet(self.theme_manager.get_main_stylesheet())
        
        # Apply theme directly to table for proper alternating colors
        if hasattr(self, 'messages_table'):
            self.theme_manager.apply_table_theme(self.messages_table)
        
        # Refresh data to ensure proper display
        self.load_messages()

    def _setup_ui(self):
        """Setup online request UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Header
        self._create_header(main_layout)

        # Controls
        self._create_controls(main_layout)

        # Main content
        self._create_content(main_layout)

    def _create_header(self, layout):
        """Create header section with counter badge"""
        colors = self.theme_manager.get_colors()

        # Title row
        title_layout = QHBoxLayout()
        
        title_label = QLabel("🌐 ONLINE REQUESTS")
        title_label.setStyleSheet(f"""
            font-size: 18pt;
            font-weight: bold;
            color: {colors['primary']};
        """)
        title_layout.addWidget(title_label)
        
        # Counter badge
        self.counter_badge = QLabel("0")
        self.counter_badge.setStyleSheet("""
            background-color: #ef4444;
            color: white;
            font-size: 11pt;
            font-weight: bold;
            min-width: 28px;
            max-width: 28px;
            min-height: 28px;
            max-height: 28px;
            border-radius: 14px;
            padding: 4px 8px;
        """)
        self.counter_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(self.counter_badge)
        
        # Auto-refresh status
        self.refresh_status_label = QLabel("🔄 Auto-refresh: ON (30s)")
        self.refresh_status_label.setStyleSheet(f"""
            font-size: 9pt;
            color: {colors['muted']};
        """)
        title_layout.addWidget(self.refresh_status_label)
        
        title_layout.addStretch()
        
        # Manual refresh button
        refresh_btn = QPushButton("🔄 Refresh Now")
        refresh_btn.setObjectName("primaryButton")
        refresh_btn.setFixedWidth(130)
        refresh_btn.clicked.connect(self.load_messages)
        title_layout.addWidget(refresh_btn)
        
        layout.addLayout(title_layout)

        subtitle_label = QLabel("Manage website form submissions and service requests")
        subtitle_label.setStyleSheet(f"""
            font-size: 11pt;
            color: {colors['muted']};
        """)
        layout.addWidget(subtitle_label)

    def _create_controls(self, layout):
        """Create control buttons"""
        control_layout = QHBoxLayout()

        # Search
        search_label = QLabel("🔍 Search:")
        control_layout.addWidget(search_label)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Name, Phone, Email...")
        self.search_input.setMinimumWidth(300)
        control_layout.addWidget(self.search_input)

        # Status filter
        self.status_filter = QComboBox()
        self.status_filter.addItems(['All', 'unread', 'read', 'Contacted', 'Converted', 'Rejected'])
        control_layout.addWidget(self.status_filter)

        # Filter button
        filter_btn = QPushButton("🔍 Filter")
        filter_btn.setObjectName("primaryButton")
        filter_btn.clicked.connect(self.load_messages)
        control_layout.addWidget(filter_btn)

        control_layout.addStretch()

        # Export button
        export_btn = QPushButton("📊 Export")
        export_btn.setObjectName("secondaryButton")
        export_btn.clicked.connect(self.export_to_excel)
        control_layout.addWidget(export_btn)

        layout.addLayout(control_layout)

    def _create_content(self, layout):
        """Create main content"""
        # Messages table
        self.messages_table = QTableWidget()
        self.messages_table.setColumnCount(8)
        self.messages_table.setHorizontalHeaderLabels([
            'ID', 'Name', 'Phone', 'Email', 'Service', 'Date', 'Status', 'Message'
        ])

        header = self.messages_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.Stretch)

        self.messages_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.messages_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.messages_table.setAlternatingRowColors(True)
        self.messages_table.verticalHeader().setVisible(False)
        self.messages_table.itemSelectionChanged.connect(self.on_message_select)

        layout.addWidget(self.messages_table)

        # Action buttons
        btn_layout = QHBoxLayout()

        self.whatsapp_btn = QPushButton("💬 Send WhatsApp")
        self.whatsapp_btn.setObjectName("successButton")
        self.whatsapp_btn.clicked.connect(self.send_whatsapp_message)
        self.whatsapp_btn.setEnabled(False)
        btn_layout.addWidget(self.whatsapp_btn)

        self.contact_btn = QPushButton("📞 Contact")
        self.contact_btn.setObjectName("secondaryButton")
        self.contact_btn.clicked.connect(self.contact_customer)
        self.contact_btn.setEnabled(False)
        btn_layout.addWidget(self.contact_btn)

        self.status_btn = QPushButton("📝 Update Status")
        self.status_btn.setObjectName("primaryButton")
        self.status_btn.clicked.connect(self.update_status)
        self.status_btn.setEnabled(False)
        btn_layout.addWidget(self.status_btn)

        self.delete_btn = QPushButton("🗑️ Delete")
        self.delete_btn.setObjectName("dangerButton")
        self.delete_btn.clicked.connect(self.delete_message)
        self.delete_btn.setEnabled(False)
        btn_layout.addWidget(self.delete_btn)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)

    def load_messages(self):
        """Load messages from database"""
        search_term = self.search_input.text().strip()
        status = self.status_filter.currentText()
        if status == 'All':
            status = None

        messages = self.controller.get_all_contact_messages(
            search_term=search_term,
            status=status,
            limit=100
        )

        self.messages_table.setRowCount(0)
        for msg in (messages or []):
            row = self.messages_table.rowCount()
            self.messages_table.insertRow(row)

            self.messages_table.setItem(row, 0, QTableWidgetItem(str(msg['id'])))
            self.messages_table.setItem(row, 1, QTableWidgetItem(msg['name']))
            self.messages_table.setItem(row, 2, QTableWidgetItem(msg['phone']))
            self.messages_table.setItem(row, 3, QTableWidgetItem(msg['email']))
            self.messages_table.setItem(row, 4, QTableWidgetItem(f"{msg['service_type']} - {msg['ac_type']}"))
            
            date_str = msg['created_at'].strftime('%d-%m-%Y') if msg['created_at'] else 'N/A'
            self.messages_table.setItem(row, 5, QTableWidgetItem(date_str))
            
            # Status with color
            status_item = QTableWidgetItem(msg['status'])
            if msg['status'] in ['Pending', 'unread']:
                status_item.setBackground(Qt.GlobalColor.darkOrange)
                status_item.setForeground(Qt.GlobalColor.white)
            elif msg['status'] in ['Contacted', 'read']:
                status_item.setBackground(Qt.GlobalColor.darkCyan)
                status_item.setForeground(Qt.GlobalColor.white)
            elif msg['status'] == 'Converted':
                status_item.setBackground(Qt.GlobalColor.darkGreen)
                status_item.setForeground(Qt.GlobalColor.white)
            else:
                status_item.setBackground(Qt.GlobalColor.gray)
                status_item.setForeground(Qt.GlobalColor.white)
            self.messages_table.setItem(row, 6, status_item)
            
            self.messages_table.setItem(row, 7, QTableWidgetItem(msg['message'][:100] + '...' if len(msg['message']) > 100 else msg['message']))
        
        # Update counter after loading
        self.update_request_count()

    def update_request_count(self):
        """Update request counter badge"""
        try:
            stats = self.controller.get_statistics()
            if stats:
                pending_count = stats.get('pending', 0)
                total_count = stats.get('total', 0)
                
                # Update badge
                self.counter_badge.setText(str(pending_count))
                
                # Change color based on count
                if pending_count > 10:
                    self.counter_badge.setStyleSheet("""
                        background-color: #dc2626;
                        color: white;
                        font-size: 11pt;
                        font-weight: bold;
                        min-width: 28px;
                        max-width: 28px;
                        min-height: 28px;
                        max-height: 28px;
                        border-radius: 14px;
                        padding: 4px 8px;
                    """)
                elif pending_count > 0:
                    self.counter_badge.setStyleSheet("""
                        background-color: #f59e0b;
                        color: white;
                        font-size: 11pt;
                        font-weight: bold;
                        min-width: 28px;
                        max-width: 28px;
                        min-height: 28px;
                        max-height: 28px;
                        border-radius: 14px;
                        padding: 4px 8px;
                    """)
                else:
                    self.counter_badge.setStyleSheet("""
                        background-color: #10b981;
                        color: white;
                        font-size: 11pt;
                        font-weight: bold;
                        min-width: 28px;
                        max-width: 28px;
                        min-height: 28px;
                        max-height: 28px;
                        border-radius: 14px;
                        padding: 4px 8px;
                    """)
        except Exception as e:
            print(f"[ERROR] Failed to update counter: {e}")

    def auto_refresh_check(self):
        """Auto-refresh check for new requests"""
        try:
            stats = self.controller.get_statistics()
            if stats:
                current_pending = stats.get('pending', 0)
                current_total = stats.get('total', 0)
                
                # Check for new requests
                if current_total > self.last_request_count and self.last_request_count > 0:
                    # New request detected!
                    new_count = current_total - self.last_request_count
                    self.show_new_request_notification(new_count)
                    self.load_messages()  # Auto-refresh
                elif current_pending > self.last_pending_count and self.last_pending_count > 0:
                    # Pending count increased
                    self.show_new_request_notification(current_pending - self.last_pending_count)
                    self.load_messages()
                
                # Update last counts
                self.last_request_count = current_total
                self.last_pending_count = current_pending
                
                # Update refresh status
                self.refresh_status_label.setText(f"🔄 Auto-refresh: ON (Last: {datetime.now().strftime('%H:%M:%S')})")
                
        except Exception as e:
            print(f"[ERROR] Auto-refresh check failed: {e}")

    def show_new_request_notification(self, count):
        """Show toast notification for new requests"""
        # Play sound
        if self.sound_enabled:
            self.play_notification_sound()
        
        # Show toast notification
        self.show_toast_notification(
            title="🔔 New Request" if count == 1 else f"🔔 {count} New Requests",
            message="Website se naya service request aaya hai!",
            duration=5000
        )

    def play_notification_sound(self):
        """Play notification sound"""
        try:
            # Use Windows default sound
            import winsound
            # Play system notification sound
            winsound.PlaySound("SystemNotification", winsound.SND_ALIAS | winsound.SND_ASYNC)
        except Exception as e:
            print(f"[INFO] Sound play failed: {e}")

    def show_toast_notification(self, title, message, duration=5000):
        """Show toast notification at bottom-right"""
        try:
            # Create notification widget
            self.toast_widget = QWidget()
            self.toast_widget.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)
            self.toast_widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            self.toast_widget.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
            
            # Layout
            layout = QVBoxLayout(self.toast_widget)
            layout.setContentsMargins(20, 15, 20, 15)
            
            # Content
            content_layout = QVBoxLayout()
            
            # Title
            title_label = QLabel(title)
            title_label.setStyleSheet("""
                font-size: 14pt;
                font-weight: bold;
                color: white;
            """)
            content_layout.addWidget(title_label)
            
            # Message
            msg_label = QLabel(message)
            msg_label.setStyleSheet("""
                font-size: 11pt;
                color: #e2e8f0;
            """)
            msg_label.setWordWrap(True)
            content_layout.addWidget(msg_label)
            
            layout.addLayout(content_layout)
            
            # Style
            self.toast_widget.setStyleSheet("""
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0ea5e9,
                    stop:1 #8b5cf6);
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            """)
            
            # Position at bottom-right
            screen_geometry = self.window().windowHandle().screen().geometry()
            toast_width = 350
            toast_height = 120
            
            x = screen_geometry.width() - toast_width - 40
            y = screen_geometry.height() - toast_height - 40
            
            self.toast_widget.setGeometry(x, y, toast_width, toast_height)
            
            # Show with fade-in animation
            self.toast_widget.show()
            
            # Auto-hide after duration
            QTimer.singleShot(duration, self.toast_widget.close)
            
        except Exception as e:
            print(f"[ERROR] Toast notification failed: {e}")

    def on_message_select(self):
        """Handle message selection"""
        selected_rows = self.messages_table.selectedItems()
        has_selection = len(selected_rows) > 0
        self.whatsapp_btn.setEnabled(has_selection)
        self.contact_btn.setEnabled(has_selection)
        self.status_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)

        if has_selection:
            row = selected_rows[0].row()
            self.selected_message_id = int(self.messages_table.item(row, 0).text())

    def send_whatsapp_message(self):
        """Send WhatsApp message to customer"""
        if not self.selected_message_id:
            return

        # Get message details
        messages = self.controller.get_all_contact_messages()
        msg = next((m for m in messages if m['id'] == self.selected_message_id), None)

        if not msg:
            self.show_warning_message("Customer details not found")
            return

        # Professional WhatsApp message template
        message = f"""*Ansh Air Cool - Service Request Confirmation* ✅

Dear *{msg['name']}*,

Thank you for contacting Ansh Air Cool!

📋 *Your Request Details:*
━━━━━━━━━━━━━━━━
🔹 Request ID: #{msg['id']}
🔹 Service: {msg['service_type'].title()}
🔹 AC Type: {msg['ac_type']}
🔹 Date: {msg['created_at'].strftime('%d-%m-%Y') if msg['created_at'] else 'N/A'}
━━━━━━━━━━━━━━━━

👨‍🔧 *Next Steps:*
• Our team will review your request
• A technician will contact you within 2-4 hours
• Service appointment will be scheduled as per your preference

📞 *Need Immediate Help?*
Call us: +91 9819104977
WhatsApp: +91 9819104977

🌐 Website: anshaircool.com

*Ansh Air Cool Team* ❄️
Cool Solutions, Happy Customers!
"""

        # Open WhatsApp Web with pre-filled message
        self._open_whatsapp(msg['phone'], message)

    def contact_customer(self):
        """Contact customer via phone/WhatsApp"""
        if not self.selected_message_id:
            return

        # Get message details
        messages = self.controller.get_all_contact_messages()
        msg = next((m for m in messages if m['id'] == self.selected_message_id), None)

        if msg:
            # Show contact options
            dialog = ContactOptionsDialog(msg, self)
            dialog.exec()

    def _open_whatsapp(self, phone, message):
        """Open WhatsApp Web with pre-filled message"""
        import webbrowser
        import urllib.parse

        # Clean phone number
        clean_phone = phone.replace(' ', '').replace('-', '').replace('+', '')
        
        # Add India country code if not present
        if not clean_phone.startswith('91') and len(clean_phone) == 10:
            clean_phone = '91' + clean_phone
        
        # Create WhatsApp URL
        url = f"https://wa.me/{clean_phone}?text={urllib.parse.quote(message)}"
        
        # Open in browser
        webbrowser.open(url)
        
        # Update status to Contacted
        from database.db_connection import DatabaseContext
        with DatabaseContext() as db:
            db.execute_query(
                "UPDATE contact_messages SET status = 'Contacted', updated_at = NOW() WHERE id = %s",
                (self.selected_message_id,)
            )
        
        self.load_messages()

    def update_status(self):
        """Update message status"""
        if not self.selected_message_id:
            return

        dialog = StatusUpdateDialog(self.selected_message_id, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_messages()
            self.show_success_message("Status updated successfully")

    def delete_message(self):
        """Delete selected message"""
        if not self.selected_message_id:
            self.show_warning_message("Please select a message to delete")
            return

        if self.show_question("Are you sure you want to delete this message?"):
            self.controller.delete_message(self.selected_message_id)
            self.selected_message_id = None
            self.load_messages()
            self.show_success_message("Message deleted successfully")

    def export_to_excel(self):
        """Export messages to Excel"""
        try:
            from openpyxl import Workbook
            from PySide6.QtWidgets import QFileDialog
            
            wb = Workbook()
            ws = wb.active
            ws.title = "Online Requests"
            
            headers = ['ID', 'Name', 'Phone', 'Email', 'Service Type', 'AC Type', 
                      'Preferred Date', 'Time Slot', 'Message', 'Status', 'Created At']
            ws.append(headers)
            
            messages = self.controller.get_all_contact_messages(limit=1000)
            for msg in (messages or []):
                ws.append([
                    msg['id'], msg['name'], msg['phone'], msg['email'],
                    msg['service_type'], msg['ac_type'], msg['preferred_date'],
                    msg['time_slot'], msg['message'], msg['status'],
                    msg['created_at'].strftime('%Y-%m-%d %H:%M:%S') if msg['created_at'] else ''
                ])
            
            filename = f"Online_Requests_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Report", filename, "Excel Files (*.xlsx)")
            
            if file_path:
                wb.save(file_path)
                self.show_success_message(f"Report exported to: {file_path}")
                
        except Exception as e:
            self.show_error_message(f"Export failed: {str(e)}")

    def cleanup(self):
        """Cleanup timer when view is closed"""
        if self.refresh_timer.isActive():
            self.refresh_timer.stop()
        print("[INFO] Online Request View cleanup complete")


class ContactOptionsDialog(QDialog):
    """Dialog for contacting customer via phone or WhatsApp"""

    def __init__(self, customer_data, parent=None):
        super().__init__(parent)
        self.customer = customer_data
        self.setWindowTitle("Contact Customer")
        self.setMinimumWidth(500)

        self._setup_ui()

    def _setup_ui(self):
        """Setup dialog UI"""
        layout = QVBoxLayout(self)

        # Customer info
        info_group = QGroupBox("Customer Details")
        info_layout = QFormLayout()
        
        info_layout.addRow("Name:", QLabel(self.customer['name']))
        info_layout.addRow("Phone:", QLabel(self.customer['phone']))
        info_layout.addRow("Email:", QLabel(self.customer['email'] or 'N/A'))
        info_layout.addRow("Service:", QLabel(f"{self.customer['service_type']} - {self.customer['ac_type']}"))
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)

        # Contact options
        contact_label = QLabel("How would you like to contact?")
        contact_label.setStyleSheet("font-size: 11pt; font-weight: bold; margin: 10px 0;")
        layout.addWidget(contact_label)

        btn_layout = QHBoxLayout()

        # WhatsApp button
        whatsapp_btn = QPushButton("💬 WhatsApp Message")
        whatsapp_btn.setObjectName("successButton")
        whatsapp_btn.setMinimumHeight(50)
        whatsapp_btn.clicked.connect(self.send_whatsapp)
        btn_layout.addWidget(whatsapp_btn)

        # Call button
        call_btn = QPushButton("📞 Phone Call")
        call_btn.setObjectName("primaryButton")
        call_btn.setMinimumHeight(50)
        call_btn.clicked.connect(self.make_call)
        btn_layout.addWidget(call_btn)

        layout.addLayout(btn_layout)

        # Close button
        close_btn = QPushButton("Close")
        close_btn.setObjectName("secondaryButton")
        close_btn.clicked.connect(self.reject)
        layout.addWidget(close_btn)

    def send_whatsapp(self):
        """Send WhatsApp message"""
        import webbrowser
        import urllib.parse

        message = f"""*Ansh Air Cool - Service Request Confirmation* ✅

Dear *{self.customer['name']}*,

Thank you for contacting Ansh Air Cool!

📋 *Your Request Details:*
━━━━━━━━━━━━━━━━
🔹 Request ID: #{self.customer['id']}
🔹 Service: {self.customer['service_type'].title()}
🔹 AC Type: {self.customer['ac_type']}
━━━━━━━━━━━━━━━━

👨‍🔧 Our team will contact you within 2-4 hours.

📞 Need Help? Call: +91 9819104977

*Ansh Air Cool Team* ❄️
"""

        # Clean phone number
        clean_phone = self.customer['phone'].replace(' ', '').replace('-', '').replace('+', '')
        if not clean_phone.startswith('91') and len(clean_phone) == 10:
            clean_phone = '91' + clean_phone
        
        url = f"https://wa.me/{clean_phone}?text={urllib.parse.quote(message)}"
        webbrowser.open(url)
        
        # Update status
        from database.db_connection import DatabaseContext
        with DatabaseContext() as db:
            db.execute_query(
                "UPDATE contact_messages SET status = 'Contacted', updated_at = NOW() WHERE id = %s",
                (self.customer['id'],)
            )
        
        self.accept()
        QMessageBox.information(self, "WhatsApp", "WhatsApp Web opened! Press Enter to send the message.")

    def make_call(self):
        """Make phone call"""
        phone = self.customer['phone']
        reply = QMessageBox.question(
            self, "Call Customer",
            f"Do you want to call {self.customer['name']} at {phone}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Update status
            from database.db_connection import DatabaseContext
            with DatabaseContext() as db:
                db.execute_query(
                    "UPDATE contact_messages SET status = 'Contacted', updated_at = NOW() WHERE id = %s",
                    (self.customer['id'],)
                )
            self.accept()


class StatusUpdateDialog(QDialog):
    """Dialog for updating message status"""

    def __init__(self, message_id, parent=None):
        super().__init__(parent)
        self.message_id = message_id
        self.setWindowTitle("Update Status")
        self.setMinimumWidth(400)
        
        self._setup_ui()

    def _setup_ui(self):
        """Setup dialog UI"""
        layout = QVBoxLayout(self)
        
        form = QFormLayout()

        self.status_combo = QComboBox()
        self.status_combo.addItems(['unread', 'read', 'Contacted', 'Converted', 'Rejected'])
        form.addRow("Status:", self.status_combo)
        
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(100)
        form.addRow("Notes:", self.notes_input)
        
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def accept(self):
        """Save and close"""
        from database.db_connection import DatabaseContext
        
        status = self.status_combo.currentText()
        
        with DatabaseContext() as db:
            db.execute_query(
                "UPDATE contact_messages SET status = %s, updated_at = NOW() WHERE id = %s",
                (status, self.message_id)
            )
        
        super().accept()
