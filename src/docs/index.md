---
hide:
  - navigation
  - toc
---

# 🌿 GardenOS Terminal

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.3.0/papaparse.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

<style>
/* Global Layout Fixes */
.md-content__inner { max-width: none !important; margin: 0 !important; padding: 1rem 2rem !important; }
.md-main__inner { max-width: none !important; }
.md-sidebar { display: none !important; } /* Kill all sidebars on this page */

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
.sync-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    color: #4ade80;
    font-weight: bold;
}

.dash-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem;
}
.dash-card {
    flex: 1;
    min-width: 320px;
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1);
}
.dash-card h3 {
    margin: 0 0 1.2rem 0 !important;
    font-size: 0.85rem;
    text-transform: uppercase;
    color: #94a3b8;
    letter-spacing: 0.12em;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.val-large { font-size: 2.8em; font-weight: 800; letter-spacing: -0.02em; }
.val-unit { font-size: 1.2em; font-weight: 600; opacity: 0.7; margin-left: 2px; }

/* Navigation Tiles */
.nav-tiles {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
    flex-wrap: wrap;
}
.nav-tile {
    padding: 8px 18px;
    background: #1e293b;
    border-radius: 8px;
    color: #cbd5e1 !important;
    text-decoration: none !important;
    font-size: 0.85rem;
    font-weight: 600;
    transition: all 0.2s;
    border: 1px solid #334155;
}
.nav-tile:hover {
    background: #334155;
    border-color: #4ade80;
    color: #4ade80 !important;
}

.vision-container {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #334155;
    background: #000;
}
#live-photo { width: 100%; display: block; aspect-ratio: 16/9; object-fit: cover; }

.chart-box {
    background: #1e293b;
    padding: 1.5rem;
    border-radius: 16px;
    border: 1px solid #334155;
    height: 420px;
    margin-top: 1.5rem;
}
#warden-log-output {
    background: #0f172a;
    padding: 24px;
    border-radius: 16px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.92rem;
    border: 1px solid #334155;
    color: #cbd5e1;
    line-height: 1.7;
}
</style>

<!-- Top Status Bar -->
<div class="status-header">
    <div style="display: flex; align-items: center; gap: 15px;">
        <span style="font-size: 1.4rem;">🌿</span>
        <span style="font-weight: 700; color: #f8fafc; letter-spacing: 0.05em;">BIOME STATUS: <span style="color: #4ade80;">ACTIVE</span></span>
    </div>
    <div class="sync-badge">
        LAST SYNC: <span id="sync-status">--:--</span>
    </div>
</div>

<div class="nav-tiles">
    <a href="gallery/" class="nav-tile">📖 Daily Gallery</a>
    <a href="blog/origins/" class="nav-tile">🧠 Setup & Origins</a>
    <a href="https://github.com/surendranb/gardenbot" class="nav-tile">GitHub Source</a>
</div>

<div class="dash-grid">
    <!-- Atmosphere -->
    <div class="dash-card">
        <h3>🌡 Atmosphere</h3>
        <div style="display: flex; align-items: baseline; gap: 0.8rem;">
            <div style="color:#f97316;"><span id="val-temp" class="val-large">--</span><span class="val-unit">°C</span></div>
            <div style="color:#64748b; font-size: 2.2rem; font-weight: 100;">|</div>
            <div style="color:#38bdf8;"><span id="val-hum" class="val-large">--</span><span class="val-unit">%</span></div>
        </div>
        <div style="margin-top: 1.2rem; display: flex; justify-content: space-between; align-items: center;">
            <span style="color: #94a3b8; font-size: 0.85rem;">Vapor Pressure Deficit</span>
            <span style="color:#a855f7; font-weight: 800; background: rgba(168, 85, 247, 0.15); padding: 2px 8px; border-radius: 4px;"><span id="val-vpd">--</span> kPa</span>
        </div>
    </div>

    <!-- Soil Moisture -->
    <div class="dash-card">
        <h3>🍃 Biome Vitality</h3>
        <div style="display: flex; flex-direction: column; gap: 0.8rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 8px;">
                <span style="color:#4ade80; font-weight: 600;">p1: Nickels</span>
                <div><strong id="p1-val" style="font-size: 1.2rem;">--</strong> <span id="p1-status" style="font-size: 0.65rem; padding: 2px 6px; border-radius: 4px; margin-left: 5px; font-weight: 800;"></span></div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 8px;">
                <span style="color:#a3e635; font-weight: 600;">p2: Mint</span>
                <div><strong id="p2-val" style="font-size: 1.2rem;">--</strong> <span id="p2-status" style="font-size: 0.65rem; padding: 2px 6px; border-radius: 4px; margin-left: 5px; font-weight: 800;"></span></div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color:#facc15; font-weight: 600;">p3: Pothos</span>
                <div><strong id="p3-val" style="font-size: 1.2rem;">--</strong> <span id="p3-status" style="font-size: 0.65rem; padding: 2px 6px; border-radius: 4px; margin-left: 5px; font-weight: 800;"></span></div>
            </div>
        </div>
        <div style="margin-top: 1rem; font-size: 0.85rem; color: #64748b; display: flex; justify-content: space-between;">
            <span>🔆 Solar Intensity</span>
            <span style="color: #fca5a5; font-weight: 800;"><span id="val-light">--</span> Lux</span>
        </div>
    </div>

    <!-- Vision -->
    <div class="dash-card" style="flex: 1.5; min-width: 400px;">
        <h3>📸 Live Vision Feed</h3>
        <div class="vision-container">
            <img id="live-photo" src="media/latest.jpg" alt="Garden View">
        </div>
    </div>
</div>

<h2 style="margin-top: 3rem !important; border-bottom: 1px solid #334155; padding-bottom: 10px;">72-Hour Environmental Trends</h2>
<div class="chart-box">
    <canvas id="telemetryChart"></canvas>
</div>

<h2 style="margin-top: 4rem !important; border-bottom: 1px solid #334155; padding-bottom: 10px;">The Warden's Ledger</h2>
<div id="warden-log-output">
    Accessing encrypted neural audit...
</div>

<script>
    const CSV_TELEMETRY = "data/telemetry.csv";
    const CSV_METRICS = "data/metrics.csv";
    const MD_LEDGER = "data/ledger.md";

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
            const img = document.getElementById('live-photo');
            if (img) img.src = `media/latest.jpg?t=${Date.now()}`;

            const [tel, met] = await Promise.all([parseCSV(CSV_TELEMETRY), parseCSV(CSV_METRICS)]);
            if (!tel.length) return;

            const lT = tel[tel.length - 1];
            const lM = met[met.length - 1];

            document.getElementById('sync-status').textContent = new Date(lT.timestamp).toLocaleTimeString([], {hour:'2-digit', minute:'2-digit', hour12: false});
            document.getElementById('val-temp').textContent = parseFloat(lT.temp).toFixed(1);
            document.getElementById('val-hum').textContent = Math.round(lT.hum);
            document.getElementById('val-vpd').textContent = parseFloat(lM.vpd).toFixed(2);
            document.getElementById('val-light').textContent = lT.light;

            const upP = (p) => {
                const val = lM[`${p}_pct`];
                const dry = lM[`${p}_is_dry`] === "True";
                document.getElementById(`${p}-val`).textContent = `${parseFloat(val).toFixed(1)}%`;
                const el = document.getElementById(`${p}-status`);
                el.textContent = dry ? "CRITICAL" : "OPTIMAL";
                el.style.backgroundColor = dry ? "#991b1b" : "#064e3b";
                el.style.color = dry ? "#fecaca" : "#a7f3d0";
            };
            ['p1', 'p2', 'p3'].forEach(upP);

            const cData = met.slice(-216).map(m => {
                const t = tel.find(x => x.timestamp === m.timestamp);
                return t ? {...m, temp: t.temp, hum: t.hum, light: t.light} : m;
            });
            draw(cData);

            const res = await fetch(MD_LEDGER);
            if (res.ok) {
                const text = await res.text();
                const parts = text.split(/^## /m);
                if (parts.length > 1) {
                    document.getElementById('warden-log-output').innerHTML = marked.parse("## " + parts[parts.length-1].trim());
                }
            }
        } catch(e) { console.error(e); }
    }

    let chart = null;
    function draw(data) {
        const ctx = document.getElementById('telemetryChart').getContext('2d');
        if (chart) chart.destroy();
        chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.map(d => d.timestamp ? d.timestamp.split(' ')[1].substring(0,5) : ''),
                datasets: [
                    { label: 'p1 (Nickels)', data: data.map(d => d.p1_pct), borderColor: '#4ade80', tension: 0.3, pointRadius: 0 },
                    { label: 'p2 (Mint)', data: data.map(d => d.p2_pct), borderColor: '#a3e635', tension: 0.3, pointRadius: 0 },
                    { label: 'p3 (Pothos)', data: data.map(d => d.p3_pct), borderColor: '#facc15', tension: 0.3, pointRadius: 0 },
                    { label: 'Temp', data: data.map(d => d.temp), borderColor: 'rgba(249,115,22,0.3)', tension: 0.3, pointRadius: 0, borderWidth: 1 },
                    { label: 'Solar', data: data.map(d => d.light), borderColor: 'rgba(250,204,21,0.3)', tension: 0.3, pointRadius: 0, borderWidth: 1, yAxisID: 'yL' }
                ]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                scales: { 
                    y: { min: 0, max: 100, grid: { color: '#334155' }, ticks: { color: '#94a3b8' } },
                    yL: { position: 'right', min: 0, grid: { display: false }, ticks: { color: '#94a3b8' } },
                    x: { ticks: { maxTicksLimit: 12, color: '#64748b' }, grid: { display: false } }
                },
                plugins: { legend: { labels: { color: '#94a3b8', usePointStyle: true, boxWidth: 6 } } }
            }
        });
    }

    refresh();
    setInterval(refresh, 60000);
</script>
