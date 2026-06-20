import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

function formatLabelTimestamp(rawTs) {
  try {
    if (!rawTs) return '--';
    const t = rawTs.replace(/-/g, '/');
    const dt = new Date(t);
    if (isNaN(dt.getTime())) return rawTs;
    const timeStr = dt.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true });
    const dateStr = dt.toLocaleDateString([], { month: 'short', day: 'numeric' });
    return `${dateStr} ${timeStr}`;
  } catch (e) { return rawTs; }
}

export default function TelemetryDashboard({ data }) {
  const telemetry = data?.telemetry || [];
  const sortedTelemetry = [...telemetry].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
  const latestTelemetry = sortedTelemetry.length > 0 ? sortedTelemetry[sortedTelemetry.length - 1] : null;

  const interpretations = data?.interpretations || [];
  const latestInterp = interpretations.length > 0 ? interpretations[0] : null;

  const vision = data?.vision || [];
  const latestVision = vision.length > 0 ? vision[0] : null;

  let vitalityPct = 100;
  let healthStatus = latestInterp?.health_status || 'UNKNOWN';
  if (healthStatus === 'STRESSED') vitalityPct = 75;
  if (healthStatus === 'CRITICAL') vitalityPct = 40;
  if (latestVision?.turgidity_score !== undefined && latestVision?.turgidity_score !== null) {
      vitalityPct = Math.round(latestVision.turgidity_score * 100);
  }

  const perimeter = 345.5;
  const offset = perimeter - (vitalityPct / 100) * perimeter;

  const labels = sortedTelemetry.map(t => formatLabelTimestamp(t.timestamp));

  const getChartOptions = (unit) => ({
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: {
          label: (context) => `${context.parsed.y}${unit}`
        }
      }
    },
    scales: {
      x: { 
        grid: { display: false },
        ticks: { color: '#8c968f', font: { size: 9 }, maxTicksLimit: 6, maxRotation: 0 }
      },
      y: { 
        grid: { color: 'rgba(0,0,0,0.04)', drawTicks: false },
        ticks: { 
          color: '#8c968f', 
          font: { size: 10 }, 
          maxTicksLimit: 6,
          callback: (value) => value + unit
        }
      }
    },
    elements: {
      point: { radius: 0, hitRadius: 10, hoverRadius: 4 }
    }
  });

  const createChartData = (label, dataset, color, bgColor) => ({
    labels,
    datasets: [
      {
        label,
        data: sortedTelemetry.map(t => t[dataset]),
        borderColor: color,
        backgroundColor: bgColor,
        borderWidth: 2,
        tension: 0.2,
        fill: true,
      }
    ]
  });

  return (
    <div className="dashboard-grid">
      
      {/* LEFT COLUMN */}
      <div className="col-left">
        <div className="framed-art">
          <div className="camera-frame">
            <img 
              id="latest-image" 
              src="./latest.jpg" 
              alt="Latest visual feed snapshot" 
              onError={(e) => { e.target.style.display = 'none'; }}
            />
          </div>
          <div className="image-timestamp">
            Lens: Optical Desk Capture {latestVision && `(${formatLabelTimestamp(latestVision.timestamp)})`}
          </div>
        </div>

        <div className="metric-list">
          <div className="metric-card">
            <div className="metric-icon-wrapper">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M12 22a7 7 0 0 0 7-7c0-4.3-7-11-7-11S5 10.7 5 15a7 7 0 0 0 7 7z"/></svg>
            </div>
            <div className="metric-details">
              <span className="metric-title">Soil Moisture</span>
              <span className="metric-subtitle">{latestTelemetry ? latestTelemetry.soil_moisture : '--'}</span>
            </div>
          </div>

          <div className="metric-card">
            <div className="metric-icon-wrapper">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z"/></svg>
            </div>
            <div className="metric-details">
              <span className="metric-title">Temperature</span>
              <span className="metric-subtitle">{latestTelemetry ? `${latestTelemetry.temp?.toFixed(1)}°C` : '--°C'}</span>
            </div>
          </div>

          <div className="metric-card">
            <div className="metric-icon-wrapper">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
            </div>
            <div className="metric-details">
              <span className="metric-title">Humidity</span>
              <span className="metric-subtitle">{latestTelemetry ? `${latestTelemetry.hum?.toFixed(0)}%` : '--%'}</span>
            </div>
          </div>

          <div className="metric-card">
            <div className="metric-icon-wrapper">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>
            </div>
            <div className="metric-details">
              <span className="metric-title">Light Lux</span>
              <span className="metric-subtitle">{latestTelemetry ? `${Number(latestTelemetry.light).toLocaleString()} lx` : '-- lx'}</span>
            </div>
          </div>
        </div>
      </div>

      {/* MIDDLE COLUMN */}
      <div className="col-middle">
        <div className="trend-card">
          <div className="trend-card-header"><h2 className="trend-card-title">Soil Moisture</h2></div>
          <div className="chart-wrapper">
            <Line options={getChartOptions('')} data={createChartData('Moisture', 'soil_moisture', '#67947d', 'rgba(103, 148, 125, 0.1)')} />
          </div>
        </div>
        <div className="trend-card">
          <div className="trend-card-header"><h2 className="trend-card-title">Temperature</h2></div>
          <div className="chart-wrapper">
            <Line options={getChartOptions('°C')} data={createChartData('Temperature', 'temp', '#ca6747', 'rgba(202, 103, 71, 0.1)')} />
          </div>
        </div>
        <div className="trend-card">
          <div className="trend-card-header"><h2 className="trend-card-title">Humidity</h2></div>
          <div className="chart-wrapper">
            <Line options={getChartOptions('%')} data={createChartData('Humidity', 'hum', '#5a655d', 'rgba(90, 101, 93, 0.1)')} />
          </div>
        </div>
        <div className="trend-card">
          <div className="trend-card-header"><h2 className="trend-card-title">Light Lux</h2></div>
          <div className="chart-wrapper">
            <Line options={getChartOptions(' lx')} data={createChartData('Lux', 'light', '#d09f5e', 'rgba(208, 159, 94, 0.1)')} />
          </div>
        </div>
      </div>

      {/* RIGHT COLUMN */}
      <div className="col-right">
        <div className="vitality-card">
          <h2 className="vitality-title">Plant Vitality</h2>
          <div className="vitality-ring-wrapper">
            <svg className="vitality-ring-svg" width="130" height="130">
              <circle className="vitality-ring-bg" cx="65" cy="65" r="55"></circle>
              <circle 
                className="vitality-ring-progress" 
                cx="65" cy="65" r="55"
                style={{ strokeDashoffset: offset }}
              ></circle>
            </svg>
            <div className="vitality-text-center">
              <span className="vitality-percentage">{vitalityPct}%</span>
              <span className="vitality-label-sub">Health</span>
            </div>
          </div>
          <div className="vitality-footer">Vitality: {healthStatus}</div>
        </div>

        <div className="status-card">
          <h2 className="status-card-header">Garden Status</h2>
          <div className="status-bot-badge">Garden Warden</div>
          <div className="agent-note-box">
            {latestInterp ? `"${latestInterp.interpretation || latestInterp.reasoning}"` : `"Connecting to gardenbot warden..."`}
          </div>
        </div>

        <div className="profile-card">
          <h2 className="status-card-header">Plant Profile</h2>
          <div className="spec-grid">
            <div className="spec-item"><strong>Stature</strong> 8cm & 7cm</div>
            <div className="spec-item"><strong>Pot</strong> 8x8 Terracotta</div>
            <div className="spec-item"><strong>VPD Target</strong> 0.8-1.5 kPa</div>
            <div className="spec-item"><strong>Climate</strong> 30-36°C Indoor</div>
          </div>
        </div>

        <div className="updated-card">
          <h2 className="updated-title">Last Updated</h2>
          <span className="updated-subtitle">Current Data</span>
          <div className="updated-time">
            {latestTelemetry ? formatLabelTimestamp(latestTelemetry.timestamp) : '--'}
          </div>
        </div>
      </div>

    </div>
  );
}
