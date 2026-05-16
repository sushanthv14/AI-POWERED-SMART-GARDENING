import React from 'react';
import '../styles/CarePage.css';

const timeline = [
  {
    step: '1',
    title: 'Diagnosis Review',
    description: 'Confirm the identified disease and severity before starting treatment.',
  },
  {
    step: '2',
    title: 'Targeted Care Steps',
    description: 'Apply precision watering, pruning, and nutrient support to accelerate recovery.',
  },
  {
    step: '3',
    title: 'Soil + Microbiome Boost',
    description: 'Use gentle organic amendments to restore healthy soil biology.',
  },
  {
    step: '4',
    title: 'Follow-up Check',
    description: 'Reassess after 5 days and adjust the care plan as needed.',
  },
];

const sparklinePoints = '0,40 25,32 50,48 75,36 100,52 125,44 150,58 175,50 200,62';

const CarePage: React.FC = () => {
  return (
    <div className="care-page">
      <section className="care-hero-card glass-card">
        <div className="hero-copy">
          <span className="eyebrow">Care & Treatment</span>
          <h2>Plant recovery simplified with expert AI guidance.</h2>
          <p>
            A premium care page that blends plant diagnostics, treatment sequencing, and personalized follow-up in one calm interface.
          </p>
        </div>

        <div className="diagnosis-hero">
          <div className="diagnosis-top">
            <div>
              <p className="diagnosis-label">Diagnosis</p>
              <h3>Tomato | Early Blight</h3>
              <p className="diagnosis-note">A fungal infection detected at early stage. Immediate treatment reduces spread and preserves yield.</p>
            </div>
            <div className="gauge-card">
              <div className="gauge-ring">
                <span className="gauge-value">93%</span>
              </div>
              <p className="gauge-label">Confidence</p>
            </div>
          </div>

          <div className="diagnosis-details">
            <div>
              <p>Risk Level</p>
              <strong>Moderate</strong>
            </div>
            <div>
              <p>Priority</p>
              <strong>Urgent care</strong>
            </div>
            <div>
              <p>Recommended action</p>
              <strong>Fungicide + hydration</strong>
            </div>
          </div>
        </div>
      </section>

      <div className="care-layout">
        <section className="timeline-card glass-card">
          <div className="section-header">
            <div>
              <span>Recovery Timeline</span>
              <h3>4-step treatment plan</h3>
            </div>
            <button className="pill-button">Edit plan</button>
          </div>
          <div className="timeline-list">
            {timeline.map((item) => (
              <div className="timeline-step" key={item.step}>
                <div className="timeline-badge">{item.step}</div>
                <div>
                  <h4>{item.title}</h4>
                  <p>{item.description}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        <aside className="aside-column">
          <section className="score-card glass-card">
            <span className="eyebrow">Care Score</span>
            <h3>Growth momentum</h3>
            <div className="score-visual">
              <svg viewBox="0 0 200 80" preserveAspectRatio="none">
                <polyline
                  points={sparklinePoints}
                  fill="none"
                  stroke="#2563eb"
                  strokeWidth="3"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
              <div className="score-summary">
                <strong>87</strong>
                <p>Healthy growth rating</p>
              </div>
            </div>
          </section>

          <section className="expert-card glass-card">
            <div className="expert-header">
              <div>
                <span>Plant Doctor</span>
                <h3>AI expert advice</h3>
              </div>
            </div>
            <div className="expert-chats">
              <div className="chat-item received">
                <p>Hi! I recommend applying natural copper spray and improving airflow around the tomato plant.</p>
              </div>
              <div className="chat-item sent">
                <p>What is the best schedule for follow-up care?</p>
              </div>
              <div className="chat-item received">
                <p>Repeat inspections every 3 days, and if spots shrink, switch to maintenance watering only.</p>
              </div>
            </div>
            <button className="chat-action">Ask the Plant Doctor</button>
          </section>
        </aside>
      </div>
    </div>
  );
};

export default CarePage;
