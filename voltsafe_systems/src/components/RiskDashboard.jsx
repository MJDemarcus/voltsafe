import React from 'react';

export default function RiskDashboard({ riskProfile, contentMap, onGenerateDocs }) {
    const { level, score, flags } = riskProfile;

    const getLevelColor = (l) => {
        switch (l) {
            case 'Critical': return '#ff3333';
            case 'High': return '#ff8800';
            case 'Medium': return '#ffcc00';
            default: return 'var(--color-text-accent)';
        }
    };

    return (
        <div className="risk-dashboard" style={{ animation: 'fadeIn 0.5s ease-out' }}>
            <div className="dashboard-grid" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>

                {/* Risk Score Card */}
                <div className="card" style={{ borderColor: getLevelColor(level) }}>
                    <h3 style={{ borderBottom: '1px solid var(--color-border)', paddingBottom: '12px', marginBottom: '20px' }}>
                        Risk Profile
                    </h3>
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                        <div>
                            <div style={{ fontSize: '3rem', fontWeight: 700, color: getLevelColor(level) }}>
                                {level.toUpperCase()}
                            </div>
                            <div style={{ color: 'var(--color-text-secondary)' }}>Audit Risk Level</div>
                        </div>
                        <div style={{ textAlign: 'right' }}>
                            <div style={{ fontSize: '2rem', fontWeight: 600 }}>{score}</div>
                            <div style={{ color: 'var(--color-text-secondary)' }}>Risk Score</div>
                        </div>
                    </div>
                </div>

                {/* Modules Card */}
                <div className="card">
                    <h3 style={{ borderBottom: '1px solid var(--color-border)', paddingBottom: '12px', marginBottom: '20px' }}>
                        Generated Modules
                    </h3>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                        {Object.entries(contentMap).map(([key, active]) => (
                            active && (
                                <div key={key} style={{
                                    padding: '8px 12px',
                                    background: 'var(--color-bg-tertiary)',
                                    borderRadius: '4px',
                                    fontSize: '0.85rem',
                                    borderLeft: '2px solid var(--color-text-accent)'
                                }}>
                                    {key.replace(/_/g, ' ').toUpperCase()}
                                </div>
                            )
                        ))}
                    </div>
                </div>
            </div>

            {/* Critical Flags */}
            {flags.length > 0 && (
                <div className="card" style={{ marginTop: '24px', background: 'rgba(255, 51, 51, 0.05)', borderColor: '#ff3333' }}>
                    <h3 style={{ color: '#ff3333', marginBottom: '16px' }}>⚠ High Audit Risk Detected</h3>
                    <div style={{ display: 'grid', gap: '12px' }}>
                        {flags.map((flag, idx) => (
                            <div key={idx} style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
                                <span style={{
                                    background: '#ff3333',
                                    color: 'black',
                                    padding: '4px 8px',
                                    borderRadius: '4px',
                                    fontWeight: 700,
                                    fontSize: '0.8rem'
                                }}>{flag.severity}</span>
                                <div>
                                    <div style={{ fontWeight: 600 }}>{flag.label}</div>
                                    <div style={{ fontSize: '0.9rem', color: 'var(--color-text-secondary)' }}>{flag.message}</div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            <div style={{ marginTop: '40px', textAlign: 'center', display: 'flex', gap: '20px', justifyContent: 'center' }}>
                <button className="btn-primary" onClick={onGenerateDocs} style={{ padding: '16px 32px', fontSize: '1.1rem' }}>
                    Download Audit Pack (PDF)
                </button>
                <button className="btn-secondary" onClick={onGenerateMatrix} style={{
                    padding: '16px 32px',
                    fontSize: '1.1rem',
                    background: 'transparent',
                    border: '1px solid var(--color-border)',
                    color: 'var(--color-text-primary)',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    fontWeight: 600
                }}>
                    Export Matrix (Excel)
                </button>
            </div>
        </div>
    );
}
