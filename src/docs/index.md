---
hide:
  - navigation
  - toc
---

<style>
/* Modern Glassmorphic Dashboard */
.md-content__inner { max-width: none !important; margin: 0 !important; padding: 1rem 2rem !important; }
.md-main__inner { max-width: none !important; }

/* Force Single Row UI */
h1 { display: none !important; }
.md-tabs { display: none !important; }
.status-header { display: none !important; }

.dash-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 1.5rem;
}
.dash-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
}
.val-large { font-size: 2.4em; font-weight: 800; letter-spacing: -0.02em; }
.label-sub { font-size: 0.7rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 0.6rem; display: block; font-weight: 600; }
.vision-container {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #334155;
    background: #000;
}
.chart-container {
    background: #1e293b;
    padding: 1.5rem;
    border-radius: 16px;
    border: 1px solid #334155;
    height: 380px;
    margin-top: 0.5rem;
}
.chart-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 2rem;
    margin-top: 1.5rem;
}
@media (min-width: 1200px) {
    .chart-grid { grid-template-columns: 1fr 1fr; }
    .chart-full { grid-column: span 2; }
}

.db-meter {
    background: #0f172a;
    height: 6px;
    border-radius: 3px;
    margin-top: 4px;
    overflow: hidden;
}
.db-fill {
    height: 100%;
    background: #10b981;
    transition: width 0.5s ease;
}
.stale-warning { color: #facc15; font-size: 0.65rem; font-weight: 700; margin-left: 8px; animation: pulse-stale 2s infinite; display: inline-flex; align-items: center; gap: 4px; }
@keyframes pulse-stale { 0% { opacity: 0.5; } 50% { opacity: 1; } 100% { opacity: 0.5; } }
</style>

<!-- Hidden Native Status Header (CSS display:none) -->
<div class="status-header">
    <span id="reg-status">SYNCHRONIZED</span>
    <span id="sync-status">--:--:--</span>
</div>

<div class="dash-grid">
    <!-- Atmosphere -->
    <div class="dash-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <span class="label-sub">🌡 ATMOMSPHERIC STATISTICS</span>
            <span id="val-state" style="font-size: 0.65rem; color: #4ade80; border: 1px solid #4ade80; padding: 1px 6px; border-radius: 4px; font-weight: bold;">STABLE</span>
        </div>
        <div style="display: flex; align-items: baseline; gap: 1.2rem; margin-top: 0.5rem;">
            <div style="color:#f97316;">
                <span id="val-temp" class="val-large">--</span><span style="font-size: 1rem; opacity: 0.7;">°C</span>
                <span id="stale-temp" class="stale-warning" style="display:none;">⚠️ STALE</span>
            </div>
            <div style="color:#0ea5e9;">
                <span id="val-hum" class="val-large">--</span><span style="font-size: 1rem; opacity: 0.7;">%</span>
                <span id="stale-hum" class="stale-warning" style="display:none;">⚠️ STALE</span>
            </div>
            <div style="color:#a855f7; margin-left: auto;"><span id="val-vpd" class="val-large">--</span><span style="font-size: 1rem; opacity: 0.7;"> kPa</span></div>
        </div>
        
        <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #334155; display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; font-size: 0.8rem;">
            <div>
                <span class="label-sub" style="font-size: 0.6rem; margin-bottom: 2px;">LIGHT INTENSITY</span>
                <span id="val-light" style="color:#f59e0b; font-weight: 700; font-size: 1.1rem;">--</span>
                <span id="stale-light" class="stale-warning" style="display:none; font-size: 0.55rem;">⚠️ STALE</span>
            </div>
            <div>
                <span class="label-sub" style="font-size: 0.6rem; margin-bottom: 2px;">ACOUSTIC FLOOR</span>
                <span id="val-db" style="color:#10b981; font-weight: 700; font-size: 1.1rem;">-- dB</span>
                <span id="stale-db" class="stale-warning" style="display:none; font-size: 0.55rem;">⚠️ STALE</span>
                <div class="db-meter"><div id="db-fill" class="db-fill" style="width: 0%"></div></div>
            </div>
            <div>
                <span class="label-sub" style="font-size: 0.6rem; margin-bottom: 2px;">AIR QUALITY (VOC)</span>
                <span id="val-gas" style="color:#a855f7; font-weight: 700; font-size: 1.1rem;">-- kΩ</span>
                <span id="stale-gas" class="stale-warning" style="display:none; font-size: 0.55rem;">⚠️ STALE</span>
            </div>
            <div>
                <span class="label-sub" style="font-size: 0.6rem; margin-bottom: 2px;">BARO PRESSURE</span>
                <span id="val-press" style="color:#f8fafc; font-weight: 700; font-size: 1.1rem;">-- hPa</span>
                <span id="stale-press" class="stale-warning" style="display:none; font-size: 0.55rem;">⚠️ STALE</span>
            </div>
        </div>
    </div>

    <!-- Vision -->
    <div class="dash-card">
        <span class="label-sub">📸 OPTICAL GROUND-TRUTH</span>
        <div class="vision-container">
            <img id="live-photo" src="https://raw.githubusercontent.com/surendranb/gardenbot/main/media/latest.jpg" style="width: 100%; aspect-ratio: 16/9; object-fit: cover;">
        </div>
    </div>
</div>

<div class="chart-grid">
    <!-- Chart: Atmosphere -->
    <div class="chart-full">
        <span class="label-sub">📊 ATMOSPHERIC DYNAMICS (48H)</span>
        <div class="chart-container">
            <canvas id="atmosChart"></canvas>
        </div>
    </div>

    <!-- Chart: Kinetic Registry -->
    <div>
        <span class="label-sub">🔊 KINETIC & CHEMICAL REGISTRY (48H)</span>
        <div class="chart-container">
            <canvas id="kineticChart"></canvas>
        </div>
    </div>

    <!-- Chart: Vitality -->
    <div>
        <span class="label-sub">📈 METABOLIC VITALITY (48H)</span>
        <div class="chart-container">
            <canvas id="vitalityChart"></canvas>
        </div>
    </div>
</div>

<h2 style="margin-top: 4rem !important; border-bottom: 1px solid #334155; padding-bottom: 10px;">The Warden's Ledger</h2>
<div id="warden-log-output" style="background: #0f172a; padding: 25px; border-radius: 12px; font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; line-height: 1.7; border: 1px solid #334155; color: #cbd5e1;">
    Accessing neural audit...
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.3.0/papaparse.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

<script>
    document.addEventListener("DOMContentLoaded", () => {
        // Inject Unified Single-Row Nav & Status into the MkDocs Top Header
        const headerInner = document.querySelector('.md-header__inner');
        if(headerInner) {
            const topBar = document.createElement('div');
            topBar.style.display = 'flex';
            topBar.style.alignItems = 'center';
            topBar.style.gap = '24px';
            topBar.style.marginLeft = 'auto'; // push right
            topBar.style.marginRight = '16px'; // before github logo
            topBar.style.fontSize = '0.85rem';
            
            topBar.innerHTML = `
                <a href="." style="color:#ffffff; font-weight:600; text-decoration:none">Dashboard</a>
                <a href="architecture/" style="color:#94a3b8; text-decoration:none">Architecture</a>
                <a href="gallery/" style="color:#94a3b8; text-decoration:none">Gallery</a>
                <div style="width:1px; height:15px; background:#334155;"></div>
                <div style="display:flex; gap:10px; align-items:center;">
                    <span style="font-weight:700; color:#f8fafc; letter-spacing:0.05em;">STATUS: <span id="nav-reg-status" style="color:#4ade80;">SYNC</span></span>
                    <span id="nav-sync-status" style="color:#4ade80; font-family:'JetBrains Mono', monospace; font-weight:bold;">--:--:--</span>
                </div>
            `;
            const sourceNode = document.querySelector('.md-header__source');
            if(sourceNode) {
                headerInner.insertBefore(topBar, sourceNode);
            } else {
                headerInner.appendChild(topBar);
            }
        }
    });

    const GITHUB_RAW = "https://raw.githubusercontent.com/surendranb/gardenbot/main/";
    const CSV_METRICS = GITHUB_RAW + "data/metrics.csv";
    const CSV_TELEMETRY = GITHUB_RAW + "data/telemetry.csv";
    const CSV_WEATHER = GITHUB_RAW + "data/weather.csv";

    // V3 Palette
    const PALETTE = {
        temp: '#f97316', hum: '#0ea5e9', light: '#f59e0b',
        db: '#10b981', voc: '#a855f7',
        p1: '#2dd4bf', p2: '#f59e0b', p3: '#f43f5e',
        grid: '#334155', text: '#94a3b8', label: '#64748b'
    };

    function parseCSV(url) {
        return new Promise((resolve, reject) => {
            Papa.parse(url, { download: true, header: true, skipEmptyLines: true, 
                complete: (r) => resolve(r.data), error: (e) => reject(e) });
        });
    }

    function parseTimestamp(value) {
        const normalized = String(value || "").replace(" ", "T");
        const d = new Date(normalized);
        return isNaN(d.getTime()) ? null : d;
    }

    function formatXAxis(timestamp) {
        const d = parseTimestamp(timestamp);
        if (!d) return "";
        return d.toLocaleString([], { hour: '2-digit', minute: '2-digit', hour12: false });
    }

    function timeSince(timestamp) {
        const d = parseTimestamp(timestamp);
        if (!d) return "";
        const diff = (new Date() - d) / (1000 * 60); // minutes
        if (diff < 60) return Math.round(diff) + "m ago";
        return (diff / 60).toFixed(1) + "h ago";
    }

    function findLastValid(data, key, minVal = 0.001) {
        for (let i = data.length - 1; i >= 0; i--) {
            const val = parseFloat(data[i][key]);
            if (!isNaN(val) && val > minVal) {
                return { value: val, timestamp: data[i].timestamp, isStale: i < data.length - 1 };
            }
        }
        return { value: null, timestamp: null, isStale: false };
    }

    function lastHours(data, hours) {
        if (!data.length) return data;
        const points = data
            .map(row => ({ row, dt: parseTimestamp(row.timestamp) }))
            .filter(item => item.dt)
            .sort((a, b) => a.dt - b.dt);
        if (!points.length) return data;
        const cutoff = points[points.length - 1].dt.getTime() - (hours * 60 * 60 * 1000);
        return points.filter(item => item.dt.getTime() >= cutoff).map(item => item.row);
    }

    async function refresh() {
        try {
            const [met, tel, wea] = await Promise.all([parseCSV(CSV_METRICS), parseCSV(CSV_TELEMETRY), parseCSV(CSV_WEATHER)]);
            if (!met.length || !tel.length) return;

            const lM = met[met.length - 1];
            const lT = tel[tel.length - 1];
            const lW = wea.length ? wea[wea.length - 1] : {};

            // Metric Updates with Resilience Logic
            const metrics = [
                { id: 'temp', key: 'temp', min: 1.0, precision: 1 },
                { id: 'hum', key: 'hum', min: 1.0, precision: 0 },
                { id: 'press', key: 'press', min: 900, precision: 0 },
                { id: 'gas', key: 'gas', min: 0.1, precision: 2 },
                { id: 'light', key: 'light', min: -0.1, precision: 0 },
                { id: 'db', key: 'db', min: -100, precision: 1 }
            ];

            let hardwareWarning = false;

            metrics.forEach(m => {
                const res = findLastValid(tel, m.key, m.min);
                const el = document.getElementById(`val-${m.id}`);
                const staleEl = document.getElementById(`stale-${m.id}`);
                
                if (res.value !== null) {
                    el.textContent = m.precision === 0 ? Math.round(res.value) : res.value.toFixed(m.precision);
                    if (res.isStale) {
                        staleEl.textContent = `⚠️ stale (${timeSince(res.timestamp)})`;
                        staleEl.style.display = 'inline-block';
                        hardwareWarning = true;
                    } else {
                        staleEl.style.display = 'none';
                    }
                }
            });

            // Status Update
            const regStatus = document.getElementById('nav-reg-status');
            if (regStatus && hardwareWarning) {
                regStatus.textContent = "DISTURBED";
                regStatus.style.color = "#facc15";
            } else if (regStatus) {
                regStatus.textContent = "SYNC";
                regStatus.style.color = "#4ade80";
            }
            const syncStatus = document.getElementById('nav-sync-status');
            if(syncStatus) {
                syncStatus.textContent = formatXAxis(lT.timestamp);
                syncStatus.style.color = hardwareWarning ? "#facc15" : "#4ade80";
            }
            
            // DB Display & Meter
            const db = parseFloat(lT.db) || -60;
            document.getElementById('val-db').textContent = db.toFixed(1) + " dB";
            const dbPercent = Math.min(100, Math.max(0, (db + 80) * 1.25)); // Map -80..0 to 0..100
            document.getElementById('db-fill').style.width = dbPercent + "%";

            // State Inference
            const vpd = parseFloat(lM.vpd);
            const stateEl = document.getElementById('val-state');
            if (vpd > 2.0) { stateEl.textContent = "HIGH STRESS"; stateEl.style.color = "#ef4444"; stateEl.style.borderColor = "#ef4444"; }
            else if (vpd < 0.5) { stateEl.textContent = "STAGNANT"; stateEl.style.color = "#38bdf8"; stateEl.style.borderColor = "#38bdf8"; }
            else { stateEl.textContent = "STABLE"; stateEl.style.color = "#4ade80"; stateEl.style.borderColor = "#4ade80"; }

            document.getElementById('live-photo').src = GITHUB_RAW + "media/latest.jpg?t=" + Date.now();

            const m48 = lastHours(met, 48);
            const t48 = lastHours(tel, 48);
            
            drawVitality(m48);
            drawAtmos(t48);
            drawKinetic(t48);

            // Ledger
            try {
                const res = await fetch(GITHUB_RAW + "logs/latest_report.md?t=" + Date.now());
                if (res.ok) {
                    const mdText = await res.text();
                    document.getElementById('warden-log-output').innerHTML = marked.parse(mdText);
                }
            } catch (e) {}
        } catch(e) { console.error(e); }
    }

    const baseOptions = {
        responsive: true, maintainAspectRatio: false,
        elements: { point: { radius: 0 }, line: { tension: 0.35, borderWidth: 2, spanGaps: true } },
        scales: {
            x: { grid: { display: false }, ticks: { color: PALETTE.label, maxTicksLimit: 12, autoSkip: true } },
            y: { grid: { color: PALETTE.grid }, ticks: { color: PALETTE.text } }
        },
        plugins: { legend: { position: 'top', align: 'end', labels: { color: PALETTE.text, usePointStyle: true, boxWidth: 6, padding: 20, font: { size: 11 } } } }
    };

    function drawVitality(data) {
        const ctx = document.getElementById('vitalityChart').getContext('2d');
        if (window.vChart) window.vChart.destroy();
        window.vChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.map(d => formatXAxis(d.timestamp)),
                datasets: [
                    { label: 'Nickels (%)', data: data.map(d => parseFloat(d.p1_pct) || null), borderColor: PALETTE.p1 },
                    { label: 'Mint (%)', data: data.map(d => parseFloat(d.p2_pct) || null), borderColor: PALETTE.p2 },
                    { label: 'Pothos (%)', data: data.map(d => parseFloat(d.p3_pct) || null), borderColor: PALETTE.p3 }
                ]
            },
            options: { ...baseOptions, scales: { ...baseOptions.scales, y: { ...baseOptions.scales.y, min: 0, max: 100, title: { display: true, text: 'MOISTURE (%)', color: PALETTE.label } } } }
        });
    }

    function drawAtmos(data) {
        const ctx = document.getElementById('atmosChart').getContext('2d');
        if (window.aChart) window.aChart.destroy();
        window.aChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.map(d => formatXAxis(d.timestamp)),
                datasets: [
                    { label: 'Temp (°C)', data: data.map(d => parseFloat(d.temp) || null), borderColor: PALETTE.temp, yAxisID: 'y' },
                    { label: 'Humidity (%)', data: data.map(d => parseFloat(d.hum) || null), borderColor: PALETTE.hum, yAxisID: 'y' },
                    { label: 'Light Intensity', data: data.map(d => parseFloat(d.light) || null), borderColor: PALETTE.light, yAxisID: 'yRight', fill: true, backgroundColor: 'rgba(245, 158, 11, 0.05)' }
                ]
            },
            options: { 
                ...baseOptions, 
                scales: { 
                    x: baseOptions.scales.x,
                    y: { ...baseOptions.scales.y, title: { display: true, text: 'T (°C) / H (%)', color: PALETTE.label } },
                    yRight: { position: 'right', grid: { display: false }, ticks: { color: PALETTE.label }, title: { display: true, text: 'LIGHT (RAW)', color: PALETTE.label } }
                } 
            }
        });
    }

    function drawKinetic(data) {
        const ctx = document.getElementById('kineticChart').getContext('2d');
        if (window.kChart) window.kChart.destroy();
        window.kChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.map(d => formatXAxis(d.timestamp)),
                datasets: [
                    { label: 'Acoustics (dB)', data: data.map(d => parseFloat(d.db) || null), borderColor: PALETTE.db, yAxisID: 'y' },
                    { label: 'VOC Resist (kΩ)', data: data.map(d => parseFloat(d.gas) || null), borderColor: PALETTE.voc, yAxisID: 'yRight' }
                ]
            },
            options: { 
                ...baseOptions, 
                scales: { 
                    x: baseOptions.scales.x,
                    y: { ...baseOptions.scales.y, min: -80, max: 0, title: { display: true, text: 'ENERGY (dB)', color: PALETTE.label } },
                    yRight: { position: 'right', grid: { display: false }, ticks: { color: PALETTE.label }, title: { display: true, text: 'CHEM (kΩ)', color: PALETTE.label } }
                } 
            }
        });
    }

    refresh();
    setInterval(refresh, 300000);
</script>
