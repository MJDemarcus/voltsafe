export const contentBlocks = {
    sms_core: {
        title: "1.0 Safety Management System Core",
        body: `
      1.1 Leadership & Commitment
      Top management is committed to preventing injury and ill health, maintaining compliance with legal requirements, and continually improving the OH&S management system.

      1.2 Policy
      VoltSafe Systems operates under a zero-harm policy. All work must stop if controls are not effective or if conditions change.
    `
    },

    proc_hv_isolation: {
        title: "2.1 High Voltage Isolation & Access",
        body: `
      SCOPE: This procedure applies to all work on or near High Voltage (HV) apparatus.
      
      MANDATORY CONTROLS:
      1. Switching Program must be approved 48 hours prior.
      2. Sanction to Test (STT) or Permit to Work (PTW) required.
      3. Verifying Dead: Must use a tested Proximity Tester followed by Contact Tester.
      
      WARNING: HV access requires specialized authorization. Unauthorized access is grounds for immediate termination.
    `
    },

    proc_live_work: {
        title: "2.2 Live Low Voltage Work Control",
        body: `
      CRITICAL RISK WARNING: Live work is only permitted when de-energization introduces a greater risk.
      
      REQUIREMENTS:
      1. Live Work Permit signed by Director.
      2. Rescue Kit (Hook + Resuscitation Mask) at the switching point.
      3. Arc Flash PPE (Category 2 minimum) must be worn.
      4. Safety Observer must be present and competent in LVR.
    `
    },

    proc_confined_space: {
        title: "2.3 Confined Space Entry",
        body: `
      DEFINITION: Any enclosed or partially enclosed space working at atmospheric pressure.
      
      ENTRY PROTOCOL:
      1. Gas Test (O2, LEL, H2S, CO) prior to entry.
      2. Mechanical Ventilation established.
      3. Sentry / Standby Person at entry point.
      4. Communication system tested and active.
    `
    },

    proc_ewp: {
        title: "2.4 Elevated Work Platform (EWP) Operations",
        body: `
      1. Harness must be worn and attached to anchor point at all times in boom lifts.
      2. Ground conditions must be assessed for stability.
      3. Spotter required for all movements in congested areas.
    `
    },

    proc_permit_to_work: {
        title: "3.0 Permit to Work System",
        body: `
      All high-risk activities require a Permit to Work (PTW).
      
      PERMIT TYPES:
      - Hot Work
      - Confined Space
      - Excavation
      - Live Electrical Work
      - Work at Heights
      
      A permit is only valid for one shift and must be closed out upon completion.
    `
    },

    subcontractor_management: {
        title: "4.0 Subcontractor Management",
        body: `
      All subcontractors must undergo the VoltSafe Prequalification process.
      Evidence of insurances, SWMS, and competency must be verified before work commences.
    `
    },

    client_lendlease_addendum: {
        title: "APPENDIX A: Lendlease GMR Compliance",
        body: `
      Specific controls for Lendlease Global Minimum Requirements (GMRs):
      - GMR 4.1: Energy Isolation
      - GMR 4.3: Work at Heights
      (Refer to project specific management plan for details).
    `
    },

    client_multiplex_addendum: {
        title: "APPENDIX A: Multiplex Critical Risks",
        body: `
      Alignment with Multiplex Critical Risk Standards (CRS).
      Focus on disconnect/reconnect procedures and temporary power.
    `
    }
};
