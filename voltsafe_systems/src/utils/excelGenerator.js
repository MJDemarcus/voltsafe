import * as XLSX from 'xlsx';

export function generateTraceabilityMatrix(completedData, riskProfile, contentMap) {
    // 1. Prepare Data for Matrix
    const rows = [
        ["VoltSafe Systems - Compliance Traceability Matrix"],
        ["Generated Date", new Date().toLocaleDateString()],
        ["Risk Level", riskProfile.level],
        ["Risk Score", riskProfile.score],
        [],
        ["Requirement ID", "Module Name", "Status", "Trigger Condition"]
    ];

    // Map content to rows
    Object.entries(contentMap).forEach(([key, isActive]) => {
        let trigger = "Standard Requirement";

        // Reverse engineer trigger reason for traceability
        if (key === 'proc_hv_isolation') trigger = "High Voltage Ops Selected";
        if (key === 'proc_live_work') trigger = "Live Work Selected";
        if (key === 'proc_confined_space') trigger = "Confined Space Selected";
        if (key === 'proc_ewp') trigger = "EWP Selected";
        if (key === 'client_lendlease_addendum') trigger = "Lendlease Audit Selected";

        rows.push([
            key.toUpperCase(),
            key.replace(/_/g, ' ').toUpperCase(),
            isActive ? "INCLUDED" : "EXCLUDED",
            isActive ? trigger : "N/A"
        ]);
    });

    // Add Critical Risks Section
    rows.push([]);
    rows.push(["CRITICAL RISK FLAGS"]);
    rows.push(["Severity", "Risk Description", "Control Action"]);

    riskProfile.flags.forEach(flag => {
        rows.push([flag.severity, flag.label, flag.message]);
    });

    // 2. Create Sheet
    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.aoa_to_sheet(rows);

    // Column Widths
    const wscols = [
        { wch: 25 },
        { wch: 40 },
        { wch: 15 },
        { wch: 40 }
    ];
    ws['!cols'] = wscols;

    XLSX.utils.book_append_sheet(wb, ws, "Traceability_Matrix");

    // 3. Save File
    XLSX.writeFile(wb, "VoltSafe_Traceability_Matrix.xlsx");
}
