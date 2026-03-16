"""
Unified Theme - Single Cyan/Blue Color Palette
Professional Qt Theme for AC Service Billing Software
"""
from config import COLORS, FONTS
from PySide6.QtGui import QPalette, QColor


class UnifiedTheme:
    """Unified cyan/blue theme manager for consistent UI"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_colors(cls):
        return COLORS['dark']

    @classmethod
    def apply_palette(cls, widget):
        """Apply QPalette colors to a widget for proper theme support"""
        colors = cls.get_colors()
        palette = QPalette()

        # Base colors
        palette.setColor(QPalette.ColorRole.Window, QColor(colors['bg']))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(colors['fg']))
        palette.setColor(QPalette.ColorRole.Base, QColor(colors['card_bg']))

        # Critical: AlternateBase for QTableWidget alternating rows
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(colors['alt_row']))

        # Text color
        palette.setColor(QPalette.ColorRole.Text, QColor(colors['fg']))

        # Highlight (selection)
        palette.setColor(QPalette.ColorRole.Highlight, QColor(colors['primary']))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(colors['bg']))

        # Button colors
        palette.setColor(QPalette.ColorRole.Button, QColor(colors['card_bg']))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(colors['fg']))

        # Additional colors
        palette.setColor(QPalette.ColorRole.BrightText, QColor('#ffffff'))
        palette.setColor(QPalette.ColorRole.Light, QColor(colors['hover']))
        palette.setColor(QPalette.ColorRole.Midlight, QColor(colors['border']))
        palette.setColor(QPalette.ColorRole.Dark, QColor(colors['bg']))

        # Tooltip colors
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(colors['card_bg']))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(colors['fg']))

        # Disabled colors
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor(colors['muted']))
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, QColor(colors['muted']))
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor(colors['muted']))

        widget.setPalette(palette)

        # Force style refresh
        widget.style().unpolish(widget)
        widget.style().polish(widget)

    @classmethod
    def apply_table_theme(cls, table):
        """Apply theme specifically to QTableWidget for proper alternating rows"""
        from PySide6.QtWidgets import QTableWidget
        if not isinstance(table, QTableWidget):
            return

        colors = cls.get_colors()

        # Apply palette directly to table
        cls.apply_palette(table)

        # Apply stylesheet with explicit alternating row colors
        table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {colors['card_bg']};
                color: {colors['fg']};
                border: 1px solid {colors['border']};
                border-radius: 6px;
                gridline-color: {colors['border']};
                selection-background-color: {colors['primary']};
                selection-color: white;
                outline: none;
                alternate-background-color: {colors['alt_row']};
            }}
            QTableWidget::item {{
                padding: 8px;
                border: none;
                color: {colors['fg']};
                background-color: transparent;
            }}
            QTableWidget::item:selected {{
                background-color: {colors['primary']};
                color: white;
            }}
            QTableWidget::item:hover {{
                background-color: {colors['hover']};
                color: {colors['fg']};
            }}
            QTableWidget::item:alternate {{
                background-color: {colors['alt_row']};
                color: {colors['fg']};
            }}
            QTableWidget::item:alternate:selected {{
                background-color: {colors['primary']};
                color: white;
            }}
            QTableWidget::item:alternate:hover {{
                background-color: {colors['hover']};
                color: {colors['fg']};
            }}
            QHeaderView::section {{
                background-color: {colors['hover']};
                color: {colors['fg']};
                padding: 10px 8px;
                border: none;
                border-bottom: 2px solid {colors['border']};
                border-right: 1px solid {colors['border']};
                font-weight: bold;
                font-size: 10pt;
                text-transform: uppercase;
            }}
        """)

        # Force style refresh
        table.style().unpolish(table)
        table.style().polish(table)

    @classmethod
    def get_main_stylesheet(cls):
        """Get unified cyan/blue theme stylesheet"""
        colors = cls.get_colors()

        return f"""
        /* ========================================
           UNIFIED CYAN/BLUE THEME
           Professional AC Service Billing Software
           ======================================== */

        /* GLOBAL STYLES */
        QMainWindow, QWidget {{
            background-color: {colors['bg']};
            color: {colors['fg']};
            font-family: 'Segoe UI Variable', 'Segoe UI', Arial, sans-serif;
            font-size: 10pt;
        }}

        /* ========================================
           MAIN WINDOW WITH BORDER
           ======================================== */
        QMainWindow#mainWindow {{
            background-color: {colors['bg']};
            border: 1px solid {colors['border']};
        }}

        /* ========================================
           CARDS WITH PROPER BORDERS
           ======================================== */
        QFrame#cardFrame, QFrame#infoCard {{
            background-color: {colors['card_bg']};
            border: 1px solid {colors['border']};
            border-radius: 8px;
        }}

        QFrame#cardFrame:hover, QFrame#infoCard:hover {{
            border: 1px solid {colors['primary']};
            background-color: {colors['card_bg']};
        }}

        QFrame#metricCard {{
            background-color: {colors['card_bg']};
            border: 1px solid {colors['border']};
            border-radius: 8px;
        }}

        QFrame#metricCard:hover {{
            background-color: {colors['card_bg']};
            border: 1px solid {colors['primary']};
        }}

        /* ========================================
           SIDEBAR WITH MODERN STYLE
           ======================================== */
        QFrame#sidebarFrame {{
            background-color: {colors['sidebar']};
            border-right: 1px solid {colors['border']};
        }}

        QPushButton#sidebarButton {{
            background-color: transparent;
            color: {colors['fg']};
            border: 1px solid transparent;
            border-radius: 6px;
            padding: 12px 16px;
            text-align: left;
            font-size: 10pt;
            font-weight: normal;
        }}

        QPushButton#sidebarButton:hover {{
            background-color: {colors['hover']};
            border: 1px solid {colors['border']};
        }}

        QPushButton#sidebarButton:checked {{
            background-color: {colors['primary']};
            color: #ffffff;
            border: 1px solid {colors['primary']};
            font-weight: 600;
        }}

        QPushButton#sidebarButton::indicator {{
            width: 0px;
        }}

        /* ========================================
           HEADER WITH BORDER
           ======================================== */
        QFrame#headerFrame {{
            background-color: {colors['header']};
            border-bottom: 1px solid {colors['border']};
        }}

        QLabel#headerTitle {{
            font-size: 16pt;
            font-weight: 600;
            color: #ffffff;
        }}

        /* ========================================
           PRIMARY BUTTONS - CYAN
           ======================================== */
        QPushButton {{
            background-color: {colors['primary']};
            color: #ffffff;
            border: 1px solid {colors['primary']};
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: 600;
            font-size: 10pt;
        }}

        QPushButton:hover {{
            background-color: {colors['primary_hover']};
            border: 1px solid {colors['primary_hover']};
        }}

        QPushButton:pressed {{
            background-color: {colors['primary']};
            border: 1px solid {colors['primary']};
        }}

        QPushButton:disabled {{
            background-color: {colors['muted']};
            color: {colors['bg']};
        }}

        QPushButton#primaryButton {{
            background-color: {colors['primary']};
            color: #ffffff;
            border: 1px solid {colors['primary']};
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: 600;
        }}

        QPushButton#primaryButton:hover {{
            background-color: {colors['primary_hover']};
            border: 1px solid {colors['primary_hover']};
        }}

        QPushButton#secondaryButton {{
            background-color: {colors['secondary']};
            color: #ffffff;
            border: 1px solid {colors['secondary']};
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: 600;
        }}

        QPushButton#secondaryButton:hover {{
            background-color: {colors['hover']};
            border: 1px solid {colors['border']};
        }}

        QPushButton#successButton {{
            background-color: {colors['success']};
            color: #ffffff;
            border: 1px solid {colors['success']};
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: 600;
        }}

        QPushButton#successButton:hover {{
            background-color: #059669;
            border: 1px solid #059669;
        }}

        QPushButton#dangerButton {{
            background-color: {colors['danger']};
            color: #ffffff;
            border: 1px solid {colors['danger']};
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: 600;
        }}

        QPushButton#dangerButton:hover {{
            background-color: #b91c1c;
            border: 1px solid #b91c1c;
        }}

        QPushButton#warningButton {{
            background-color: {colors['warning']};
            color: #ffffff;
            border: 1px solid {colors['warning']};
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: 600;
        }}

        QPushButton#warningButton:hover {{
            background-color: #b45309;
            border: 1px solid #b45309;
        }}

        QPushButton#iconButton {{
            background-color: transparent;
            border: 1px solid transparent;
            border-radius: 6px;
            padding: 6px 10px;
            font-size: 14pt;
        }}

        QPushButton#iconButton:hover {{
            background-color: {colors['hover']};
            border: 1px solid {colors['border']};
        }}

        QPushButton#fabButton {{
            background-color: {colors['success']};
            color: #ffffff;
            border: 1px solid {colors['success']};
            border-radius: 28px;
            padding: 0px;
            font-size: 20pt;
            font-weight: bold;
            min-width: 56px;
            min-height: 56px;
            max-width: 56px;
            max-height: 56px;
        }}

        QPushButton#fabButton:hover {{
            background-color: #059669;
            border: 1px solid #059669;
        }}

        /* ========================================
           INPUT FIELDS WITH BORDERS
           ======================================== */
        QLineEdit {{
            background-color: {colors['card_bg']};
            color: {colors['fg']};
            border: 1px solid {colors['border']};
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 10pt;
            selection-background-color: {colors['primary']};
            selection-color: #ffffff;
        }}

        QLineEdit:hover {{
            border: 1px solid {colors['border']};
        }}

        QLineEdit:focus {{
            border: 1px solid {colors['primary']};
            background-color: {colors['card_bg']};
        }}

        QLineEdit:disabled {{
            background-color: {colors['hover']};
            color: {colors['muted']};
        }}

        QTextEdit, QPlainTextEdit {{
            background-color: {colors['card_bg']};
            color: {colors['fg']};
            border: 1px solid {colors['border']};
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 10pt;
            selection-background-color: {colors['primary']};
            selection-color: #ffffff;
        }}

        QTextEdit:hover, QPlainTextEdit:hover {{
            border: 1px solid {colors['border']};
        }}

        QTextEdit:focus, QPlainTextEdit:focus {{
            border: 1px solid {colors['primary']};
            background-color: {colors['card_bg']};
        }}

        /* ========================================
           COMBO BOX
           ======================================== */
        QComboBox {{
            background-color: {colors['card_bg']};
            color: {colors['fg']};
            border: 1px solid {colors['border']};
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 10pt;
            min-height: 16px;
        }}

        QComboBox:hover {{
            border: 1px solid {colors['border']};
        }}

        QComboBox:focus {{
            border: 1px solid {colors['primary']};
        }}

        QComboBox::drop-down {{
            border: none;
            width: 30px;
        }}

        QComboBox::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 6px solid {colors['fg']};
            margin-right: 10px;
        }}

        QComboBox QAbstractItemView {{
            background-color: {colors['card_bg']};
            color: {colors['fg']};
            border: 1px solid {colors['border']};
            border-radius: 6px;
            selection-background-color: {colors['primary']};
            selection-color: #ffffff;
            outline: none;
            padding: 4px;
        }}

        QComboBox QAbstractItemView::item {{
            min-height: 30px;
            padding: 4px 8px;
            border-radius: 4px;
        }}

        QComboBox QAbstractItemView::item:hover {{
            background-color: {colors['hover']};
        }}

        QComboBox QAbstractItemView::item:selected {{
            background-color: {colors['primary']};
            color: #ffffff;
        }}

        /* ========================================
           TABLE WITH PROPER BORDERS
           ======================================== */
        QTableWidget {{
            background-color: {colors['card_bg']};
            color: {colors['fg']};
            border: 1px solid {colors['border']};
            border-radius: 8px;
            gridline-color: {colors['border']};
            selection-background-color: {colors['primary']};
            selection-color: {colors['bg']};
            outline: none;
            alternate-background-color: {colors['alt_row']};
        }}

        QTableWidget::item {{
            padding: 10px;
            border: none;
            color: {colors['fg']};
            background-color: transparent;
        }}

        QTableWidget::item:selected {{
            background-color: {colors['primary']};
            color: {colors['bg']};
        }}

        QTableWidget::item:hover {{
            background-color: {colors['hover']};
            color: {colors['fg']};
        }}

        /* Alternate row styling */
        QTableWidget::item:alternate {{
            background-color: {colors['alt_row']};
            color: {colors['fg']};
        }}

        QTableWidget::item:alternate:selected {{
            background-color: {colors['primary']};
            color: {colors['bg']};
        }}

        QTableWidget::item:alternate:hover {{
            background-color: {colors['hover']};
            color: {colors['fg']};
        }}

        QHeaderView::section {{
            background-color: {colors['card_bg']};
            color: {colors['fg']};
            padding: 12px 8px;
            border: none;
            border-bottom: 2px solid {colors['border']};
            border-right: 1px solid {colors['border']};
            font-weight: 600;
            font-size: 10pt;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        QHeaderView::section:first {{
            border-top-left-radius: 8px;
        }}

        QHeaderView::section:last {{
            border-top-right-radius: 8px;
            border-right: none;
        }}

        QHeaderView::section:hover {{
            background-color: {colors['border']};
        }}

        /* ========================================
           SCROLLBARS - CYAN THEME
           ======================================== */
        QScrollBar:vertical {{
            background-color: {colors['bg']};
            width: 14px;
            border-radius: 7px;
            margin: 0px;
            border: 1px solid {colors['border']};
        }}

        QScrollBar::handle:vertical {{
            background-color: {colors['primary']};
            border-radius: 6px;
            min-height: 20px;
            margin: 1px;
        }}

        QScrollBar::handle:vertical:hover {{
            background-color: {colors['primary_hover']};
        }}

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}

        QScrollBar:horizontal {{
            background-color: {colors['bg']};
            height: 14px;
            border-radius: 7px;
            margin: 0px;
            border: 1px solid {colors['border']};
        }}

        QScrollBar::handle:horizontal {{
            background-color: {colors['primary']};
            border-radius: 6px;
            min-width: 20px;
            margin: 1px;
        }}

        QScrollBar::handle:horizontal:hover {{
            background-color: {colors['primary_hover']};
        }}

        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}

        /* ========================================
           GROUP BOX WITH BORDER
           ======================================== */
        QGroupBox {{
            background-color: {colors['card_bg']};
            border: 1px solid {colors['border']};
            border-radius: 8px;
            margin-top: 12px;
            padding-top: 16px;
            font-weight: 600;
            font-size: 11pt;
        }}

        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 12px;
            top: 0px;
            padding: 0 8px;
            color: {colors['primary']};
        }}

        /* ========================================
           LABELS
           ======================================== */
        QLabel {{
            background-color: transparent;
            color: {colors['fg']};
        }}

        QLabel#headingLabel {{
            font-size: 18pt;
            font-weight: 600;
            color: {colors['primary']};
        }}

        QLabel#subheadingLabel {{
            font-size: 11pt;
            color: {colors['muted']};
        }}

        QLabel#titleLabel {{
            font-size: 14pt;
            font-weight: 600;
            color: {colors['fg']};
        }}

        QLabel#valueLabel {{
            font-size: 28pt;
            font-weight: 700;
            color: {colors['primary']};
        }}

        QLabel#metricValueLabel {{
            font-size: 28pt;
            font-weight: 700;
            color: {colors['primary']};
        }}

        QLabel#metricLabel {{
            font-size: 10pt;
            color: {colors['muted']};
        }}

        QLabel#statusSuccess {{
            color: {colors['success']};
            font-weight: 600;
        }}

        QLabel#statusWarning {{
            color: {colors['warning']};
            font-weight: 600;
        }}

        QLabel#statusError {{
            color: {colors['danger']};
            font-weight: 600;
        }}

        /* ========================================
           FRAME & WIDGET CONTAINERS
           ======================================== */
        QFrame#contentFrame {{
            background-color: {colors['bg']};
        }}

        QFrame#separatorLine {{
            background-color: {colors['border']};
            max-height: 1px;
        }}

        QFrame#verticalSeparator {{
            background-color: {colors['border']};
            max-width: 1px;
        }}

        /* ========================================
           TAB WIDGET
           ======================================== */
        QTabWidget::pane {{
            border: 1px solid {colors['border']};
            border-radius: 8px;
            background-color: {colors['card_bg']};
            top: -1px;
        }}

        QTabBar::tab {{
            background-color: {colors['bg']};
            color: {colors['fg']};
            padding: 10px 20px;
            border: 1px solid transparent;
            border-bottom: 2px solid transparent;
            font-weight: 500;
            font-size: 10pt;
        }}

        QTabBar::tab:selected {{
            background-color: {colors['card_bg']};
            color: {colors['primary']};
            border-bottom: 2px solid {colors['primary']};
            font-weight: 600;
        }}

        QTabBar::tab:hover:!selected {{
            background-color: {colors['hover']};
            border: 1px solid {colors['border']};
        }}

        QTabBar::tab:first {{
            border-top-left-radius: 8px;
        }}

        QTabBar::tab:last {{
            border-top-right-radius: 8px;
        }}

        /* ========================================
           PROGRESS BAR
           ======================================== */
        QProgressBar {{
            background-color: {colors['hover']};
            border: 1px solid {colors['border']};
            border-radius: 6px;
            height: 10px;
            text-align: center;
        }}

        QProgressBar::chunk {{
            background-color: {colors['primary']};
            border-radius: 6px;
        }}

        /* ========================================
           CHECK BOX & RADIO BUTTON
           ======================================== */
        QCheckBox, QRadioButton {{
            color: {colors['fg']};
            spacing: 8px;
            font-size: 10pt;
        }}

        QCheckBox::indicator, QRadioButton::indicator {{
            width: 20px;
            height: 20px;
            border-radius: 4px;
            border: 2px solid {colors['border']};
            background-color: {colors['card_bg']};
        }}

        QCheckBox::indicator:checked, QRadioButton::indicator:checked {{
            background-color: {colors['primary']};
            border-color: {colors['primary']};
        }}

        QCheckBox::indicator:hover, QRadioButton::indicator:hover {{
            border-color: {colors['primary']};
        }}

        QRadioButton::indicator {{
            border-radius: 10px;
        }}

        /* ========================================
           SLIDER
           ======================================== */
        QSlider::groove:horizontal {{
            background-color: {colors['hover']};
            height: 6px;
            border-radius: 3px;
            border: 1px solid {colors['border']};
        }}

        QSlider::handle:horizontal {{
            background-color: {colors['primary']};
            width: 18px;
            margin: -6px 0;
            border-radius: 9px;
            border: 1px solid {colors['primary']};
        }}

        QSlider::handle:horizontal:hover {{
            background-color: {colors['primary_hover']};
        }}

        QSlider::groove:vertical {{
            background-color: {colors['hover']};
            width: 6px;
            border-radius: 3px;
            border: 1px solid {colors['border']};
        }}

        QSlider::handle:vertical {{
            background-color: {colors['primary']};
            height: 16px;
            margin: 0 -5px;
            border-radius: 8px;
            border: 1px solid {colors['primary']};
        }}

        /* ========================================
           SPIN BOX & DATE/TIME EDIT
           ======================================== */
        QSpinBox, QDoubleSpinBox {{
            background-color: {colors['card_bg']};
            color: {colors['fg']};
            border: 1px solid {colors['border']};
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 10pt;
        }}

        QSpinBox:focus, QDoubleSpinBox:focus {{
            border: 1px solid {colors['primary']};
        }}

        QSpinBox::up-button, QDoubleSpinBox::up-button,
        QSpinBox::down-button, QDoubleSpinBox::down-button {{
            background-color: transparent;
            border: none;
            width: 20px;
        }}

        QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
        QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{
            background-color: {colors['hover']};
        }}

        QDateEdit, QTimeEdit, QDateTimeEdit {{
            background-color: {colors['card_bg']};
            color: {colors['fg']};
            border: 1px solid {colors['border']};
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 10pt;
        }}

        QDateEdit:focus, QTimeEdit:focus, QDateTimeEdit:focus {{
            border: 1px solid {colors['primary']};
        }}

        QDateEdit::drop-down, QTimeEdit::drop-down, QDateTimeEdit::drop-down {{
            border: none;
            width: 30px;
        }}

        /* ========================================
           TOOL TIP
           ======================================== */
        QToolTip {{
            background-color: {colors['card_bg']};
            color: {colors['fg']};
            border: 1px solid {colors['border']};
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 9pt;
        }}

        /* ========================================
           MENU
           ======================================== */
        QMenu {{
            background-color: {colors['card_bg']};
            border: 1px solid {colors['border']};
            border-radius: 8px;
            padding: 6px;
        }}

        QMenu::item {{
            padding: 8px 24px;
            border-radius: 4px;
        }}

        QMenu::item:selected {{
            background-color: {colors['primary']};
            color: #ffffff;
        }}

        QMenu::separator {{
            height: 1px;
            background-color: {colors['border']};
            margin: 4px 0;
        }}

        /* ========================================
           STATUS BAR
           ======================================== */
        QStatusBar {{
            background-color: {colors['card_bg']};
            color: {colors['muted']};
            border-top: 1px solid {colors['border']};
            font-size: 9pt;
        }}

        QStatusBar::item {{
            border: none;
        }}

        /* ========================================
           SCROLL AREA
           ======================================== */
        QScrollArea {{
            background-color: transparent;
            border: none;
        }}

        /* ========================================
           LIST WIDGET
           ======================================== */
        QListWidget {{
            background-color: {colors['card_bg']};
            color: {colors['fg']};
            border: 1px solid {colors['border']};
            border-radius: 8px;
            outline: none;
        }}

        QListWidget::item {{
            padding: 10px;
            border-radius: 4px;
            border: 1px solid transparent;
        }}

        QListWidget::item:selected {{
            background-color: {colors['primary']};
            color: #ffffff;
            border: 1px solid {colors['primary']};
        }}

        QListWidget::item:hover {{
            background-color: {colors['hover']};
            border: 1px solid {colors['border']};
        }}

        /* ========================================
           TREE WIDGET
           ======================================== */
        QTreeWidget {{
            background-color: {colors['card_bg']};
            color: {colors['fg']};
            border: 1px solid {colors['border']};
            border-radius: 8px;
            outline: none;
        }}

        QTreeWidget::item {{
            padding: 8px;
            border: 1px solid transparent;
        }}

        QTreeWidget::item:selected {{
            background-color: {colors['primary']};
            color: #ffffff;
            border: 1px solid {colors['primary']};
        }}

        QTreeWidget::item:hover {{
            background-color: {colors['hover']};
            border: 1px solid {colors['border']};
        }}

        /* ========================================
           STACKED WIDGET
           ======================================== */
        QStackedWidget {{
            background-color: {colors['bg']};
        }}

        /* ========================================
           SPLASH SCREEN
           ======================================== */
        QSplashScreen {{
            background-color: {colors['bg']};
            border: 1px solid {colors['border']};
        }}
        """

    @classmethod
    def get_login_stylesheet(cls):
        """Get specialized stylesheet for login window"""
        colors = cls.get_colors()

        return f"""
        QMainWindow, QWidget {{
            background-color: {colors['bg']};
            color: {colors['fg']};
            font-family: 'Segoe UI Variable', 'Segoe UI', Arial, sans-serif;
        }}

        QLineEdit {{
            background-color: {colors['card_bg']};
            color: {colors['fg']};
            border: 1px solid {colors['border']};
            border-radius: 6px;
            padding: 12px 16px;
            font-size: 11pt;
            selection-background-color: {colors['primary']};
            selection-color: #ffffff;
        }}

        QLineEdit:focus {{
            border: 2px solid {colors['primary']};
        }}

        QPushButton#loginButton {{
            background-color: {colors['primary']};
            color: #ffffff;
            border: 1px solid {colors['primary']};
            border-radius: 8px;
            padding: 14px 32px;
            font-weight: bold;
            font-size: 11pt;
            min-height: 20px;
        }}

        QPushButton#loginButton:hover {{
            background-color: {colors['primary_hover']};
            border: 1px solid {colors['primary_hover']};
        }}

        QPushButton#loginButton:pressed {{
            background-color: {colors['primary']};
            border: 1px solid {colors['primary']};
        }}

        QPushButton#loginButton:disabled {{
            background-color: {colors['muted']};
        }}

        QLabel#loginTitle {{
            font-size: 24pt;
            font-weight: 600;
            color: {colors['primary']};
        }}

        QLabel#loginSubtitle {{
            font-size: 11pt;
            color: {colors['muted']};
        }}

        QLabel#inputLabel {{
            font-size: 9pt;
            font-weight: 600;
            color: {colors['fg']};
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        QFrame#loginCard {{
            background-color: {colors['card_bg']};
            border: 1px solid {colors['border']};
            border-radius: 16px;
        }}

        QFrame#logoFrame {{
            background-color: transparent;
            border: none;
        }}
        """
