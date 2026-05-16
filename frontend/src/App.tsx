import React, { useState } from 'react';
import './styles/App.css';
import Dashboard from './components/Dashboard';
import PredictPage from './pages/PredictPage';
import CarePage from './pages/CarePage';

const tabs = [
  { key: 'dashboard', label: 'Dashboard' },
  { key: 'predict', label: 'Prediction' },
  { key: 'care', label: 'Care & Treatment' },
];

function App() {
  const [activeTab, setActiveTab] = useState('care');

  return (
    <div className="App">
      <div className="app-shell">
        <header className="app-topbar">
          <div className="brand-block">
            <div className="brand-mark">🌿</div>
            <div>
              <p className="brand-label">GeoSense</p>
              <h1>Plant Care Suite</h1>
            </div>
          </div>
          <nav className="top-navigation">
            {tabs.map((tab) => (
              <button
                key={tab.key}
                className={`nav-pill ${activeTab === tab.key ? 'active' : ''}`}
                onClick={() => setActiveTab(tab.key)}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        </header>

        <main className="app-content">
          {activeTab === 'dashboard' && <Dashboard />}
          {activeTab === 'predict' && (
            <section className="section-shell">
              <div className="section-header">
                <span className="eyebrow">Live prediction</span>
                <h2>Instant plant diagnosis from image uploads</h2>
              </div>
              <PredictPage />
            </section>
          )}
          {activeTab === 'care' && <CarePage />}
        </main>
      </div>
    </div>
  );
}

export default App;
