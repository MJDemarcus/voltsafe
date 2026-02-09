from fpdf import FPDF
import datetime

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'VoltSafe Systems - Safety Management System', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_sms_pdf(answers, risk_profile, content_map, content_blocks):
    pdf = PDFReport()
    pdf.add_page()
    
    # Title Page
    pdf.set_font("Arial", size=24)
    pdf.cell(200, 40, txt="Safety Management System", ln=True, align='C')
    
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt=f"Date: {datetime.date.today()}", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Risk Level: {risk_profile['level']}", ln=True, align='C')
    pdf.ln(20)
    
    # Executive Summary (The WHY)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Executive Summary: Audit Readiness", ln=True, align='L')
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, txt="Electrical contractors entering Data Centres are often failing audits not because they are unsafe, but because their Safety Management Systems (SMS) are generic or not aligned with Tier-1 expectations.\n\nThis VoltSafe generated system is designed to provide specific, audit-ready documentation to demonstrate:\n1. Alignment with Client / Tier-1 expectations.\n2. Understanding of legal duties as PCBUs and officers.\n3. Traceability between client requirements, system controls, and evidence.")
    pdf.ln(10)
    
    # Legislation Section
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Legislative Framework", ln=True, align='L')
    pdf.ln(5)

    if not risk_profile['flags']:
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="No critical risk flags detected.", ln=True, align='L')
    else:
        for flag in risk_profile['flags']:
            pdf.set_text_color(255, 0, 0)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(200, 10, txt=f"[{flag['severity']}] {flag['label']}", ln=True)
            
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", size=11)
            pdf.multi_cell(0, 8, txt=flag['message'])
            pdf.ln(5)

    pdf.add_page()
    
    # Content Blocks
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="System Content", ln=True, align='L')
    pdf.ln(10)

    for key, is_active in content_map.items():
        if is_active and key in content_blocks:
            block = content_blocks[key]
            
            # Title
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, txt=block['title'], ln=True)
            
            # Body
            pdf.set_font("Arial", size=11)
            pdf.multi_cell(0, 7, txt=block['body'].strip())
            pdf.ln(10)

    return pdf.output(dest='S').encode('latin-1')
