"""
Professional A4 GST-Compliant Invoice PDF Generator
AC Service & AMC Billing Software
Supports: Regular Invoice, AMC, Installation, Service
All fields dynamic - No hardcoded values
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, 
    Image, KeepTogether, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from datetime import datetime
import os


class PDFGenerator:
    """Professional GST Invoice Generator for AC Service & AMC Billing"""
    
    def __init__(self):
        # Professional Color Scheme
        self.PRIMARY_COLOR = colors.HexColor('#1F4E79')      # Dark Blue
        self.SECONDARY_COLOR = colors.HexColor('#2E75B6')    # Medium Blue
        self.ACCENT_COLOR = colors.HexColor('#5B9BD5')       # Light Blue
        self.LIGHT_BG = colors.HexColor('#E3F2FD')           # Very Light Blue
        self.HEADER_BG = colors.HexColor('#4472C4')          # Blue Header
        self.TOTAL_BG = colors.HexColor('#FFC000')           # Yellow/Orange
        self.BALANCE_BG = colors.HexColor('#C00000')         # Red for balance
        self.SUCCESS_COLOR = colors.HexColor('#059669')      # Green (Paid)
        self.WARNING_COLOR = colors.HexColor('#D97706')      # Amber (Pending)
        self.BORDER_COLOR = colors.HexColor('#000000')       # Black
        self.TEXT_DARK = colors.HexColor('#000000')          # Black
        self.TEXT_MEDIUM = colors.HexColor('#333333')        # Dark Gray
        self.TEXT_LIGHT = colors.HexColor('#666666')         # Gray
        self.WHITE = colors.HexColor('#FFFFFF')
        
        self.styles = getSampleStyleSheet()
        self._setup_fonts_and_styles()
    
    def _setup_fonts_and_styles(self):
        """Setup fonts and styles - Clean Professional Style"""
        # Use Helvetica for clean professional look
        self.FONT_NORMAL = 'Helvetica'
        self.FONT_BOLD = 'Helvetica-Bold'

        # Professional Color Scheme - Minimal
        self.PRIMARY_COLOR = colors.black
        self.SECONDARY_COLOR = colors.HexColor('#333333')
        self.LIGHT_GREY = colors.HexColor('#CCCCCC')
        self.BORDER_COLOR = colors.black
        self.TEXT_DARK = colors.black
        self.TEXT_MEDIUM = colors.HexColor('#555555')
        self.TEXT_LIGHT = colors.HexColor('#777777')
        self.WHITE = colors.white
        self.HEADER_BG = colors.HexColor('#F0F0F0')  # Light grey for headers
        self.TOTAL_BG = colors.HexColor('#F5F5F5')  # Very light grey for totals

        # Custom Paragraph Styles
        self.styles.add(ParagraphStyle(
            name='CompanyName',
            parent=self.styles['Heading1'],
            fontName=self.FONT_BOLD,
            fontSize=24,
            textColor=self.TEXT_DARK,
            spaceAfter=2,
            alignment=TA_LEFT,
            leading=28
        ))

        self.styles.add(ParagraphStyle(
            name='CompanyTagline',
            parent=self.styles['Normal'],
            fontName=self.FONT_NORMAL,
            fontSize=9,
            textColor=self.TEXT_MEDIUM,
            spaceAfter=8,
            alignment=TA_LEFT,
            leading=11
        ))

        self.styles.add(ParagraphStyle(
            name='InvoiceTitle',
            parent=self.styles['Heading2'],
            fontName=self.FONT_BOLD,
            fontSize=22,
            textColor=self.TEXT_DARK,
            spaceAfter=3,
            alignment=TA_RIGHT,
            leading=26
        ))

        self.styles.add(ParagraphStyle(
            name='InvoiceNumber',
            parent=self.styles['Normal'],
            fontName=self.FONT_BOLD,
            fontSize=10,
            textColor=self.TEXT_DARK,
            spaceAfter=2,
            alignment=TA_RIGHT,
            leading=12
        ))

        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Normal'],
            fontName=self.FONT_BOLD,
            fontSize=9,
            textColor=self.TEXT_DARK,
            spaceAfter=2,
            spaceBefore=2,
            alignment=TA_LEFT,
            leading=11
        ))

        self.styles.add(ParagraphStyle(
            name='SectionLabel',
            parent=self.styles['Normal'],
            fontName=self.FONT_BOLD,
            fontSize=8,
            textColor=self.TEXT_DARK,
            spaceAfter=1,
            leading=10
        ))

        self.styles.add(ParagraphStyle(
            name='Label',
            parent=self.styles['Normal'],
            fontName=self.FONT_BOLD,
            fontSize=7,
            textColor=self.TEXT_MEDIUM,
            spaceAfter=1,
            leading=9
        ))

        self.styles.add(ParagraphStyle(
            name='Value',
            parent=self.styles['Normal'],
            fontName=self.FONT_NORMAL,
            fontSize=8,
            textColor=self.TEXT_DARK,
            spaceAfter=1,
            leading=10
        ))

        self.styles.add(ParagraphStyle(
            name='ValueBold',
            parent=self.styles['Normal'],
            fontName=self.FONT_BOLD,
            fontSize=9,
            textColor=self.TEXT_DARK,
            spaceAfter=2,
            leading=11
        ))

        self.styles.add(ParagraphStyle(
            name='TableHeader',
            parent=self.styles['Normal'],
            fontName=self.FONT_BOLD,
            fontSize=8,
            textColor=self.TEXT_DARK,
            alignment=TA_CENTER,
            leading=10
        ))

        self.styles.add(ParagraphStyle(
            name='TableCell',
            parent=self.styles['Normal'],
            fontName=self.FONT_NORMAL,
            fontSize=8,
            textColor=self.TEXT_DARK,
            alignment=TA_LEFT,
            leading=10
        ))

        self.styles.add(ParagraphStyle(
            name='TableCellRight',
            parent=self.styles['Normal'],
            fontName=self.FONT_NORMAL,
            fontSize=8,
            textColor=self.TEXT_DARK,
            alignment=TA_RIGHT,
            leading=10
        ))

        self.styles.add(ParagraphStyle(
            name='TableCellCenter',
            parent=self.styles['Normal'],
            fontName=self.FONT_NORMAL,
            fontSize=8,
            textColor=self.TEXT_DARK,
            alignment=TA_CENTER,
            leading=10
        ))

        self.styles.add(ParagraphStyle(
            name='TotalLabel',
            parent=self.styles['Normal'],
            fontName=self.FONT_BOLD,
            fontSize=9,
            textColor=self.TEXT_DARK,
            alignment=TA_RIGHT,
            leading=11
        ))

        self.styles.add(ParagraphStyle(
            name='GrandTotal',
            parent=self.styles['Normal'],
            fontName=self.FONT_BOLD,
            fontSize=11,
            textColor=self.TEXT_DARK,
            alignment=TA_RIGHT,
            leading=14
        ))

        self.styles.add(ParagraphStyle(
            name='BalanceDue',
            parent=self.styles['Normal'],
            fontName=self.FONT_BOLD,
            fontSize=11,
            textColor=self.TEXT_DARK,
            alignment=TA_RIGHT,
            leading=14
        ))

        self.styles.add(ParagraphStyle(
            name='Terms',
            parent=self.styles['Normal'],
            fontName=self.FONT_NORMAL,
            fontSize=7,
            textColor=self.TEXT_LIGHT,
            spaceAfter=1,
            leading=9
        ))

        self.styles.add(ParagraphStyle(
            name='FooterText',
            parent=self.styles['Normal'],
            fontName=self.FONT_BOLD,
            fontSize=9,
            textColor=self.TEXT_DARK,
            alignment=TA_CENTER,
            leading=11
        ))

        self.styles.add(ParagraphStyle(
            name='SignatureText',
            parent=self.styles['Normal'],
            fontName=self.FONT_BOLD,
            fontSize=9,
            textColor=self.TEXT_DARK,
            alignment=TA_RIGHT,
            leading=11
        ))
    
    def generate_invoice(self, invoice_data, shop_data, output_path):
        """
        Generate professional A4 GST-compliant invoice PDF
        
        Args:
            invoice_data: dict containing all invoice fields
            shop_data: dict containing shop/company details
            output_path: str path to save PDF
        """
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=20*mm,
            leftMargin=20*mm,
            topMargin=15*mm,
            bottomMargin=15*mm,
            title=f"Invoice {invoice_data.get('invoice_no', 'N/A')}"
        )
        
        story = []
        
        # 1. Company Header with Logo
        story.extend(self._create_company_header(shop_data, invoice_data))
        story.append(Spacer(1, 6*mm))
        
        # 2. Customer & Service/AC Details Section
        story.extend(self._create_customer_service_section(invoice_data))
        story.append(Spacer(1, 6*mm))
        
        # 3. Item Details Table
        story.extend(self._create_items_table(invoice_data))
        story.append(Spacer(1, 6*mm))
        
        # 4. GST & Tax Summary
        story.extend(self._create_tax_summary(invoice_data))
        story.append(Spacer(1, 6*mm))
        
        # 5. Payment Details
        story.extend(self._create_payment_section(invoice_data))
        story.append(Spacer(1, 6*mm))
        
        # 6. AMC Details (if applicable)
        if invoice_data.get('invoice_type') == 'AMC':
            story.extend(self._create_amc_section(invoice_data))
            story.append(Spacer(1, 6*mm))
        
        # 7. Notes & Terms
        story.extend(self._create_notes_terms(invoice_data))
        story.append(Spacer(1, 5*mm))
        
        # 8. Footer with Signature
        story.extend(self._create_footer(shop_data))
        
        doc.build(story)
        print(f"[OK] Professional PDF generated: {output_path}")
    
    def _create_company_header(self, shop_data, invoice_data):
        """Create company header - Clean Professional Layout (No Emojis)"""
        elements = []

        logo_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'assets',
            'Logo.png'
        )

        # ============================================================================
        # MAIN HEADER TABLE: Logo + Company Info (Left) | Invoice Details (Right)
        # ============================================================================
        header_table_data = []

        # --- LEFT SIDE: Logo + Company Name ---
        left_content = []

        # Logo
        if os.path.exists(logo_path):
            try:
                logo = Image(logo_path, width=20*mm, height=20*mm)
                left_content.append(logo)
            except:
                left_content.append(Paragraph('[LOGO]', self.styles['Normal']))
        else:
            left_content.append(Paragraph('[LOGO]', self.styles['Normal']))

        # Company Name (Bold & Large)
        company_name = shop_data.get('shop_name', 'ANSH AIR COOL')
        tagline = shop_data.get('tagline', 'AC Service & AMC Solutions')

        company_text = f"""
        <para alignment="left">
        <font size="22" color="#000000"><b>{company_name}</b></font><br/>
        <font size="9" color="#555555">{tagline}</font>
        </para>
        """
        left_content.append(Paragraph(company_text, self.styles['Normal']))

        # --- RIGHT SIDE: Invoice Details (Right Aligned) ---
        invoice_no = invoice_data.get('invoice_no', 'N/A')
        invoice_date = invoice_data.get('invoice_date', 'N/A')
        due_date = invoice_data.get('due_date', 'N/A')
        payment_status = invoice_data.get('payment_status', 'Pending')

        status_text = payment_status.upper()

        right_content = f"""
        <para alignment="right">
        <font size="20" color="#000000"><b>INVOICE</b></font><br/>
        <font size="11" color="#000000"><b>#{invoice_no}</b></font><br/>
        <font size="8" color="#555555">Date: {invoice_date}</font><br/>
        <font size="8" color="#555555">Due: {due_date}</font><br/>
        <font size="9" color="#000000"><b>Status: {status_text}</b></font>
        </para>
        """

        # Combine into header table row
        header_table_data.append([left_content[0], left_content[1], Paragraph(right_content, self.styles['Normal'])])

        # Create header table
        header_table = Table(header_table_data, colWidths=[23*mm, 97*mm, 60*mm])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (0,0), (0,0), 'LEFT'),
            ('ALIGN', (1,0), (1,0), 'LEFT'),
            ('ALIGN', (2,0), (2,0), 'RIGHT'),
            ('PADDING', (0,0), (-1,-1), 3),
        ]))
        elements.append(header_table)

        # ============================================================================
        # HORIZONTAL LINE SEPARATOR
        # ============================================================================
        line_table = Table([[Paragraph('', self.styles['Normal'])]], colWidths=[180*mm])
        line_table.setStyle(TableStyle([
            ('LINEBELOW', (0,0), (-1,-1), 1, self.BORDER_COLOR),
            ('TOPPADDING', (0,0), (-1,-1), 5),
        ]))
        elements.append(line_table)
        elements.append(Spacer(1, 2*mm))

        # ============================================================================
        # SHOP ADDRESS (Below Company Name, Above Line)
        # ============================================================================
        address = shop_data.get('address', 'Address not available')
        phone = shop_data.get('phone', shop_data.get('mobile', 'N/A'))
        email = shop_data.get('email', 'N/A')
        gstin = shop_data.get('gstin', '')

        address_text = f"""
        <para alignment="left">
        <font size="8" color="#000000"><b>{address}</b></font><br/>
        <font size="7" color="#555555">Phone: {phone} | Email: {email}</font>
        """

        if gstin:
            address_text += f'<br/><font size="7" color="#555555">GSTIN: {gstin}</font>'

        address_text += '</para>'
        elements.append(Paragraph(address_text, self.styles['Value']))

        return elements
    
    def _create_customer_service_section(self, invoice_data):
        """Create Customer Details and Service/AC Details section - Clean Professional"""
        elements = []

        # Two column layout
        section_data = [
            # Headers
            [
                Paragraph('BILL TO:', self.styles['SectionHeader']),
                Paragraph('SERVICE & AC DETAILS', self.styles['SectionHeader'])
            ],
            # Content
            [
                self._create_customer_block(invoice_data),
                self._create_service_block(invoice_data)
            ]
        ]

        section_table = Table(section_data, colWidths=[90*mm, 90*mm])
        section_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ]))
        elements.append(section_table)

        return elements

    def _create_customer_block(self, invoice_data):
        """Create customer details block - Clean without emojis"""
        customer_name = invoice_data.get('customer_name', 'N/A')
        mobile = invoice_data.get('customer_mobile', 'N/A')
        email = invoice_data.get('customer_email', 'N/A')
        address = invoice_data.get('customer_address', 'N/A')
        landmark = invoice_data.get('landmark', '')

        # Add customer complaint if available
        complaint = invoice_data.get('complaint', '')

        customer_data = [
            [Paragraph(f"<b>{customer_name}</b>", self.styles['ValueBold'])],
            [Paragraph(f"Mobile: {mobile}", self.styles['Value'])],
        ]

        if email and email != 'N/A':
            customer_data.append([Paragraph(f"Email: {email}", self.styles['Value'])])

        customer_data.append([Paragraph(f"Address: {address}", self.styles['Value'])])

        if landmark:
            customer_data.append([Paragraph(f"Landmark: {landmark}", self.styles['Value'])])

        # Add customer complaint/issue if available
        if complaint and complaint != 'N/A':
            customer_data.append([Paragraph('', self.styles['Value'])])  # Spacer
            customer_data.append([Paragraph(f"<b>Complaint:</b>", self.styles['SectionLabel'])])
            customer_data.append([Paragraph(f"{complaint}", self.styles['Value'])])

        customer_table = Table(customer_data, colWidths=[85*mm])
        customer_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('PADDING', (0,0), (-1,-1), 2),
        ]))

        return customer_table

    def _create_service_block(self, invoice_data):
        """Create service and AC details block - Clean without emojis"""
        # Get service details
        technician = invoice_data.get('technician_name', 'N/A')
        technician_mobile = invoice_data.get('technician_mobile', 'N/A')
        service_date = invoice_data.get('service_date', 'N/A')
        invoice_type = invoice_data.get('invoice_type', 'Regular')
        service_type = invoice_data.get('service_type', 'AC Service')

        # AC Details
        ac_brand = invoice_data.get('ac_brand', 'N/A')
        ac_type = invoice_data.get('ac_type', 'N/A')
        ac_ton = invoice_data.get('ac_ton', 'N/A')
        ac_star = invoice_data.get('ac_star', 'N/A')
        ac_inverter = invoice_data.get('ac_inverter', 'N/A')
        ac_gas = invoice_data.get('ac_gas', 'N/A')
        ac_serial = invoice_data.get('ac_serial', 'N/A')

        service_data = [
            [
                Paragraph('<b>Technician:</b>', self.styles['Label']),
                Paragraph(f"{technician}", self.styles['Value'])
            ],
            [
                Paragraph('<b>Contact:</b>', self.styles['Label']),
                Paragraph(f"{technician_mobile}", self.styles['Value'])
            ],
            [
                Paragraph('<b>Service Date:</b>', self.styles['Label']),
                Paragraph(f"{service_date}", self.styles['Value'])
            ],
            [
                Paragraph('<b>Invoice Type:</b>', self.styles['Label']),
                Paragraph(f"{invoice_type}", self.styles['Value'])
            ],
            [
                Paragraph('<b>Service Type:</b>', self.styles['Label']),
                Paragraph(f"{service_type}", self.styles['Value'])
            ],
            [Paragraph('', self.styles['Value']), Paragraph('', self.styles['Value'])],  # Spacer
            [
                Paragraph('<b>AC Brand:</b>', self.styles['Label']),
                Paragraph(f"{ac_brand}", self.styles['Value'])
            ],
            [
                Paragraph('<b>Type:</b>', self.styles['Label']),
                Paragraph(f"{ac_type}", self.styles['Value'])
            ],
            [
                Paragraph('<b>Capacity:</b>', self.styles['Label']),
                Paragraph(f"{ac_ton}", self.styles['Value'])
            ],
            [
                Paragraph('<b>Star Rating:</b>', self.styles['Label']),
                Paragraph(f"{ac_star}", self.styles['Value'])
            ],
            [
                Paragraph('<b>Inverter:</b>', self.styles['Label']),
                Paragraph(f"{ac_inverter}", self.styles['Value'])
            ],
            [
                Paragraph('<b>Gas Type:</b>', self.styles['Label']),
                Paragraph(f"{ac_gas}", self.styles['Value'])
            ],
        ]

        # Add serial number if available
        if ac_serial and ac_serial != 'N/A':
            service_data.append([
                Paragraph('<b>Serial No:</b>', self.styles['Label']),
                Paragraph(f"{ac_serial}", self.styles['Value'])
            ])

        service_table = Table(service_data, colWidths=[35*mm, 48*mm])
        service_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('PADDING', (0,0), (-1,-1), 2),
        ]))

        return service_table
    
    def _create_items_table(self, invoice_data):
        """Create item details table - Clean Professional (No HSN, No Colors)"""
        elements = []

        # Table headers (HSN/SAC column removed)
        items_data = [[
            Paragraph('<b>SR.</b>', self.styles['TableHeader']),
            Paragraph('<b>DESCRIPTION</b>', self.styles['TableHeader']),
            Paragraph('<b>QTY</b>', self.styles['TableHeader']),
            Paragraph('<b>RATE</b>', self.styles['TableHeader']),
            Paragraph('<b>GST %</b>', self.styles['TableHeader']),
            Paragraph('<b>AMOUNT</b>', self.styles['TableHeader'])
        ]]

        # Add items
        items = invoice_data.get('items', [])
        for i, item in enumerate(items, 1):
            description = item.get('service_name') or item.get('part_name') or item.get('description', 'N/A')
            quantity = item.get('quantity', item.get('qty', 1))
            rate = float(item.get('rate', 0))
            gst_percent = float(item.get('gst_percent', item.get('gst', 18)))
            amount = float(item.get('amount', quantity * rate))

            items_data.append([
                Paragraph(str(i), self.styles['TableCellCenter']),
                Paragraph(description, self.styles['TableCell']),
                Paragraph(str(quantity), self.styles['TableCellCenter']),
                Paragraph(f"Rs. {rate:,.2f}", self.styles['TableCellRight']),
                Paragraph(f"{gst_percent}%", self.styles['TableCellCenter']),
                Paragraph(f"Rs. {amount:,.2f}", self.styles['TableCellRight'])
            ])

        # Create table
        items_table = Table(items_data, colWidths=[
            12*mm, 80*mm, 18*mm, 25*mm, 20*mm, 25*mm
        ])
        items_table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0,0), (-1,0), self.HEADER_BG),
            ('GRID', (0,0), (-1,-1), 0.5, self.BORDER_COLOR),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('FONTNAME', (0,0), (-1,-1), self.FONT_BOLD),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('PADDING', (0,0), (-1,-1), 5),

            # Data rows
            ('BACKGROUND', (0,1), (-1,-1), self.WHITE),
            ('ALIGN', (2,0), (-1,-1), 'RIGHT'),
            ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ]))

        elements.append(items_table)
        return elements
    
    def _create_tax_summary(self, invoice_data):
        """Create GST and tax summary - Clean Right Aligned Block"""
        elements = []

        subtotal = float(invoice_data.get('subtotal', 0))
        cgst_rate = float(invoice_data.get('cgst_rate', 9))
        cgst_amount = float(invoice_data.get('cgst_amount', 0))
        sgst_amount = float(invoice_data.get('sgst_amount', cgst_amount))
        igst_amount = float(invoice_data.get('igst_amount', 0))
        total_tax = cgst_amount + sgst_amount + igst_amount
        total = float(invoice_data.get('total', subtotal + total_tax))
        advance = float(invoice_data.get('amount_paid', 0))
        balance = float(invoice_data.get('balance_due', total - advance))

        sgst_rate = float(invoice_data.get('sgst_rate', cgst_rate))

        # Build summary data
        summary_data = []

        # CGST
        summary_data.append([
            Paragraph(f'CGST @ {cgst_rate}%:', self.styles['Label']),
            Paragraph(f"Rs. {cgst_amount:,.2f}", self.styles['TableCellRight'])
        ])

        # SGST
        summary_data.append([
            Paragraph(f'SGST @ {sgst_rate}%:', self.styles['Label']),
            Paragraph(f"Rs. {sgst_amount:,.2f}", self.styles['TableCellRight'])
        ])

        # Add IGST if applicable
        if igst_amount > 0:
            igst_rate = float(invoice_data.get('igst_rate', 18))
            summary_data.append([
                Paragraph(f'IGST @ {igst_rate}%:', self.styles['Label']),
                Paragraph(f"Rs. {igst_amount:,.2f}", self.styles['TableCellRight'])
            ])

        # Total Tax
        summary_data.append([
            Paragraph('<b>Total Tax:</b>', self.styles['TotalLabel']),
            Paragraph(f"<b>Rs. {total_tax:,.2f}</b>", self.styles['TotalLabel'])
        ])

        # Grand Total
        summary_data.append([
            Paragraph('<b>Grand Total:</b>', self.styles['GrandTotal']),
            Paragraph(f"<b>Rs. {total:,.2f}</b>", self.styles['GrandTotal'])
        ])

        # Advance Paid
        summary_data.append([
            Paragraph('Advance Paid:', self.styles['Label']),
            Paragraph(f"Rs. {advance:,.2f}", self.styles['TableCellRight'])
        ])

        # Balance Due
        summary_data.append([
            Paragraph('<b>Balance Due:</b>', self.styles['BalanceDue']),
            Paragraph(f"<b>Rs. {balance:,.2f}</b>", self.styles['BalanceDue'])
        ])

        summary_table = Table(summary_data, colWidths=[100*mm, 60*mm])
        summary_table.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, self.BORDER_COLOR),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('FONTNAME', (0,0), (-1,-1), self.FONT_NORMAL),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('PADDING', (0,0), (-1,-1), 4),
            ('ALIGN', (1,0), (1,-1), 'RIGHT'),
            ('BACKGROUND', (0,0), (-1,-1), self.WHITE),
        ]))

        elements.append(summary_table)
        return elements
    
    def _create_payment_section(self, invoice_data):
        """Create payment details section - Clean"""
        elements = []

        payment_mode = invoice_data.get('payment_mode', 'N/A')
        payment_status = invoice_data.get('payment_status', 'Pending')
        next_due_date = invoice_data.get('next_due_date', 'N/A')

        payment_data = [
            [Paragraph('<b>PAYMENT DETAILS</b>', self.styles['SectionHeader'])],
            [
                Paragraph(f"Payment Mode: {payment_mode}", self.styles['Value']),
                Paragraph(f"Status: {payment_status}", self.styles['Value'])
            ],
        ]

        # Add next due date for partial payments
        if payment_status == 'Partial' and next_due_date != 'N/A':
            payment_data.append([
                Paragraph(f"Next Due Date: {next_due_date}", self.styles['Value'])
            ])

        payment_table = Table(payment_data, colWidths=[160*mm])
        payment_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), self.HEADER_BG),
            ('GRID', (0,0), (-1,-1), 0.5, self.BORDER_COLOR),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('PADDING', (0,0), (-1,-1), 5),
        ]))

        elements.append(payment_table)
        return elements
    
    def _create_amc_section(self, invoice_data):
        """Create AMC contract details section (if applicable)"""
        elements = []
        
        amc_id = invoice_data.get('amc_id', 'N/A')
        contract_type = invoice_data.get('contract_type', 'N/A')
        duration = invoice_data.get('duration', 'N/A')
        start_date = invoice_data.get('start_date', 'N/A')
        end_date = invoice_data.get('end_date', 'N/A')
        services_per_year = invoice_data.get('services_per_year', 'N/A')
        units_covered = invoice_data.get('units_covered', 'N/A')
        services_remaining = invoice_data.get('services_remaining', 'N/A')
        
        amc_data = [
            [Paragraph('<b>AMC CONTRACT DETAILS</b>', self.styles['SectionHeader'])],
            [
                Paragraph('<b>AMC ID:</b>', self.styles['Label']),
                Paragraph(amc_id, self.styles['Value']),
                Paragraph('<b>Contract Type:</b>', self.styles['Label']),
                Paragraph(contract_type, self.styles['Value'])
            ],
            [
                Paragraph('<b>Duration:</b>', self.styles['Label']),
                Paragraph(duration, self.styles['Value']),
                Paragraph('<b>Start Date:</b>', self.styles['Label']),
                Paragraph(start_date, self.styles['Value'])
            ],
            [
                Paragraph('<b>End Date:</b>', self.styles['Label']),
                Paragraph(end_date, self.styles['Value']),
                Paragraph('<b>Services/Year:</b>', self.styles['Label']),
                Paragraph(f"{services_per_year} services", self.styles['Value'])
            ],
            [
                Paragraph('<b>Units Covered:</b>', self.styles['Label']),
                Paragraph(units_covered, self.styles['Value']),
                Paragraph('<b>Services Remaining:</b>', self.styles['Label']),
                Paragraph(f"{services_remaining} services", self.styles['Value'])
            ],
        ]
        
        amc_table = Table(amc_data, colWidths=[40*mm, 50*mm, 40*mm, 50*mm])
        amc_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), self.ACCENT_COLOR),
            ('GRID', (0,0), (-1,-1), 0.5, self.BORDER_COLOR),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('PADDING', (0,0), (-1,-1), 4),
            ('BACKGROUND', (0,1), (-1,-1), self.LIGHT_BG),
        ]))
        
        elements.append(amc_table)
        return elements
    
    def _create_notes_terms(self, invoice_data):
        """Create notes and terms & conditions section - Clean"""
        elements = []

        notes = invoice_data.get('notes', 'Thank you for your business!')
        terms = invoice_data.get('terms', [])

        # Default terms if none provided
        if not terms:
            terms = [
                "Goods once sold will not be taken back.",
                "Interest @18% p.a. will be charged if payment not made within due date.",
                "All disputes subject to local jurisdiction only."
            ]

        notes_terms_data = [
            [Paragraph('<b>NOTES:</b>', self.styles['SectionHeader'])],
            [Paragraph(notes, self.styles['Value'])],
            [Paragraph('', self.styles['Terms'])],
            [Paragraph('<b>TERMS & CONDITIONS:</b>', self.styles['SectionHeader'])],
        ]

        # Add terms
        for term in terms:
            notes_terms_data.append([Paragraph(term, self.styles['Terms'])])

        notes_table = Table(notes_terms_data, colWidths=[160*mm])
        notes_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), self.HEADER_BG),
            ('BACKGROUND', (0,3), (-1,3), self.HEADER_BG),
            ('GRID', (0,0), (-1,-1), 0.5, self.BORDER_COLOR),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('PADDING', (0,0), (-1,-1), 4),
        ]))

        elements.append(notes_table)
        return elements

    def _create_footer(self, shop_data):
        """Create footer with thank you message and signature - Clean"""
        elements = []

        # Thank you message
        footer_data = [
            [Paragraph('THANK YOU FOR YOUR BUSINESS!', self.styles['FooterText'])]
        ]

        footer_table = Table(footer_data, colWidths=[160*mm])
        footer_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('PADDING', (0,0), (-1,-1), 8),
            ('BACKGROUND', (0,0), (-1,-1), self.HEADER_BG),
            ('BOX', (0,0), (-1,-1), 0.5, self.BORDER_COLOR),
        ]))
        elements.append(footer_table)

        # Signature section
        elements.append(Spacer(1, 10*mm))

        signature_text = f"""
        <para alignment="right">
        <br/>
        _______________________<br/>
        <b>Authorized Signatory</b><br/>
        <font size="8" color="#555555">{shop_data.get('shop_name', 'ANSH AIR COOL')}</font>
        </para>
        """
        elements.append(Paragraph(signature_text, self.styles['SignatureText']))

        return elements
