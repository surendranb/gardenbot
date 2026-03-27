# 🌿 GardenOS Terminal

<div class="status-header" style="display: flex; justify-content: space-between; align-items: center; background: #0f172a; padding: 10px 20px; border-radius: 12px; border: 1px solid #334155; margin-bottom: 1.5rem;">
    <div style="display: flex; align-items: center; gap: 15px;">
        <span style="font-size: 1.4rem;">🌿</span>
        <span style="font-weight: 700; color: #f8fafc; letter-spacing: 0.05em;">BIOME STATUS: <span id="sync-status-text" style="color: #4ade80;">ACTIVE</span></span>
    </div>
    <div style="font-family: monospace; font-size: 0.85rem; color: #4ade80; font-weight: bold;">
        LAST SYNC: <span id="sync-status">--:--</span>
    </div>
</div>

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem;">
    <!-- Atmosphere -->
    <div style="background: #1e293b; border: 1px solid #334155; border-radius: 16px; padding: 1.5rem;">
        <h3 style="margin: 0 0 1.2rem 0; font-size: 0.85rem; text-transform: uppercase; color: #94a3b8; letter-spacing: 0.12em;">🌡 Atmosphere</h3>
        <div style="display: flex; align-items: baseline; gap: 0.8rem;">
            <div style="color:#f97316;"><span id="val-temp" style="font-size: 2.8em; font-weight: 800;">--</span><span style="font-size: 1.2em; opacity: 0.7;">°C</span></div>
            <div style="color:#64748b; font-size: 2.2rem; font-weight: 100;">|</div>
            <div style="color:#38bdf8;"><span id="val-hum" style="font-size: 2.8em; font-weight: 800;">--</span><span style="font-size: 1.2em; opacity: 0.7;">%</span></div>
        </div>
        <div style="margin-top: 1.2rem; display: flex; justify-content: space-between; align-items: center;">
            <span style="color: #94a3b8; font-size: 0.85rem;">Vapor Pressure Deficit</span>
            <span style="color:#a855f7; font-weight: 800; background: rgba(168, 85, 247, 0.15); padding: 2px 8px; border-radius: 4px;"><span id="val-vpd">--</span> kPa</span>
        </div>
    </div>

    <!-- Vision -->
    <div style="background: #1e293b; border: 1px solid #334155; border-radius: 16px; padding: 1.5rem;">
        <h3 style="margin: 0 0 1.2rem 0; font-size: 0.85rem; text-transform: uppercase; color: #94a3b8; letter-spacing: 0.12em;">📸 Live Vision</h3>
        <div style="border-radius: 12px; overflow: hidden; border: 1px solid #334155; background: #000;">
            <img id="live-photo" src="https://raw.githubusercontent.com/surendranb/gardenbot/main/media/latest.jpg" alt="Garden View" style="width: 100%; display: block; aspect-ratio: 16/9; object-fit: cover;">
        </div>
    </div>
</div>

<h2 style="margin-top: 3rem !important; border-bottom: 1px solid #334155; padding-bottom: 10px;">72-Hour Environmental Trends</h2>
<div style="background: #1e293b; padding: 1.5rem; border-radius: 16px; border: 1px solid #334155; height: 420px; margin-top: 1.5rem;">
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
            Papa.parse(url, {
                download: true,
                header: true,
                skipEmptyLines: true,
                complete: (results) => resolve(results.data),
                error: (err) => reject(err)
            });
        });
    }

    async function refresh() {
        try {
            const [met, tel] = await Promise.all([parseCSV(CSV_METRICS), parseCSV(CSV_TELEMETRY)]);
            if (!met.length || !tel.length) return;

            const lM = met[met.length - 1];
            const lT = tel[tel.length - 1];

            document.getElementById('sync-status').textContent = lM.timestamp.split(' ')[1].substring(0,5);
            document.getElementById('val-temp').textContent = parseFloat(lT.temp).toFixed(1);
            document.getElementById('val-hum').textContent = Math.round(lT.hum);
            document.getElementById('val-vpd').textContent = parseFloat(lM.vpd).toFixed(2);
            
            // Photo refresh (cache busting)
            document.getElementById('live-photo').src = GITHUB_RAW + "media/latest.jpg?t=" + Date.now();

            drawChart(met.slice(-144), tel.slice(-144)); // Last 72 hours (approx 2 reads/hour)
        } catch(e) { console.error("Refresh failed", e); }
    }

    let chart = null;
    function drawChart(met, tel) {
        const ctx = document.getElementById('telemetryChart').getContext('2d');
        if (chart) chart.destroy();
        chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: met.map(m => m.timestamp.split(' ')[1].substring(0,5)),
                datasets: [
                    { label: 'p1 %', data: met.map(m => m.p1_pct), borderColor: '#4ade80', tension: 0.3, pointRadius: 0 },
                    { label: 'p2 %', data: met.map(m => m.p2_pct), borderColor: '#a3e635', tension: 0.3, pointRadius: 0 },
                    { label: 'p3 %', data: met.map(m => m.p3_pct), borderColor: '#facc15', tension: 0.3, pointRadius: 0 }
                ]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                scales: { 
                    y: { min: 0, max: 100, grid: { color: '#334155' }, ticks: { color: '#94a3b8' } },
                    x: { ticks: { maxTicksLimit: 12, color: '#64748b' }, grid: { display: false } }
                }
            }
        });
    }

    refresh();
    setInterval(refresh, 300000); // Sync with GitHub raw cache (5 mins)
</script>