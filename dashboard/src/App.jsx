import { useState, useEffect } from 'react';
import TelemetryDashboard from './components/TelemetryDashboard';
import TopologyMap from './components/TopologyMap';
import './index.css';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [data, setData] = useState({ telemetry: [], interpretations: [], vision: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('./data.json');
        if (response.ok) {
          const json = await response.json();
          setData(json);
        }
      } catch (err) {
        console.error("Failed to fetch data:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
    // Refresh every 30s
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="dashboard-container">
      <header>
        <div className="brand-title">gardenbot</div>
        <nav>
          <button 
            className={`nav-btn ${activeTab === 'dashboard' ? 'active' : ''}`} 
            onClick={() => setActiveTab('dashboard')}
          >
            Dashboard
          </button>
          <button 
            className={`nav-btn ${activeTab === 'architecture' ? 'active' : ''}`} 
            onClick={() => setActiveTab('architecture')}
          >
            Architecture
          </button>
        </nav>
      </header>

      <main>
        {loading ? (
          <div style={{ textAlign: 'center', padding: '4rem', color: 'var(--text-secondary)' }}>Loading telemetry...</div>
        ) : (
          <>
            <div className={`tab-pane ${activeTab === 'dashboard' ? 'active' : ''}`}>
              {activeTab === 'dashboard' && <TelemetryDashboard data={data} />}
            </div>
            <div className={`tab-pane ${activeTab === 'architecture' ? 'active' : ''}`}>
              {activeTab === 'architecture' && <TopologyMap />}
            </div>
          </>
        )}
      </main>
    </div>
  );
}

export default App;
