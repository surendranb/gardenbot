---
hide:
  - navigation
  - toc
---

# 🌿 GardenOS Terminal

<style>
/* Full Width Overrides */
.md-content__inner { max-width: none !important; margin: 0 !important; padding: 1rem 2rem !important; }
.md-main__inner { max-width: none !important; }
.md-sidebar { display: none !important; }

.status-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #0f172a;
    padding: 10px 20px;
    border-radius: 12px;
    border: 1px solid #334155;
    margin-bottom: 1.5rem;
}
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
}
.val-large { font-size: 2.2em; font-weight: 800; letter-spacing: -0.02em; }
.label-sub { font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem; display: block; }
.vision-container {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #334155;
    background: #000;
}
.chart-container {
    background: #1e293b;
    padding: 1.2rem;
    border-radius: 16px;
    border: 1px solid #334155;
    height: 400px;
    margin-top: 1rem;
}
.chart-note {
    color: #94a3b8;
    font-size: 0.78rem;
    margin-top: 0.35rem;
}
</style>

<div class="status-header">
    <div style="display: flex; align-items: center; gap: 15px;">
        <span style="font-size: 1.4rem;">🌿</span>
        <span style="font-weight: 700; color: #f8fafc; letter-spacing: 0.05em;">BIOME STATUS: <span style="color: #4ade80;">ACTIVE</span></span>
    </div>
    <div style="font-family: monospace; font-size: 0.85rem; color: #4ade80; font-weight: bold;">
        LAST SYNC: <span id="sync-status">--:--</span>
    </div>
</div>

<div class="dash-grid">
    <!-- Atmosphere -->
    <div class="dash-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <span class="label-sub">🌡 ATMOSPHERE</span>
            <span id="val-state" style="font-size: 0.65rem; color: #4ade80; border: 1px solid #4ade80; padding: 1px 6px; border-radius: 4px; font-weight: bold;">STABLE</span>
        </div>
        <div style="display: flex; align-items: baseline; gap: 1.2rem; margin-top: 0.5rem;">
            <div style="color:#f97316;"><span id="val-temp" class="val-large">--</span><span style="font-size: 1rem; opacity: 0.7;">°C</span></div>
            <div style="color:#38bdf8;"><span id="val-hum" class="val-large">--</span><span style="font-size: 1rem; opacity: 0.7;">%</span></div>
            <div style="color:#a855f7; margin-left: auto;"><span id="val-vpd" class="val-large">--</span><span style="font-size: 1rem; opacity: 0.7;"> kPa</span></div>
        </div>
        
        <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #334155; display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; font-size: 0.8rem;">
            <div>
                <span style="color: #94a3b8; font-size: 0.7rem; display: block;">LUMINOUS INTENSITY</span>
                <span id="val-light" style="color:#facc15; font-weight: 600;">--</span>
            </div>
            <div>
                <span style="color: #94a3b8; font-size: 0.7rem; display: block;">SHIELDING (ΔT/ΔH)</span>
                <span id="val-shield" style="color:#4ade80; font-weight: 600;">--</span>
            </div>
            <div>
                <span style="color: #94a3b8; font-size: 0.7rem; display: block;">BARO PRESSURE</span>
                <span id="val-press" style="color:#94a3b8;">-- hPa</span>
            </div>
            <div>
                <span style="color: #94a3b8; font-size: 0.7rem; display: block;">RAIN PROBABILITY</span>
                <span id="val-pop" style="color:#38bdf8;">--%</span>
            </div>
        </div>

        <div style="margin-top: 1rem; padding-top: 0.5rem; border-top: 1px dashed #334155; display: flex; justify-content: space-between; font-size: 0.8rem;">
            <span style="color: #94a3b8;">Outdoor Forecast</span>
            <span id="val-forecast" style="color:#38bdf8; font-weight: 600;">--</span>
        </div>
    </div>

    <!-- Vision -->
    <div class="dash-card">
        <span class="label-sub">📸 LIVE VISION FEED</span>
        <div class="vision-container">
            <img id="live-photo" src="https://raw.githubusercontent.com/surendranb/gardenbot/main/media/latest.jpg" style="width: 100%; aspect-ratio: 16/9; object-fit: cover;">
        </div>
    </div>
</div>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-top: 1.5rem;">
    <!-- Chart 1: Vitality -->
    <div>
        <span class="label-sub">📈 PLANT VITALITY (LAST 48H)</span>
        <div class="chart-container">
            <canvas id="vitalityChart"></canvas>
        </div>
        <div class="chart-note">Full date/time labels shown for every point in the 48-hour window.</div>
    </div>
    <!-- Chart 2: Environment -->
    <div>
        <span class="label-sub">📊 ENVIRONMENTAL CHRONICLE (LAST 48H)</span>
        <div class="chart-container">
            <canvas id="envChart"></canvas>
        </div>
        <div class="chart-note">Full date/time labels shown for every point in the 48-hour window.</div>
    </div>
</div>

<h2 style="margin-top: 3rem !important; border-bottom: 1px solid #334155; padding-bottom: 10px;">The Warden's Ledger</h2>
<div id="warden-log-output" style="background: #0f172a; padding: 20px; border-radius: 12px; font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; line-height: 1.6; border: 1px solid #334155; color: #cbd5e1;">
    Accessing neural audit...
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.3.0/papaparse.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

<script>
    const GITHUB_RAW = "https://raw.githubusercontent.com/surendranb/gardenbot/main/";
    const CSV_METRICS = GITHUB_RAW + "data/metrics.csv";
    const CSV_TELEMETRY = GITHUB_RAW + "data/telemetry.csv";
    const CSV_WEATHER = GITHUB_RAW + "data/weather.csv";

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
        if (!d) return String(timestamp || "--");
        return d.toLocaleString([], {
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            hour12: false
        });
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
            const lW = wea.length ? wea[wea.length - 1] : { description: "N/A", pressure: "--", pop: 0, temp: lT.temp, humidity: lT.hum };

            // UI Updates
            document.getElementById('sync-status').textContent = lM.timestamp || "--:--";
            document.getElementById('val-temp').textContent = lT.temp ? parseFloat(lT.temp).toFixed(1) : "--";
            document.getElementById('val-hum').textContent = lT.hum ? Math.round(lT.hum) : "--";
            document.getElementById('val-vpd').textContent = lM.vpd ? parseFloat(lM.vpd).toFixed(2) : "--";
            document.getElementById('val-forecast').textContent = (lW.description || "N/A").toUpperCase();
            document.getElementById('live-photo').src = GITHUB_RAW + "media/latest.jpg?t=" + Date.now();

            // New Factual Metrics
            document.getElementById('val-light').textContent = lT.light || "--";
            document.getElementById('val-press').textContent = (lW.pressure || "--") + " hPa";
            
            // Handle pop as either 0-1 or 0-100
            let popVal = parseFloat(lW.pop) || 0;
            if (popVal > 0 && popVal <= 1) popVal = popVal * 100;
            document.getElementById('val-pop').textContent = Math.round(popVal) + "%";
            
            // Shielding Delta (Outdoor - Indoor)
            if (lW.temp && lT.temp) {
                const dT = (parseFloat(lW.temp) - parseFloat(lT.temp)).toFixed(1);
                const dH = (parseFloat(lW.humidity || lW.hum) - parseFloat(lT.hum)).toFixed(0);
                document.getElementById('val-shield').textContent = `${dT > 0 ? '+' : ''}${dT}° / ${dH > 0 ? '+' : ''}${dH}%`;
            } else {
                document.getElementById('val-shield').textContent = "-- / --";
            }

            // Simple State Inference (One factual-based indicator)
            const vpd = parseFloat(lM.vpd);
            const stateEl = document.getElementById('val-state');
            if (vpd > 2.0) { stateEl.textContent = "HIGH STRESS"; stateEl.style.color = "#ef4444"; stateEl.style.borderColor = "#ef4444"; }
            else if (vpd < 0.5) { stateEl.textContent = "STAGNANT"; stateEl.style.color = "#38bdf8"; stateEl.style.borderColor = "#38bdf8"; }
            else { stateEl.textContent = "STABLE"; stateEl.style.color = "#4ade80"; stateEl.style.borderColor = "#4ade80"; }

            const met48 = lastHours(met, 48);
            const tel48 = lastHours(tel, 48);
            drawVitality(met48);
            drawEnv(tel48, met48);

            // Ledger
            const res = await fetch(GITHUB_RAW + "logs/vision_ledger.md?t=" + Date.now());
            if (res.ok) {
                const text = await res.text();
                // Split by H1 headers (the WARDEN REPT lines)
                const blocks = text.split(/^# /m).filter(b => b.trim().startsWith('WARDEN REPT'));
                if (blocks.length) {
                    let latest = "# " + blocks[blocks.length - 1].trim();
                    // Hide internal state section from public dashboard
                    latest = latest.split('## 💾 STATE UPDATE')[0].trim();
                    document.getElementById('warden-log-output').innerHTML = marked.parse(latest);
                } else {
                    document.getElementById('warden-log-output').innerHTML = "No recent reports found.";
                }
            }
        } catch(e) { console.error(e); }
    }

    const commonScaleOptions = {
        y: { grid: { color: '#334155' }, ticks: { color: '#94a3b8' } },
        x: { ticks: { 
            maxTicksLimit: 12, 
            color: '#64748b',
            autoSkip: true,
            maxRotation: 0
        }, grid: { display: false } }
    };

    function drawVitality(data) {
        const ctx = document.getElementById('vitalityChart').getContext('2d');
        if (window.vChart) window.vChart.destroy();
        window.vChart = new Chart(ctx, {
            type: 'line',
            data: {
            labels: data.map(d => formatXAxis(d.timestamp)),
            datasets: [
                { label: 'p1 (Nickels)', data: data.map(d => d.p1_pct), borderColor: '#4ade80', pointRadius: 0, tension: 0.3 },
                { label: 'p2 (Mint)', data: data.map(d => d.p2_pct), borderColor: '#a3e635', pointRadius: 0, tension: 0.3 },
                { label: 'p3 (Pothos)', data: data.map(d => d.p3_pct), borderColor: '#facc15', pointRadius: 0, tension: 0.3 }
            ]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                scales: commonScaleOptions,
                plugins: { legend: { labels: { color: '#94a3b8', usePointStyle: true, boxWidth: 6 } } }
            }
        });
    }

    function drawEnv(tel, met) {
        const ctx = document.getElementById('envChart').getContext('2d');
        if (window.eChart) window.eChart.destroy();
        window.eChart = new Chart(ctx, {
            type: 'line',
            data: {
            labels: tel.map(t => formatXAxis(t.timestamp)),
            datasets: [
                { label: 'Temp °C', data: tel.map(t => t.temp), borderColor: '#f97316', pointRadius: 0, yAxisID: 'y', tension: 0.3 },
                { label: 'Hum %', data: tel.map(t => t.hum), borderColor: '#38bdf8', pointRadius: 0, yAxisID: 'y', tension: 0.3 },
                    { label: 'Solar', data: tel.map(t => t.light), borderColor: '#facc15', pointRadius: 0, fill: true, backgroundColor: 'rgba(250, 204, 21, 0.05)', yAxisID: 'ySolar', tension: 0.3 }
                ]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                scales: {
                    y: { ...commonScaleOptions.y, min: 0, max: 100 },
                    ySolar: { position: 'right', min: 0, max: 1024, grid: { display: false }, ticks: { display: false } },
                    x: commonScaleOptions.x
                },
                plugins: { legend: { labels: { color: '#94a3b8', usePointStyle: true, boxWidth: 6 } } }
            }
        });
    }

    refresh();
    setInterval(refresh, 300000);
</script>
