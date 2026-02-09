import React from 'react';

export default function WizardContainer({ questions, onComplete }) {
    const [currentStep, setCurrentStep] = React.useState(0);
    const [answers, setAnswers] = React.useState({});
    const [direction, setDirection] = React.useState('forward');

    const handleAnswer = (questionId, value) => {
        setAnswers(prev => ({ ...prev, [questionId]: value }));
    };

    const handleNext = () => {
        if (currentStep < questions.length - 1) {
            setDirection('forward');
            setCurrentStep(prev => prev + 1);
        } else {
            onComplete(answers);
        }
    };

    const handleBack = () => {
        if (currentStep > 0) {
            setDirection('back');
            setCurrentStep(prev => prev - 1);
        }
    };

    const currentQuestion = questions[currentStep];
    const progress = ((currentStep + 1) / questions.length) * 100;

    return (
        <div className="wizard-container" style={{ maxWidth: '600px', margin: '0 auto' }}>
            {/* Progress Bar */}
            <div className="progress-track" style={{
                height: '4px',
                background: 'var(--color-bg-tertiary)',
                borderRadius: '2px',
                marginBottom: '40px'
            }}>
                <div className="progress-fill" style={{
                    width: `${progress}%`,
                    height: '100%',
                    background: 'var(--color-text-accent)',
                    borderRadius: '2px',
                    transition: 'width 0.3s ease-out'
                }} />
            </div>

            {/* Question Card */}
            <div className="card question-card" style={{ padding: '40px', minHeight: '300px', display: 'flex', flexDirection: 'column' }}>
                <h2 style={{ marginBottom: '30px', color: 'var(--color-text-primary)' }}>
                    {currentQuestion.text}
                </h2>

                <div className="options-grid" style={{ display: 'grid', gap: '15px', flexGrow: 1 }}>
                    <QuestionInput
                        question={currentQuestion}
                        value={answers[currentQuestion.id]}
                        onChange={(val) => handleAnswer(currentQuestion.id, val)}
                    />
                </div>

                <div className="wizard-actions" style={{ marginTop: '40px', display: 'flex', justifyContent: 'space-between' }}>
                    <button
                        onClick={handleBack}
                        disabled={currentStep === 0}
                        style={{
                            background: 'transparent',
                            border: 'none',
                            color: 'var(--color-text-secondary)',
                            cursor: currentStep === 0 ? 'not-allowed' : 'pointer',
                            opacity: currentStep === 0 ? 0.5 : 1
                        }}
                    >
                        ← Back
                    </button>

                    <button
                        className="btn-primary"
                        onClick={handleNext}
                        disabled={!answers[currentQuestion.id]}
                        style={{
                            opacity: !answers[currentQuestion.id] ? 0.5 : 1,
                            cursor: !answers[currentQuestion.id] ? 'not-allowed' : 'pointer'
                        }}
                    >
                        {currentStep === questions.length - 1 ? 'Generate System' : 'Next →'}
                    </button>
                </div>
            </div>
        </div>
    );
}

function QuestionInput({ question, value, onChange }) {
    if (question.type === 'radio' || question.type === 'boolean') {
        const options = question.type === 'boolean'
            ? [{ label: 'Yes', value: true }, { label: 'No', value: false }]
            : question.options;

        return options.map((opt) => (
            <label
                key={opt.value.toString()}
                style={{
                    display: 'flex',
                    alignItems: 'center',
                    padding: '15px 20px',
                    background: value === opt.value ? 'rgba(0, 255, 157, 0.1)' : 'var(--color-bg-tertiary)',
                    border: `1px solid ${value === opt.value ? 'var(--color-text-accent)' : 'var(--color-border)'}`,
                    borderRadius: 'var(--radius-md)',
                    cursor: 'pointer',
                    transition: 'all 0.2s',
                    color: value === opt.value ? 'var(--color-text-accent)' : 'var(--color-text-primary)'
                }}
                onMouseEnter={(e) => {
                    if (value !== opt.value) e.currentTarget.style.borderColor = 'var(--color-text-secondary)';
                }}
                onMouseLeave={(e) => {
                    if (value !== opt.value) e.currentTarget.style.borderColor = 'var(--color-border)';
                }}
            >
                <input
                    type="radio"
                    name={question.id}
                    value={opt.value}
                    checked={value === opt.value}
                    onChange={() => onChange(opt.value)}
                    style={{ marginRight: '15px', accentColor: 'var(--color-text-accent)' }}
                />
                {opt.label}
            </label>
        ));
    }
    return null;
}
