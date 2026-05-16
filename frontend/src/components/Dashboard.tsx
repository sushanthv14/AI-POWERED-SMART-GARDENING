import React from 'react';
import '../styles/Dashboard.css';

const stats = [
  {
    label: 'Model accuracy',
    value: '93%',
    icon: '🌿',
    description: 'Confident disease detection on real plant leaves',
  },
  {
    label: 'Plant classes',
    value: '38',
    icon: '🍅',
    description: 'All major crop diseases and healthy classes supported',
  },
  {
    label: 'Live predictions',
    value: 'Ready',
    icon: '⚡',
    description: 'Upload photos and get instant plant health insights',
  },
  {
    label: 'Dashboard mode',
    value: 'Interactive',
    icon: '📊',
    description: 'One place for predictions, insights and recommendations',
  },
];

const Dashboard: React.FC = () => {
  return (
    <section className="dashboard-shell">
      <div className="hero-panel">
        <div className="hero-copy">
          <span className="eyebrow">Smart Gardening Dashboard</span>
          <h1>Grow smarter with AI-powered plant disease detection</h1>
          <p>
            Convert plant images into actionable care guidance. Upload a leaf photo and receive a disease prediction, confidence score, and next-step recommendation instantly.
          </p>
          <div className="hero-actions">
            <a href="#prediction" className="hero-cta">
              Start analysis
            </a>
            <a href="#insights" className="hero-secondary">
              See insights
            </a>
          </div>
        </div>
        <div className="hero-overview-card">
          <div className="overview-header">
            <span>Live status</span>
            <strong>All systems green</strong>
          </div>
          <div className="overview-metric">
            <span>Pipeline uptime</span>
            <strong>99.9%</strong>
          </div>
          <div className="overview-metric">
            <span>API latency</span>
            <strong>120ms</strong>
          </div>
          <div className="overview-note">Ready for your demo.</div>
        </div>
      </div>

      <div className="stats-grid" id="insights">
        {stats.map((item) => (
          <div className="stat-card" key={item.label}>
            <div className="stat-icon">{item.icon}</div>
            <div className="stat-body">
              <p className="stat-value">{item.value}</p>
              <p className="stat-label">{item.label}</p>
              <p className="stat-description">{item.description}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default Dashboard;
