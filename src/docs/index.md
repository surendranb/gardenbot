---
hide:
  - toc
---

# 🌿 GardenOS Live Telemetry

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.3.0/papaparse.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

<style>
/* SLEDGEHAMMER: Force content area to be full width on the dashboard */
.md-content__inner {
    max-width: none !important;
    padding-top: 0 !important;
}
.md-main__inner {
    max-width: none !important;
}

/* Robust Dashboard Styling */
.dashboard-container {
    display: flex;
    flex-direction: column;
    gap: 2rem;
    width: 100%;
}
.stat-section {
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem;
    width: 100%;
}
.stat-card {
    flex: 1;
    min-width: 300px;
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
}
.stat-card h3 {
    margin: 0 0 1rem 0 !important;
    font-size: 0.9rem;
    text-transform: uppercase;
    color: #94a3b8;
    letter-spacing: 0.05em;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.val-display {
    display: flex;
    align-items: baseline;
    gap: 0.5rem;
}
.vision-img-outer {
    border-radius: 8px;
    overflow: hidden;
    margin-top: 10px;
    border: 1px solid #334155;
    background: #0f172a;
}
#live-photo {
    width: 100%;
    display: block;
    aspect-ratio: 4/3;
    object-fit: cover;
}
.chart-container {
    position: relative;
    height: 400px;
    width: 100%;
    background: #1e293b;
    padding: 1.5rem;
    border-radius: 12px;
    border: 1px solid #334155;
}
#warden-log-card {
    background-color: #0f172a;
    padding: 24px;
    border-radius: 12px;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    font-size: 0.95em;
    line-height: 1.6;
    color: #cbd5e1;
    border: 1px solid #334155;
}
/* Responsive overrides for text wrapping */
@media (max-width: 600px) {
    .stat-card { min-width: 100%; }
}
</style>

<div class="dashboard-container">
    
    <!-- Top Row: Atmosphere and Vision -->
    <div class="stat-section">
        <!-- Atmosphere -->
        <div class="stat-card">
            <h3>:material-thermometer: Atmosphere</h3>
            <div class="val-display">
                <span id="val-temp" style="color:#f97316; font-size:2.5em; font-weight:bold;">--</span><span style="color:#f97316; font-weight:bold; font-size:1.2em;">°C</span>
                <span style="color:#64748b; font-size:2em; font-weight:bold; margin: 0 10px;">|</span>
                <span id="val-hum" style="color:#38bdf8; font-size:2.5em; font-weight:bold;">--</span><span style="color:#38bdf8; font-weight:bold; font-size:1.2em;">%</span>
            </div>
            <div style="font-size: 0.9rem; color: #94a3b8; margin-top: 1rem;">
                Vapor Pressure Deficit: <span id="val-vpd" style="color:#a855f7; font-weight:bold;">--</span> kPa
            </div>
        </div>

        <!-- Water Levels -->
        <div class="stat-card">
            <h3>:material-leaf: Plant Vitality (Wetness)</h3>
            <div style="display: flex; flex-direction: column; gap: 0.8rem; margin-top: 5px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color:#4ade80; font-weight: 500;">p1 (Nickels)</span>
                    <div><strong id="p1-val" style="font-size: 1.1em;">--</strong> <span id="p1-status" style="font-size:0.75em; margin-left:8px; border-radius:4px;"></span></div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color:#a3e635; font-weight: 500;">p2 (Mint)</span>
                    <div><strong id="p2-val" style="font-size: 1.1em;">--</strong> <span id="p2-status" style="font-size:0.75em; margin-left:8px; border-radius:4px;"></span></div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color:#facc15; font-weight: 500;">p3 (Pothos)</span>
                    <div><strong id="p3-val" style="font-size: 1.1em;">--</strong> <span id="p3-status" style="font-size:0.75em; margin-left:8px; border-radius:4px;"></span></div>
                </div>
            </div>
            <div style="font-size: 0.85rem; color: #fef08a; margin-top: 1rem; border-top: 1px solid #334155; padding-top: 10px;">
                🔆 Light: <span id="val-light" style="font-weight:bold;">--</span> Lux
            </div>
        </div>

        <!-- Vision -->
        <div class="stat-card" style="flex: 1.5; min-width: 350px;">
            <h3>:material-camera: Live Vision Audit</h3>
            <div class="vision-img-outer">
                <img id="live-photo" src="media/latest.jpg" alt="Garden View">
            </div>
        </div>
    </div>

    <!-- Middle: Trends -->
    <div style="width: 100%;">
        <h2 style="margin-top: 0 !important;">72-Hour Telemetry Trends</h2>
        <div class="chart-container">
            <canvas id="telemetryChart"></canvas>
        </div>
    </div>

    <!-- Bottom: Observer Log -->
    <div style="width: 100%;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <h2 style="margin: 0 !important;">The Warden's Ledger</h2>
            <span id="last-updated" style="font-size: 0.85em; color:#4ade80; font-family: 'JetBrains Mono', monospace; font-weight: bold; background: #14532d; padding: 4px 12px; border-radius: 20px;">Syncing...</span>
        </div>
        <div id="warden-log-card">
            Analyzing telemetry data...
        </div>
    </div>

</div>

<script>
    function parseCSV(url) {
        return new Promise((resolve, reject) => {
            Papa.parse(url, {
                download: true,
                header: true,
                skipEmptyLines: true,
                complete: (results) => resolve(results.data),
                error: (err) => reject(err)
            });
        });
    }

    async function updateDashboard() {
        try {
            const img = document.getElementById('live-photo');
            if (img) img.src = `media/latest.jpg?t=${Date.now()}`;

            const [telemetry, metrics] = await Promise.all([
                parseCSV("data/telemetry.csv"),
                parseCSV("data/metrics.csv")
            ]);

            if (!telemetry.length || !metrics.length) throw new Error("Missing data in CSVs");

            const lastTel = telemetry[telemetry.length - 1];
            const lastMet = metrics[metrics.length - 1];

            document.getElementById('last-updated').textContent = `SYNC: ${new Date(lastTel.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}`;
            document.getElementById('val-temp').textContent = parseFloat(lastTel.temp).toFixed(1) || '--';
            document.getElementById('val-hum').textContent = Math.round(lastTel.hum) || '--';
            document.getElementById('val-vpd').textContent = parseFloat(lastMet.vpd).toFixed(2) || '--';
            document.getElementById('val-light').textContent = lastTel.light || '--';

            const updatePlant = (id) => {
                const pct = lastMet[`${id}_pct`];
                const isDry = lastMet[`${id}_is_dry`] === "True";
                
                if (pct !== undefined) {
                    document.getElementById(`${id}-val`).textContent = `${parseFloat(pct).toFixed(1)}%`;
                    const stat = document.getElementById(`${id}-status`);
                    stat.textContent = isDry ? "DRY" : "NOMINAL";
                    stat.style.color = isDry ? '#fca5a5' : '#4ade80';
                    stat.style.backgroundColor = isDry ? '#7f1d1d' : '#14532d';
                    stat.style.padding = '2px 8px';
                }
            };
            ['p1', 'p2', 'p3'].forEach(updatePlant);

            const chartData = metrics.slice(-216).map(m => {
                const t = telemetry.find(tel => tel.timestamp === m.timestamp);
                return t ? { ...m, temp: t.temp, hum: t.hum, light: t.light } : m;
            });
            drawChart(chartData);

            const ledgerRes = await fetch('data/ledger.md');
            if (ledgerRes.ok) {
                const text = await ledgerRes.text();
                const entries = text.split(/^## /m);
                const lastEntry = entries[entries.length - 1];
                if (lastEntry) {
                    document.getElementById('warden-log-card').innerHTML = marked.parse("## " + lastEntry.trim());
                }
            }

        } catch (e) { 
            console.error("Dashboard error:", e);
            document.getElementById('last-updated').textContent = "DATA OFFLINE";
            document.getElementById('last-updated').style.backgroundColor = '#7f1d1d';
        }
    }

    let chart = null;
    function drawChart(data) {
        const ctx = document.getElementById('telemetryChart').getContext('2d');
        if (chart) chart.destroy();
        chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.map(d => d.timestamp ? d.timestamp.split(' ')[1].substring(0,5) : ''),
                datasets: [
                    { label: 'Nickels', data: data.map(d => d.p1_pct), borderColor: '#4ade80', backgroundColor: 'rgba(74, 222, 128, 0.1)', tension: 0.3, pointRadius: 0, borderWidth: 2, z: 10 },
                    { label: 'Mint', data: data.map(d => d.p2_pct), borderColor: '#a3e635', backgroundColor: 'rgba(163, 230, 53, 0.1)', tension: 0.3, pointRadius: 0, borderWidth: 2, z: 10 },
                    { label: 'Pothos', data: data.map(d => d.p3_pct), borderColor: '#facc15', backgroundColor: 'rgba(250, 204, 21, 0.1)', tension: 0.3, pointRadius: 0, borderWidth: 2, z: 10 },
                    { label: 'Temp', data: data.map(d => d.temp), borderColor: 'rgba(249, 115, 22, 0.4)', tension: 0.3, pointRadius: 0, borderWidth: 1, fill: false },
                    { label: 'Hum', data: data.map(d => d.hum), borderColor: 'rgba(56, 189, 248, 0.4)', tension: 0.3, pointRadius: 0, borderWidth: 1, fill: false },
                    { label: 'Light', data: data.map(d => d.light), borderColor: 'rgba(250, 204, 21, 0.5)', tension: 0.3, pointRadius: 0, borderWidth: 1, yAxisID: 'yLux', fill: false }
                ]
            },
            options: { 
                responsive: true, maintainAspectRatio: false,
                interaction: { mode: 'index', intersect: false },
                scales: { 
                    y: { 
                        min: 0, max: 100,
                        grid: { color: '#334155' },
                        title: { display: true, text: 'Moisture / Humidity %', color: '#94a3b8' },
                        ticks: { color: '#94a3b8' }
                    },
                    yLux: {
                        position: 'right',
                        min: 0,
                        grid: { display: false },
                        title: { display: true, text: 'Light (Lux)', color: '#94a3b8' },
                        ticks: { color: '#facc15' }
                    },
                    x: { grid: { display: false }, ticks: { maxTicksLimit: 12, color: '#64748b' } } 
                },
                plugins: { 
                    legend: { position: 'top', labels: { color: '#94a3b8', usePointStyle: true, padding: 20 } },
                    tooltip: { backgroundColor: '#1e293b', titleColor: '#4ade80', bodyColor: '#e2e8f0', borderColor: '#334155', borderWidth: 1 }
                }
            }
        });
    }

    // Initial load
    updateDashboard();
    // Refresh every 5 minutes
    setInterval(updateDashboard, 300000);
</script>
