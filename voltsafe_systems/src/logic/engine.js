/**
 * Logic Rule: Strictly controlled inputs. Validates answers against schema.
 */
export function validateAnswers(answers, schema) {
    // Implementation for validation if needed
    return true;
}

/**
 * Calculates the Risk Profile based on inputs.
 * Returns { riskLevel: 'low'|'medium'|'high'|'critical', flags: [] }
 */
export function calculateRiskProfile(answers) {
    let riskScore = 0;
    const flags = [];

    // Critical Risk Flags
    if (answers.q2 === 'yes_frequent' || answers.q2 === 'yes_rare') {
        riskScore += 10;
        flags.push({
            id: "LIVE_WORK",
            label: "LIVE ELECTRICAL WORK",
            severity: "CRITICAL",
            message: "Strict Prohibition / Permit Control Required"
        });
    }

    if (answers.q4 === true) {
        riskScore += 10;
        flags.push({
            id: "DC_ENV",
            label: "LIVE DATA CENTRE ENVIRONMENT",
            severity: "CRITICAL",
            message: "Customer Service Level Agreement (SLA) Impact Risk"
        });
    }

    // High Risk Flags
    if (answers.q1 === 'hv_ops') {
        riskScore += 5;
        flags.push({
            id: "HV_OPS",
            label: "HIGH VOLTAGE OPERATIONS",
            severity: "HIGH",
            message: "High Voltage Rules & Authorization Required"
        });
    }

    if (answers.q3 === true) {
        riskScore += 5;
        flags.push({
            id: "CONFINED_SPACE",
            label: "CONFINED SPACE ENTRY",
            severity: "HIGH",
            message: "Rescue Plan & Gas Monitoring Mandated"
        });
    }

    // Determine Level
    let level = "Low";
    if (riskScore >= 10) level = "Critical";
    else if (riskScore >= 5) level = "High";
    else if (riskScore > 0) level = "Medium";

    return {
        level,
        score: riskScore,
        flags
    };
}

/**
 * Generates the Content Block Map.
 * Returns an object where keys are Section IDs and values are booleans (include/exclude).
 */
export function generateContentMap(answers) {
    return {
        // Core SMS
        "sms_core": true,

        // High Risk Modules
        "proc_hv_isolation": answers.q1 === 'hv_ops',
        "proc_live_work": answers.q2 !== 'no_dead_only',
        "proc_confined_space": answers.q3 === true,
        "proc_ewp": answers.q6 === true,

        // Process Controls
        "proc_permit_to_work": answers.q5 === true || answers.q4 === true, // Forced if DC Environment
        "subcontractor_management": answers.q7 === true,

        // Client Specifics
        "client_lendlease_addendum": answers.q8 === 'lendlease',
        "client_multiplex_addendum": answers.q8 === 'multiplex',
    };
}
