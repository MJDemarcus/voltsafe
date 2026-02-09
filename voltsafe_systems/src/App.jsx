import { useState } from 'react'
import WizardContainer from './components/WizardContainer'
import RiskDashboard from './components/RiskDashboard'
import { questions } from './data/questions'
import { calculateRiskProfile, generateContentMap } from './logic/engine'
import './index.css'

import { generateSMSPDF } from './utils/pdfGenerator'
import { generateTraceabilityMatrix } from './utils/excelGenerator'

function App() {
    const [hasStarted, setHasStarted] = useState(false)
    const [completedData, setCompletedData] = useState(null)
    const [riskProfile, setRiskProfile] = useState(null)
    const [contentMap, setContentMap] = useState(null)

    const handleComplete = (data) => {
        const risk = calculateRiskProfile(data)
        const map = generateContentMap(data)

        setCompletedData(data)
        setRiskProfile(risk)
        setContentMap(map)
    }

    const handleDownload = () => {
        generateSMSPDF(completedData, riskProfile, contentMap);
    }

    const handleDownloadMatrix = () => {
        generateTraceabilityMatrix(completedData, riskProfile, contentMap);
    }

    return (
        <div className="app-container">
            <header style={{
                padding: '20px 40px',
                borderBottom: '1px solid var(--color-border)',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                background: 'rgba(10, 10, 10, 0.8)',
                backdropFilter: 'blur(10px)',
                position: 'sticky',
                top: 0,
                zIndex: 100
            }}>
                <div style={{ fontWeight: 700, fontSize: '1.2rem', letterSpacing: '-0.02em' }}>
                    VoltSafe<span style={{ color: 'var(--color-text-accent)' }}>.SYSTEMS</span>
                </div>
                <div className="status-indicator" style={{
                    fontSize: '0.8rem',
                    color: 'var(--color-text-secondary)',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px'
                }}>
                    <span style={{
                        width: '8px',
                        height: '8px',
                        borderRadius: '50%',
                        background: 'var(--color-text-accent)',
                        boxShadow: '0 0 10px rgba(0, 255, 157, 0.5)'
                    }} />
                    SYSTEM ONLINE
                </div>
            </header>

            <main className="container" style={{ marginTop: '60px', paddingBottom: '60px' }}>
                {!hasStarted ? (
                    <div className="card" style={{ textAlign: 'center', padding: '60px 40px' }}>
                        <h1 style={{ fontSize: '2.5rem', marginBottom: '20px', color: 'var(--color-text-primary)' }}>Compliance. Simplified.</h1>
                        <p style={{ fontSize: '1.1rem', maxWidth: '600px', margin: '0 auto 40px auto', color: 'var(--color-text-secondary)' }}>
                            Generate audit-ready Safety Management Systems for Data Centre access.
                            ISO 45001 aligned. <span style={{ color: 'var(--color-text-accent)' }}>100% Deterministic.</span>
                        </p>
                        <button className="btn-primary" style={{ fontSize: '1.1rem', padding: '16px 40px' }} onClick={() => setHasStarted(true)}>
                            Initialize Intake Sequence
                        </button>
                    </div>
                ) : !completedData ? (
                    <WizardContainer questions={questions} onComplete={handleComplete} />
                ) : (
                    <RiskDashboard
                        riskProfile={riskProfile}
                        contentMap={contentMap}
                        onGenerateDocs={handleDownload}
                        onGenerateMatrix={handleDownloadMatrix}
                    />
                )}
            </main>
        </div>
    )
}

export default App
