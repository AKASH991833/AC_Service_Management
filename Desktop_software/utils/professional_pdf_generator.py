"""
Professional PDF Invoice Generator
Production-ready with clean, modern design
Optimized for A4 printing
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    Image, Line, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib import colors
from datetime import datetime
import os


class ProfessionalInvoicePDF:
    """
    Generate professional PDF invoices with modern design
    Features:
    - Clean A4 layout
    - Business branding
    - Proper table formatting
    - Print-optimized
    """

    # Brand Colors
    PRIMARY_COLOR = colors.HexColor('#1a237e')  # Deep Blue
    SECONDARY_COLOR = colors.HexColor('#3949ab')  # Lighter Blue
    ACCENT_COLOR = colors.HexColor('#ff6f00')  # Amber
    LIGHT_BG = colors.HexColor('#e8eaf6')
    TEXT_DARK = colors.HexColor('#212121')
    TEXT_LIGHT = colors.HexColor('#757575')

    def __init__(self, output_path="pdfs/"):
        self.output_path = output_path
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
        self._ensure_output_directory()

    def _ensure_output_directory(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

    def _create_custom_styles(self):
        """Create custom paragraph styles"""
        # Company Name Style
        self.company_style = ParagraphStyle(
            'Company',
            parent=self.styles['Heading1'],
            fontSize=28,
            textColor=self.PRIMARY_COLOR,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold',
            spaceAfter=5,
            leading=32
        )

        # Tagline Style
        self.tagline_style = ParagraphStyle(
            'Tagline',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=self.TEXT_LIGHT,
            alignment=TA_LEFT,
            spaceAfter=3,
            leading=12
        )

        # Invoice Title Style
        self.invoice_title_style = ParagraphStyle(
            'InvoiceTitle',
            parent=self.styles['Heading2'],
            fontSize=22,
            textColor=self.PRIMARY_COLOR,
            alignment=TA_RIGHT,
            fontName='Helvetica-Bold',
            spaceAfter=10,
            leading=26
        )

        # Section Header Style
        self.section_header_style = ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=self.PRIMARY_COLOR,
            fontName='Helvetica-Bold',
            spaceAfter=6,
            spaceBefore=6,
            leading=14
        )

        # Normal Text Style
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=self.TEXT_DARK,
            spaceAfter=4,
            leading=12
        )

        # Small Text Style
        self.small_style = ParagraphStyle(
            'Small',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=self.TEXT_LIGHT,
            spaceAfter=3,
            leading=11
        )

        # Table Header Style
        self.table_header_style = ParagraphStyle(
            'TableHeader',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.white,
            fontName='Helvetica-Bold',
            alignment=TA_CENTER,
            leading=12
        )

        # Table Cell Style
        self.table_cell_style = ParagraphStyle(
            'TableCell',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=self.TEXT_DARK,
            alignment=TA_CENTER,
            leading=12
        )

        # Total Label Style
        self.total_label_style = ParagraphStyle(
            'TotalLabel',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=self.TEXT_DARK,
            alignment=TA_RIGHT,
            leading=12
        )

        # Total Value Style
        self.total_value_style = ParagraphStyle(
            'TotalValue',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=self.PRIMARY_COLOR,
            fontName='Helvetica-Bold',
            alignment=TA_RIGHT,
            leading=14
        )

        # Grand Total Style
        self.grand_total_style = ParagraphStyle(
            'GrandTotal',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=self.PRIMARY_COLOR,
            fontName='Helvetica-Bold',
            alignment=TA_RIGHT,
            leading=18,
            spaceBefore=6
        )

        # Footer Style
        self.footer_style = ParagraphStyle(
            'Footer',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=self.TEXT_LIGHT,
            alignment=TA_CENTER,
            spaceBefore=10,
            leading=11
        )

        # Terms Style
        self.terms_style = ParagraphStyle(
            'Terms',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=self.TEXT_LIGHT,
            spaceAfter=4,
            leading=11
        )

    def _build_header(self, invoice_data):
        """Build invoice header with company info and invoice title"""
        elements = []

        # Company Header (Left) and Invoice Title (Right)
        header_data = [
            [
                f"<b>ANSH AIR COOL</b><br/>"
                f"<font size='9' color='#757575'>AC Sales | Service | Installation | Repair</font>",
                f"<font size='22' color='#1a237e'><b>INVOICE</b></font>"
            ]
        ]

        header_table = Table(header_data, colWidths=[4.5*inch, 2.5*inch])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (0, 0), 15),
        ]))
        elements.append(header_table)

        # Company Contact Info
        elements.append(Paragraph("<font color='#757575'>Phone: +91 9918331262 | +91 9819104977</font>", self.small_style))
        elements.append(Paragraph("<font color='#757575'>Email: anshaircool@gmail.com</font>", self.small_style))
        elements.append(Paragraph("<font color='#757575'>Mumbai, Maharashtra, India</font>", self.small_style))

        elements.append(Spacer(1, 0.3*inch))

        return elements

    def _build_invoice_info(self, invoice_data):
        """Build invoice number and date section"""
        elements = []

        info_data = [[
            f"<b>Invoice No:</b> {invoice_data['invoice_number']}",
            f"<b>Date:</b> {invoice_data.get('invoice_date', datetime.now().strftime('%d/%m/%Y'))}"
        ]]

        info_table = Table(info_data, colWidths=[3.5*inch, 3.5*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.LIGHT_BG),
            ('BOX', (0, 0), (-1, 0), 1, self.PRIMARY_COLOR),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('LEFTPADDING', (0, 0), (-1, 0), 15),
            ('RIGHTPADDING', (0, 0), (-1, 0), 15),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 0.25*inch))

        return elements

    def _build_customer_section(self, invoice_data):
        """Build customer billing section"""
        elements = []

        elements.append(Paragraph("BILL TO:", self.section_header_style))

        customer_html = f"""
        <font size='11'><b>{invoice_data.get('customer_name', 'Customer')}</b></font><br/>
        <font size='10'>{invoice_data.get('customer_address', '')}</font><br/>
        <font size='10'>Mobile: {invoice_data.get('customer_mobile', '')}</font>
        """

        if invoice_data.get('customer_email'):
            customer_html += f"<br/><font size='10'>Email: {invoice_data['customer_email']}</font>"

        elements.append(Paragraph(customer_html, self.normal_style))
        elements.append(Spacer(1, 0.2*inch))

        return elements

    def _build_items_table(self, invoice_data):
        """Build items/services table"""
        elements = []

        elements.append(Paragraph("ITEMS & SERVICES", self.section_header_style))

        # Table headers
        table_data = [[
            "<font color='white'>Sr.</font>",
            "<font color='white'>Description</font>",
            "<font color='white'>Qty</font>",
            "<font color='white'>Rate</font>",
            "<font color='white'>Amount</font>"
        ]]

        # Add items
        for i, item in enumerate(invoice_data.get('items', []), 1):
            table_data.append([
                str(i),
                item.get('description', ''),
                str(item.get('quantity', 1)),
                f"₹{item.get('rate', 0):,.2f}",
                f"₹{item.get('amount', 0):,.2f}"
            ])

        # Create table
        items_table = Table(table_data, colWidths=[0.5*inch, 3.5*inch, 0.8*inch, 1.2*inch, 1.5*inch])
        items_table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), self.PRIMARY_COLOR),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            # Rows
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            # Row backgrounds
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            # Alternating row colors
            *[('BACKGROUND', (0, i), (-1, i), self.LIGHT_BG) for i in range(2, len(table_data), 2)]
        ]))

        elements.append(items_table)
        elements.append(Spacer(1, 0.25*inch))

        return elements

    def _build_totals_section(self, invoice_data):
        """Build payment summary and totals"""
        elements = []

        elements.append(Paragraph("PAYMENT SUMMARY", self.section_header_style))

        subtotal = float(invoice_data.get('subtotal', 0))
        discount = float(invoice_data.get('discount', 0))
        tax_amount = float(invoice_data.get('tax_amount', 0))
        total_amount = float(invoice_data.get('total_amount', 0))
        paid_amount = float(invoice_data.get('paid_amount', 0))
        balance_amount = float(invoice_data.get('balance_amount', 0))

        # Totals table
        totals_data = [
            ['Subtotal:', f"₹{subtotal:,.2f}"],
            ['Discount:', f"- ₹{discount:,.2f}"],
            ['Tax (GST):', f"₹{tax_amount:,.2f}"],
            ['<b>TOTAL:</b>', f"<b>₹{total_amount:,.2f}</b>"]
        ]

        totals_table = Table(totals_data, colWidths=[4.5*inch, 2.5*inch])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('FONTNAME', (-1, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (-1, -1), (-1, -1), 12),
            ('TEXTCOLOR', (-1, -1), (-1, -1), self.PRIMARY_COLOR),
            ('BOTTOMPADDING', (0, -1), (-1, -1), 12),
            ('LINEABOVE', (0, -1), (-1, -1), 2, self.PRIMARY_COLOR),
            ('TOPPADDING', (0, 0), (-1, 0), 6),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ]))
        elements.append(totals_table)

        elements.append(Spacer(1, 0.2*inch))

        # Payment status
        status_data = [[
            f"<b>Paid:</b> ₹{paid_amount:,.2f}",
            f"<b>Balance:</b> ₹{balance_amount:,.2f}"
        ]]

        status_table = Table(status_data, colWidths=[3.5*inch, 3.5*inch])
        status_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('BOX', (0, 0), (-1, 0), 1, colors.black),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('LEFTPADDING', (0, 0), (-1, 0), 15),
            ('RIGHTPADDING', (0, 0), (-1, 0), 15),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (-1, 0), self.LIGHT_BG),
        ]))
        elements.append(status_table)

        return elements

    def _build_footer(self, invoice_data):
        """Build invoice footer with terms and bank details"""
        elements = []

        elements.append(Spacer(1, 0.3*inch))

        # Terms and Conditions
        elements.append(Paragraph("TERMS & CONDITIONS:", self.section_header_style))

        terms = [
            "1. Goods once sold will not be taken back.",
            "2. Interest @18% p.a. will be charged on delayed payments.",
            "3. All disputes subject to local jurisdiction.",
            "4. Please pay within 30 days from invoice date.",
            "5. Thank you for your business!"
        ]

        for term in terms:
            elements.append(Paragraph(term, self.terms_style))

        elements.append(Spacer(1, 0.2*inch))

        # Bank Details (Optional)
        bank_details = """
        <b>BANK DETAILS FOR PAYMENT:</b><br/>
        Account Name: Ansh Air Cool<br/>
        Bank: [Bank Name]<br/>
        Account No: [Account Number]<br/>
        IFSC Code: [IFSC Code]<br/>
        Branch: [Branch Name]
        """
        elements.append(Paragraph(bank_details, self.small_style))

        elements.append(Spacer(1, 0.3*inch))

        # Footer
        footer_text = """
        <b>ANSH AIR COOL</b><br/>
        Phone: +91 9918331262 | +91 9819104977<br/>
        Email: anshaircool@gmail.com<br/>
        Mumbai, Maharashtra, India
        """
        elements.append(Paragraph(footer_text, self.footer_style))

        return elements

    def generate(self, invoice_data):
        """
        Generate complete PDF invoice

        Args:
            invoice_data: Dictionary containing invoice details
                Required keys: invoice_number, customer_name, customer_mobile,
                              items (list), subtotal, total_amount, paid_amount, balance_amount

        Returns:
            filepath: Path to generated PDF
        """
        # Create filename
        filename = f"{invoice_data['invoice_number']}.pdf"
        filepath = os.path.join(self.output_path, filename)

        # Create document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch,
            title=f"Invoice {invoice_data['invoice_number']}"
        )

        # Build content
        story = []

        # Add all sections
        story.extend(self._build_header(invoice_data))
        story.extend(self._build_invoice_info(invoice_data))
        story.extend(self._build_customer_section(invoice_data))
        story.extend(self._build_items_table(invoice_data))
        story.extend(self._build_totals_section(invoice_data))
        story.extend(self._build_footer(invoice_data))

        # Build PDF
        doc.build(story)

        return filepath


# Convenience function
def create_invoice_pdf(invoice_data, output_path="pdfs/"):
    """
    Quick function to create professional invoice PDF

    Args:
        invoice_data: Dictionary with invoice details
        output_path: Directory to save PDF

    Returns:
        filepath: Path to generated PDF
    """
    generator = ProfessionalInvoicePDF(output_path)
    return generator.generate(invoice_data)


# Example usage
if __name__ == "__main__":
    # Sample invoice data
    sample_data = {
        'invoice_number': 'INV20260326001',
        'invoice_date': '26/03/2026',
        'customer_name': 'Rajesh Kumar',
        'customer_mobile': '9876543210',
        'customer_email': 'rajesh@example.com',
        'customer_address': '123 Main Street, Andheri West, Mumbai - 400058',
        'items': [
            {'description': 'AC Installation (1.5 Ton)', 'quantity': 1, 'rate': 500, 'amount': 500},
            {'description': 'Copper Pipe (per meter)', 'quantity': 5, 'rate': 800, 'amount': 4000},
            {'description': 'Stabilizer', 'quantity': 1, 'rate': 2500, 'amount': 2500},
        ],
        'subtotal': 7000,
        'discount': 0,
        'tax_amount': 1260,
        'total_amount': 8260,
        'paid_amount': 5000,
        'balance_amount': 3260
    }

    filepath = create_invoice_pdf(sample_data)
    print(f"Invoice generated: {filepath}")
