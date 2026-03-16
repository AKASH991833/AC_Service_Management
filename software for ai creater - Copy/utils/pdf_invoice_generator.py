"""
Simple PDF Invoice Generator
Basic but Clean Design - WORKS PERFECTLY
FREE - Uses ReportLab library
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import os


class PDFInvoiceGenerator:
    """Generate simple PDF invoices"""
    
    def __init__(self, output_path="invoices_pdf/"):
        self.output_path = output_path
        self.styles = getSampleStyleSheet()
        
        # Create custom styles
        self.company_style = ParagraphStyle(
            'Company',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a237e'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            spaceAfter=10
        )
        
        self.tagline_style = ParagraphStyle(
            'Tagline',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            spaceAfter=3
        )
        
        self.invoice_title_style = ParagraphStyle(
            'InvoiceTitle',
            parent=self.styles['Heading2'],
            fontSize=18,
            textColor=colors.HexColor('#1a237e'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            spaceAfter=15
        )
        
        self.section_style = ParagraphStyle(
            'Section',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#1a237e'),
            fontName='Helvetica-Bold',
            spaceAfter=8
        )
        
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=9,
            spaceAfter=4
        )
        
        self.footer_style = ParagraphStyle(
            'Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#757575')
        )
        
        # Create output directory
        if not os.path.exists(output_path):
            os.makedirs(output_path)
    
    def generate_invoice(self, invoice_data):
        """Generate PDF invoice"""
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
            bottomMargin=0.5*inch
        )
        
        # Build content
        story = []
        
        # 1. Company Header
        story.append(Paragraph("ANSH AIR COOL", self.company_style))
        story.append(Paragraph("AC Sales | Service | Installation | Repair", self.tagline_style))
        story.append(Paragraph("Phone: 9918331262", self.tagline_style))
        story.append(Spacer(1, 0.3*inch))
        
        # 2. Invoice Title
        story.append(Paragraph("INVOICE", self.invoice_title_style))
        
        # 3. Invoice Info
        info_data = [[
            f"Invoice No: {invoice_data['invoice_number']}",
            f"Date: {invoice_data['invoice_date']}"
        ]]
        info_table = Table(info_data, colWidths=[3.5*inch, 3.5*inch])
        info_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8eaf6')),
            ('BOX', (0, 0), (-1, 0), 1, colors.black),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('LEFTPADDING', (0, 0), (-1, 0), 15),
            ('RIGHTPADDING', (0, 0), (-1, 0), 15),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 0.25*inch))
        
        # 4. Customer Details
        customer_text = f"""
        <b>BILL TO:</b><br/>
        {invoice_data['customer_name']}<br/>
        {invoice_data['customer_address']}<br/>
        Mobile: {invoice_data['customer_mobile']}
        """
        story.append(Paragraph(customer_text, self.normal_style))
        story.append(Spacer(1, 0.2*inch))
        
        # 5. Items Table
        story.append(Paragraph("ITEMS & SERVICES", self.section_style))
        
        # Table data
        table_data = [
            ['Sr.', 'Description', 'Qty', 'Rate', 'Amount']
        ]
        
        for i, item in enumerate(invoice_data['items'], 1):
            table_data.append([
                str(i),
                item['description'],
                str(item['quantity']),
                f"Rs. {item['rate']:,.2f}",
                f"Rs. {item['amount']:,.2f}"
            ])
        
        items_table = Table(table_data, colWidths=[0.6*inch, 3.5*inch, 0.8*inch, 1.2*inch, 1.4*inch])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(items_table)
        story.append(Spacer(1, 0.25*inch))
        
        # 6. Payment Summary
        story.append(Paragraph("PAYMENT SUMMARY", self.section_style))
        
        totals_data = [
            ['Subtotal:', f"Rs. {invoice_data['subtotal']:,.2f}"],
            ['-' * 15, '-' * 12],
            ['TOTAL:', f"Rs. {invoice_data['total_amount']:,.2f}"],
        ]
        
        totals_table = Table(totals_data, colWidths=[4.5*inch, 2.5*inch])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('FONTNAME', (-1, -2), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (-1, -2), (-1, -1), 12),
            ('TEXTCOLOR', (-1, -2), (-1, -1), colors.HexColor('#1a237e')),
            ('BOTTOMPADDING', (0, -2), (-1, -1), 10),
            ('LINEABOVE', (0, -2), (-1, -2), 2, colors.black),
        ]))
        story.append(totals_table)
        story.append(Spacer(1, 0.2*inch))
        
        # 7. Payment Status
        status_data = [[
            f"Paid: Rs. {invoice_data['paid_amount']:,.2f}",
            f"Balance: Rs. {invoice_data['balance_amount']:,.2f}"
        ]]
        status_table = Table(status_data, colWidths=[3.5*inch, 3.5*inch])
        status_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('BOX', (0, 0), (-1, 0), 1, colors.black),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('LEFTPADDING', (0, 0), (-1, 0), 12),
            ('RIGHTPADDING', (0, 0), (-1, 0), 12),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]))
        story.append(status_table)
        story.append(Spacer(1, 0.25*inch))
        
        # 8. Terms & Conditions - COMMENTED OUT FOR NOW
        # story.append(Paragraph("TERMS & CONDITIONS", self.section_style))
        
        # terms = [
        #     "1. Goods once sold will not be taken back.",
        #     "2. Interest @18% p.a. will be charged on delayed payments.",
        #     "3. All disputes subject to local jurisdiction.",
        #     "4. Thank you for your business!"
        # ]
        # for term in terms:
        #     story.append(Paragraph(term, ParagraphStyle('T', fontSize=7, spaceAfter=3)))
        
        story.append(Spacer(1, 0.3*inch))
        
        # 9. Footer
        story.append(Paragraph("<b>ANSH AIR COOL</b><br/>Phone: 9918331262", self.footer_style))
        
        # Build PDF
        doc.build(story)
        
        return filepath


# Convenience function
def create_invoice_pdf(invoice_data, output_path="invoices_pdf/"):
    """Quick function to create invoice PDF"""
    generator = PDFInvoiceGenerator(output_path)
    return generator.generate_invoice(invoice_data)
