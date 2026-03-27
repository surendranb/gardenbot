# 🌿 GardenOS Terminal

<style>
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
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 1.5rem;
}
.dash-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 1.5rem;
}
.val-large { font-size: 2.5em; font-weight: 800; }
.status-badge {
    font-size: 0.65rem;
    padding: 2px 8px;
    border-radius: 4px;
    font-weight: 800;
    text-transform: uppercase;
}
.vision-container {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #334155;
    background: #000;
}
</style>

<div class="status-header">
    <div style="display: flex; align-items: center; gap: 15px;">
        <span style="font-size: 1.4rem;">🌿</span>
        <span style="font-weight: 700; color: #f8fafc;">BIOME STATUS: <span style="color: #4ade80;">ACTIVE</span></span>
    </div>
    <div style="font-family: monospace; font-size: 0.85rem; color: #4ade80; font-weight: bold;">
        LAST SYNC: <span id="sync-status">--:--</span>
    </div>
</div>

<div class="dash-grid">
    <!-- Atmosphere -->
    <div class="dash-card">
        <h3 style="margin:0 0 1rem 0; color: #94a3b8; font-size: 0.8rem; letter-spacing: 0.1em;">🌡 ATMOSPHERE</h3>
        <div style="display: flex; align-items: baseline; gap: 1rem;">
            <div style="color:#f97316;"><span id="val-temp" class="val-large">--</span><span style="font-size: 1.2em;">°C</span></div>
            <div style="color:#38bdf8;"><span id="val-hum" class="val-large">--</span><span style="font-size: 1.2em;">%</span></div>
        </div>
        <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #334155; display: flex; justify-content: space-between;">
            <span style="color: #94a3b8;">VPD Strength</span>
            <span id="val-vpd" style="color:#a855f7; font-weight: 800;">-- kPa</span>
        </div>
    </div>

    <!-- Vitality -->
    <div class="dash-card">
        <h3 style="margin:0 0 1rem 0; color: #94a3b8; font-size: 0.8rem; letter-spacing: 0.1em;">🍃 VITALITY PULSE</h3>
        <div style="display: flex; flex-direction: column; gap: 0.8rem;">
            <div style="display: flex; justify-content: space-between;">
                <span>p1: Nickels</span>
                <div><span id="p1-val">--</span> <span id="p1-status" class="status-badge"></span></div>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span>p2: Mint</span>
                <div><span id="p2-val">--</span> <span id="p2-status" class="status-badge"></span></div>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span>p3: Pothos</span>
                <div><span id="p3-val">--</span> <span id="p3-status" class="status-badge"></span></div>
            </div>
        </div>
    </div>

    <!-- Vision -->
    <div class="dash-card" style="grid-column: span 1;">
        <h3 style="margin:0 0 1rem 0; color: #94a3b8; font-size: 0.8rem; letter-spacing: 0.1em;">📸 LIVE FEED</h3>
        <div class="vision-container">
            <img id="live-photo" src="https://raw.githubusercontent.com/surendranb/gardenbot/main/media/latest.jpg" style="width: 100%; aspect-ratio: 16/9; object-fit: cover;">
        </div>
    </div>
</div>

<h2 style="margin-top: 3rem !important;">72-Hour Environmental Trends</h2>
<div style="background: #1e293b; padding: 1.5rem; border-radius: 16px; border: 1px solid #334155; height: 450px;">
    <canvas id="telemetryChart"></canvas>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.3.0/papaparse.min.js"></script>

<script>
    const GITHUB_RAW = "https://raw.githubusercontent.com/surendranb/gardenbot/main/";
    const CSV_METRICS = GITHUB_RAW + "data/metrics.csv";
    const CSV_TELEMETRY = GITHUB_RAW + "data/telemetry.csv";

    function parseCSV(url) {
        return new Promise((resolve, reject) => {
            Papa.parse(url, { download: true, header: true, skipEmptyLines: true, 
                complete: (r) => resolve(r.data), error: (e) => reject(e) });
        });
    }

    async function refresh() {
        try {
            const [met, tel] = await Promise.all([parseCSV(CSV_METRICS), parseCSV(CSV_TELEMETRY)]);
            const lM = met[met.length - 1];
            const lT = tel[tel.length - 1];

            document.getElementById('sync-status').textContent = lM.timestamp.split(' ')[1].substring(0,5);
            document.getElementById('val-temp').textContent = parseFloat(lT.temp).toFixed(1);
            document.getElementById('val-hum').textContent = Math.round(lT.hum);
            document.getElementById('val-vpd').textContent = parseFloat(lM.vpd).toFixed(2);
            document.getElementById('live-photo').src = GITHUB_RAW + "media/latest.jpg?t=" + Date.now();

            const updateBadge = (id) => {
                const val = parseFloat(lM[id + '_pct']).toFixed(1);
                const dry = lM[id + '_is_dry'] === "True";
                document.getElementById(id + '-val').textContent = val + "%";
                const b = document.getElementById(id + '-status');
                b.textContent = dry ? "Dry" : "OK";
                b.style.background = dry ? "#991b1b" : "#064e3b";
                b.style.color = dry ? "#fecaca" : "#a7f3d0";
            };
            ['p1', 'p2', 'p3'].forEach(updateBadge);

            drawChart(met.slice(-144), tel.slice(-144));
        } catch(e) { console.error(e); }
    }

    let chart = null;
    function drawChart(met, tel) {
        const ctx = document.getElementById('telemetryChart').getContext('2d');
        if (chart) chart.destroy();
        
        // Align telemetry to metrics by timestamp
        const alignedTel = met.map(m => tel.find(t => t.timestamp === m.timestamp) || {});

        chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: met.map(m => m.timestamp.split(' ')[1].substring(0,5)),
                datasets: [
                    { label: 'p1 (Nickels)', data: met.map(m => m.p1_pct), borderColor: '#4ade80', pointRadius: 0, tension: 0.3 },
                    { label: 'p2 (Mint)', data: met.map(m => m.p2_pct), borderColor: '#a3e635', pointRadius: 0, tension: 0.3 },
                    { label: 'p3 (Pothos)', data: met.map(m => m.p3_pct), borderColor: '#facc15', pointRadius: 0, tension: 0.3 },
                    { label: 'Temp °C', data: alignedTel.map(t => t.temp), borderColor: '#f97316', pointRadius: 0, borderWidth: 1, borderDash: [5,5], yAxisID: 'y1' }
                ]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                scales: { 
                    y: { min: 0, max: 100, grid: { color: '#334155' }, ticks: { color: '#94a3b8' } },
                    y1: { position: 'right', min: 20, max: 45, grid: { display: false }, ticks: { color: '#f97316' } },
                    x: { ticks: { maxTicksLimit: 12, color: '#64748b' }, grid: { display: false } }
                },
                plugins: { legend: { labels: { color: '#94a3b8', usePointStyle: true, boxWidth: 6 } } }
            }
        });
    }
    refresh();
    setInterval(refresh, 300000);
</script>
