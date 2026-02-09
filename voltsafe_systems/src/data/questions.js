export const questions = [
    {
        id: "q1",
        text: "What is the primary nature of your work?",
        type: "radio",
        options: [
            { label: "Electrical Installation (Low Voltage)", value: "lv_install" },
            { label: "High Voltage (HV) Operations", value: "hv_ops" },
            { label: "Data Centre Maintenance", value: "dc_maint" },
            { label: "Solar/Renewables", value: "solar" }
        ],
        riskFactor: "medium"
    },
    {
        id: "q2",
        text: "Will you be performing live electrical work?",
        type: "radio",
        options: [
            { label: "Yes, frequently", value: "yes_frequent" },
            { label: "Yes, but rarely (Fault finding only)", value: "yes_rare" },
            { label: "No, strictly dead work only", value: "no_dead_only" }
        ],
        riskFactor: "high"
    },
    {
        id: "q3",
        text: "Does your work involve confined spaces?",
        type: "boolean", // Render as Yes/No radio
        riskFactor: "high"
    },
    {
        id: "q4",
        text: "Are you working in a live Data Centre environment?",
        type: "boolean",
        riskFactor: "critical"
    },
    {
        id: "q5",
        text: "Do you require a Permit to Work system?",
        type: "boolean",
        riskFactor: "medium"
    },
    {
        id: "q6",
        text: "Will you be using elevated work platforms (EWP)?",
        type: "boolean",
        riskFactor: "high"
    },
    {
        id: "q7",
        text: "Do you engage subcontractors?",
        type: "boolean",
        riskFactor: "low"
    },
    {
        id: "q8",
        text: "Is this for a specific Tier 1 Contractor audit?",
        type: "radio",
        options: [
            { label: "No, general ISO 45001 compliance", value: "general" },
            { label: "Yes, Lendlease", value: "lendlease" },
            { label: "Yes, Multiplex", value: "multiplex" },
            { label: "Yes, CPB", value: "cpb" }
        ],
        riskFactor: "low"
    }
];
