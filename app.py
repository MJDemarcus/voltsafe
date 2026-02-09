import streamlit as st
import pandas as pd
import io
import datetime
from fpdf import FPDF
import xlsxwriter

# ==========================================
# 1. CONTENT CONFIGURATION (content.py)
# ==========================================
QUESTIONS = [
    {
        "id": "q1",
        "text": "What is the primary nature of your work?",
        "type": "radio",
        "options": [
            ("lv_install", "Electrical Installation (Low Voltage)"),
            ("hv_ops", "High Voltage (HV) Operations"),
            ("dc_maint", "Data Centre Maintenance"),
            ("solar", "Solar/Renewables")
        ],
        "risk_factor": "medium"
    },
    {
        "id": "q2",
        "text": "Will you be performing live electrical work?",
        "type": "radio",
        "options": [
            ("yes_frequent", "Yes, frequently"),
            ("yes_rare", "Yes, but rarely (Fault finding only)"),
            ("no_dead_only", "No, strictly dead work only")
        ],
        "risk_factor": "high"
    },
    {
        "id": "q3",
        "text": "Does your work involve confined spaces?",
        "type": "boolean",
        "risk_factor": "high"
    },
    {
        "id": "q4",
        "text": "Are you working in a live Data Centre environment?",
        "type": "boolean",
        "risk_factor": "critical"
    },
    {
        "id": "q5",
        "text": "Do you require a Permit to Work system?",
        "type": "boolean",
        "risk_factor": "medium"
    },
    {
        "id": "q6",
        "text": "Will you be using elevated work platforms (EWP)?",
        "type": "boolean",
        "risk_factor": "high"
    },
    {
        "id": "q7",
        "text": "Do you engage subcontractors?",
        "type": "boolean",
        "risk_factor": "low"
    },
    {
        "id": "q8",
        "text": "Is this for a specific Tier 1 Contractor audit?",
        "type": "radio",
        "options": [
            ("general", "No, general ISO 45001 compliance"),
            ("lendlease", "Yes, Lendlease"),
            ("multiplex", "Yes, Multiplex"),
            ("cpb", "Yes, CPB")
        ],
        "risk_factor": "low"
    }
]

CONTENT_BLOCKS = {
    "sms_core": {
        "title": "1.0 Safety Management System Core",
        "iso_ref": "ISO 45001:2018 Clause 5.2 (Policy)",
        "evidence": "Signed Safety Policy, Org Chart, Legal Register",
        "body": """
1.1 Leadership & Commitment
Top management is committed to preventing injury and ill health, maintaining compliance with legal requirements, and continually improving the OH&S management system.

1.2 Policy
VoltSafe Systems operates under a zero-harm policy. All work must stop if controls are not effective or if conditions change.
"""
    },
    "proc_hv_isolation": {
        "title": "2.1 High Voltage Isolation & Access",
        "iso_ref": "ISO 45001:2018 Clause 8.1.2 (Hazard Elimination)",
        "evidence": "Switching Schedule, Access Permit, Recipient in Charge Authority",
        "body": """
SCOPE: This procedure applies to all work on or near High Voltage (HV) apparatus.

MANDATORY CONTROLS:
1. Switching Program must be approved 48 hours prior.
2. Sanction to Test (STT) or Permit to Work (PTW) required.
3. Verifying Dead: Must use a tested Proximity Tester followed by Contact Tester.

WARNING: HV access requires specialized authorization. Unauthorized access is grounds for immediate termination.
"""
    },
    "proc_live_work": {
        "title": "2.2 Live Low Voltage Work Control",
        "iso_ref": "WHS Regulation 2017 Part 4.7",
        "evidence": "Live Work Permit, Rescue Kit Checklist, Observer Competency",
        "body": """
CRITICAL RISK WARNING: Live work is only permitted when de-energization introduces a greater risk.

REQUIREMENTS:
1. Live Work Permit signed by Director.
2. Rescue Kit (Hook + Resuscitation Mask) at the switching point.
3. Arc Flash PPE (Category 2 minimum) must be worn.
4. Safety Observer must be present and competent in LVR.
"""
    },
    "proc_confined_space": {
        "title": "2.3 Confined Space Entry",
        "iso_ref": "ISO 45001:2018 Clause 8.1.4.2 (Contractors)",
        "evidence": "Confined Space Permit, Gas Detector Calibration, Rescue Plan",
        "body": """
DEFINITION: Any enclosed or partially enclosed space working at atmospheric pressure.

ENTRY PROTOCOL:
1. Gas Test (O2, LEL, H2S, CO) prior to entry.
2. Mechanical Ventilation established.
3. Sentry / Standby Person at entry point.
4. Communication system tested and active.
"""
    },
    "proc_ewp": {
        "title": "2.4 Elevated Work Platform (EWP) Operations",
        "iso_ref": "AS/NZS 2550.10",
        "evidence": "EWP Logbook, Harness Inspection Tag, VOC",
        "body": """
1. Harness must be worn and attached to anchor point at all times in boom lifts.
2. Ground conditions must be assessed for stability.
3. Spotter required for all movements in congested areas.
"""
    },
    "proc_permit_to_work": {
        "title": "3.0 Permit to Work System",
        "iso_ref": "ISO 45001:2018 Clause 8.1.2",
        "evidence": "Completed PTW Register, Closed Permits",
        "body": """
All high-risk activities require a Permit to Work (PTW).

PERMIT TYPES:
- Hot Work
- Confined Space
- Excavation
- Live Electrical Work
- Work at Heights

A permit is only valid for one shift and must be closed out upon completion.
"""
    },
    "subcontractor_management": {
        "title": "4.0 Subcontractor Management",
        "iso_ref": "ISO 45001:2018 Clause 8.1.4",
        "evidence": "Subcontractor Insurances, SWMS Review Checklist",
        "body": """
All subcontractors must undergo the VoltSafe Prequalification process.
Evidence of insurances, SWMS, and competency must be verified before work commences.
"""
    },
    "client_lendlease_addendum": {
        "title": "APPENDIX A: Lendlease GMR Compliance",
        "iso_ref": "Lendlease GMRs v4.0",
        "evidence": "GMR Gap Analysis, Project Management Plan",
        "body": """
Specific controls for Lendlease Global Minimum Requirements (GMRs):
- GMR 4.1: Energy Isolation
- GMR 4.3: Work at Heights
(Refer to project specific management plan for details).
"""
    },
    "client_multiplex_addendum": {
        "title": "APPENDIX A: Multiplex Critical Risks",
        "iso_ref": "Multiplex CRS",
        "evidence": "CRS Checklist, Temporary Power Certificate",
        "body": """
Alignment with Multiplex Critical Risk Standards (CRS).
Focus on disconnect/reconnect procedures and temporary power.
"""
    }
}

# ==========================================
# 2. LOGIC ENGINE (logic.py)
# ==========================================
def calculate_risk_profile(answers):
    risk_score = 0
    flags = []

    q1 = answers.get("q1")
    q2 = answers.get("q2")
    q3 = answers.get("q3")
    q4 = answers.get("q4")

    if q2 in ["yes_frequent", "yes_rare"]:
        risk_score += 10
        flags.append({
            "id": "LIVE_WORK",
            "label": "LIVE ELECTRICAL WORK",
            "severity": "CRITICAL",
            "message": "Strict Prohibition / Permit Control Required"
        })

    if q4 is True:
        risk_score += 10
        flags.append({
            "id": "DC_ENV",
            "label": "LIVE DATA CENTRE ENVIRONMENT",
            "severity": "CRITICAL",
            "message": "Customer Service Level Agreement (SLA) Impact Risk"
        })

    if q1 == "hv_ops":
        risk_score += 5
        flags.append({
            "id": "HV_OPS",
            "label": "HIGH VOLTAGE OPERATIONS",
            "severity": "HIGH",
            "message": "High Voltage Rules & Authorization Required"
        })

    if q3 is True:
        risk_score += 5
        flags.append({
            "id": "CONFINED_SPACE",
            "label": "CONFINED SPACE ENTRY",
            "severity": "HIGH",
            "message": "Rescue Plan & Gas Monitoring Mandated"
        })

    level = "Low"
    if risk_score >= 10: level = "Critical"
    elif risk_score >= 5: level = "High"
    elif risk_score > 0: level = "Medium"

    return {"level": level, "score": risk_score, "flags": flags}

def generate_content_map(answers):
    return {
        "sms_core": True,
        "proc_hv_isolation": answers.get("q1") == 'hv_ops',
        "proc_live_work": answers.get("q2") != 'no_dead_only',
        "proc_confined_space": answers.get("q3") is True,
        "proc_ewp": answers.get("q6") is True,
        "proc_permit_to_work": (answers.get("q5") is True) or (answers.get("q4") is True),
        "subcontractor_management": answers.get("q7") is True,
        "client_lendlease_addendum": answers.get("q8") == 'lendlease',
        "client_multiplex_addendum": answers.get("q8") == 'multiplex',
    }

# ==========================================
# 3. PDF GENERATION (pdf_gen.py)
# ==========================================
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
    # 1. Determine Legislation based on State
    state = st.session_state.get('jurisdiction', 'nsw')
    leg_act = "Work Health and Safety Act 2011"
    leg_reg = "Work Health and Safety Regulation 2017"
    
    if state == "vic":
        leg_act = "Occupational Health and Safety Act 2004"
        leg_reg = "Occupational Health and Safety Regulations 2017"
    elif state == "wa":
        leg_act = "Work Health and Safety Act 2020"
        leg_reg = "Work Health and Safety (General) Regulations 2022"
    elif state == "qld":
        leg_act = "Work Health and Safety Act 2011"
        leg_reg = "Work Health and Safety Regulation 2011"

    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Arial", size=24)
    pdf.cell(200, 40, txt="Safety Management System", ln=True, align='C')
    
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt=f"Date: {datetime.date.today()}", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Jurisdiction: {state.upper()} ({leg_act})", ln=True, align='C')
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
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, txt=f"This Safety Management System is designed to comply with the {leg_act} and the {leg_reg}, alongside ISO 45001:2018 requirements.")
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Risk Profile & Critical Flags", ln=True, align='L')
    pdf.ln(5)

    if not risk_profile['flags']:
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="No critical risk flags detected.", ln=True, align='L')
    else:
        for flag in risk_profile['flags']:
            pdf.set_text_color(255, 0, 0)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(200, 10, txt=f"[{flag['severity']}] {flag['label']}", ln=True)
            
            # explicit director liability warning
            if flag['severity'] == 'CRITICAL':
                pdf.set_font("Arial", 'B', 10)
                pdf.cell(200, 6, txt="*** DIRECTOR LIABILITY WARNING: Failure to control this risk may result in prosecution.", ln=True)
            
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", size=11)
            pdf.multi_cell(0, 8, txt=flag['message'])
            pdf.ln(5)

    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="System Content", ln=True, align='L')
    pdf.ln(10)

    for key, is_active in content_map.items():
        if is_active and key in content_blocks:
            block = content_blocks[key]
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, txt=block['title'], ln=True)
            pdf.set_font("Arial", size=11)
            pdf.multi_cell(0, 7, txt=block['body'].strip())
            pdf.ln(10)

    return pdf.output(dest='S').encode('latin-1')

# ==========================================
# 4. EXCEL GENERATION (excel_gen.py)
# ==========================================
def generate_excel_matrix(risk_profile, content_map):
    output = io.BytesIO()
    summary_data = {
        "Metric": ["Generated Date", "Risk Level", "Risk Score"],
        "Value": [str(datetime.date.today()), risk_profile['level'], risk_profile['score']]
    }
    df_summary = pd.DataFrame(summary_data)

    matrix_rows = []
    for key, is_active in content_map.items():
        state = "INCLUDED" if is_active else "EXCLUDED"
        trigger = "Logic Rule"
        if "hv" in key: trigger = "High Voltage Ops"
        if "live" in key: trigger = "Live Work Answer"
        if "dc" in key or "permit" in key: trigger = "Environment / PTW Answer"
        
        # Fetch metadata directly from global CONTENT_BLOCKS
        block = CONTENT_BLOCKS.get(key, {})
        iso_ref = block.get('iso_ref', 'N/A')
        evidence = block.get('evidence', 'N/A')
        
        matrix_rows.append({
            "Module ID": key.upper(),
            "Module Name": key.replace("_", " ").upper(),
            "Status": state,
            "Compliance Ref": iso_ref,
            "Required Evidence": evidence,
            "Trigger": trigger
        })
    df_matrix = pd.DataFrame(matrix_rows)
    
    risk_rows = []
    for flag in risk_profile['flags']:
        risk_rows.append({
            "Severity": flag['severity'],
            "Risk Label": flag['label'],
            "Control Action": flag['message'],
            "Director Liability": "Potential" if flag['severity'] == "CRITICAL" else "Managed"

        })
    df_risks = pd.DataFrame(risk_rows)

    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_summary.to_excel(writer, sheet_name='Summary', index=False)
        df_matrix.to_excel(writer, sheet_name='Traceability_Matrix', index=False)
        if not df_risks.empty:
            df_risks.to_excel(writer, sheet_name='Risk_Register', index=False)
            
    return output.getvalue()

# ==========================================
# 5. UI CONTROLLER (app.py)
# ==========================================
st.set_page_config(page_title="VoltSafe Systems v1.3", page_icon="⚡", layout="centered")


st.markdown("""
<style>
    /* 1. FORCE THE SIDEBAR TEXT TO BE VISIBLE */
    /* This overrides the default that might be too dark */
    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    /* 2. MAKE HEADERS GREEN */
    h1, h2, h3, h4, h5, h6, strong {
        color: #00E676 !important;
    }

    /* 3. MAKE RADIO BUTTONS GREEN (AND TEXT WHITE) */
    div[role="radiogroup"] label > div:first-child[aria-checked="true"] {
        background-color: #00E676 !important;
        border-color: #00E676 !important;
    }
    /* Inner dot */
    div[role="radiogroup"] label > div:first-child[aria-checked="true"] > div {
        background-color: #000000 !important;
    }
    /* Text next to radio */
    div[role="radiogroup"] label p {
        color: #FFFFFF !important;
        font-weight: 500;
    }

    /* 4. BUTTONS - CLEAN AND CONTRAST */
    /* Primary (Green) */
    div.stButton > button:first-child {
        background-color: #00E676 !important;
        color: #000000 !important;
        font-weight: 800 !important;
        border: none !important;
        border-radius: 4px !important;
        transition: all 0.2s;
    }
    div.stButton > button:first-child:hover {
        transform: scale(1.02);
        background-color: #00C853 !important;
        box-shadow: 0 0 10px #00E676;
    }

    /* Secondary (Red) */
    div.stButton > button:nth-child(2) {
        background-color: #FF5252 !important;
        color: white !important;
        border-radius: 4px !important;
    }

    /* 5. METRICS & PROGRESS */
    [data-testid="stMetricValue"] {
        color: #00E676 !important;
    }
    .stProgress > div > div > div > div {
        background-color: #00E676 !important;
    }
</style>
""", unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 0
if 'answers' not in st.session_state: st.session_state.answers = {}

# Sidebar Configuration
with st.sidebar:
    st.header("Configuration")
    selected_state = st.selectbox(
        "Jurisdiction (State/Territory)",
        options=["NSW", "VIC", "QLD", "WA", "SA", "ACT", "NT", "TAS"],
        index=0
    )
    st.session_state['jurisdiction'] = selected_state.lower()
    st.info(f"Legislation will be set to {selected_state} standards.")
    
    with st.expander("ℹ️ About VoltSafe"):
        st.markdown("""
        **Why this exists:**
        Electrical contractors are failing audits not because they are unsafe, but because their systems are generic or not aligned with Tier-1 expectations.
        
        **Goal:** 
        To prevent failed audits, delayed mobilisation, and unmanaged legal exposure for directors.
        """)

st.markdown("### VoltSafe<span style='color:#00ff9d'>.SYSTEMS</span>", unsafe_allow_html=True)

def next_step(): st.session_state.step += 1
def prev_step(): st.session_state.step -= 1
def reset_app():
    st.session_state.step = 0
    st.session_state.answers = {}

steps = QUESTIONS
total = len(steps)

if st.session_state.step < total:
    curr = steps[st.session_state.step]
    st.progress(st.session_state.step / total)
    st.markdown("---")
    st.subheader(curr['text'])
    
    key = curr['id']
    existing = st.session_state.answers.get(key)
    val = None
    
    if curr['type'] == 'radio':
        opts_map = {o[0]: o[1] for o in curr['options']}
        rev_map = {v: k for k, v in opts_map.items()}
        lbls = list(opts_map.values())
        idx = 0
        if existing and existing in opts_map: idx = lbls.index(opts_map[existing])
        sel = st.radio("Select:", lbls, index=idx)
        val = rev_map[sel]
    elif curr['type'] == 'boolean':
        opts = ["Yes", "No"]
        idx = 0 if existing is True else 1
        sel = st.radio("Select:", opts, index=idx)
        val = True if sel == "Yes" else False
        
    st.markdown("---")
    c1, c2 = st.columns([1, 1])
    with c1:
        if st.session_state.step > 0: st.button("Back", on_click=prev_step)
    with c2:
        if st.button("Next"):
            st.session_state.answers[key] = val
            next_step()
            st.rerun()
else:
    st.progress(1.0)
    st.success("Assessment Complete")
    
    risk = calculate_risk_profile(st.session_state.answers)
    content_map = generate_content_map(st.session_state.answers)
    
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Risk Level", risk['level'])
    with c2: st.metric("Risk Score", risk['score'])
    with c3:
        state = st.session_state.get('jurisdiction', 'nsw').upper()
        st.metric("Jurisdiction", state)
    
    if risk['flags']:
        st.error("### ⚠ High Audit Risk Detected")
        for f in risk['flags']:
            st.markdown(f"**[{f['severity']}] {f['label']}**")
            st.caption(f['message'])
            
    st.markdown("### Generated Modules")
    act = [k.replace("_", " ").upper() for k, v in content_map.items() if v]
    st.dataframe(pd.DataFrame(act, columns=["Module"]), use_container_width=True)
    
    st.markdown("### Export")
    c1, c2 = st.columns(2)
    with c1:
        pdf_data = generate_sms_pdf(st.session_state.answers, risk, content_map, CONTENT_BLOCKS)
        st.download_button("Download PDF", pdf_data, "VoltSafe_SMS.pdf", "application/pdf")
    with c2:
        xls_data = generate_excel_matrix(risk, content_map)
        st.download_button("Download Excel", xls_data, "VoltSafe_Matrix.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        
    if st.button("Start Over"):
        reset_app()
        st.rerun()
