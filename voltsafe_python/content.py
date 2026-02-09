# Question Schema
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

# Content Blocks for SMS
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
