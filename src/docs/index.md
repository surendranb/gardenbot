# 🌿 GardenOS Live Telemetry

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.3.0/papaparse.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

<div class="grid cards" markdown="1">

-   :material-thermometer: __Atmosphere__
    <br><span id="val-temp" style="color:#f97316; font-size:1.8em; font-weight:bold;">--</span>°C
    <span style="color:#64748b; font-size:1.8em; font-weight:bold; margin: 0 5px;">|</span>
    <span id="val-hum" style="color:#38bdf8; font-size:1.8em; font-weight:bold;">--</span>%
    <div style="font-size: 0.85em; color: #94a3b8; margin-top: 5px;">VPD: <span id="val-vpd" style="color:#a855f7; font-weight:bold;">--</span> kPa</div>

-   :material-leaf: __Water Levels (Wetness %)__
    <div style="margin-top: 10px; line-height: 1.6;">
    <span style="color:#4ade80;">p1 (Nickels):</span> <strong id="p1-val">--</strong> - <span id="p1-status">...</span><br>
    <span style="color:#a3e635;">p2 (Mint):</span> <strong id="p2-val">--</strong> - <span id="p2-status">...</span><br>
    <span style="color:#facc15;">p3 (Pothos):</span> <strong id="p3-val">--</strong> - <span id="p3-status">...</span>
    </div>
    <div style="font-size: 0.85em; color: #fef08a; margin-top: 5px;">Light Exposure: <span id="val-light" style="font-weight:bold;">--</span> Lux</div>

-   :material-camera: __Live Vision__
    <div style="border-radius: 8px; overflow: hidden; margin-top: 10px; border: 1px solid #334155;">
        <img id="live-photo" src="media/latest.jpg" alt="Garden View" style="width: 100%; display: block; object-fit: cover;">
    </div>

</div>

## 72-Hour Telemetry Trends
<div style="position: relative; height: 400px; width: 100%; margin-bottom: 2rem;">
    <canvas id="telemetryChart"></canvas>
</div>

## Live Observer Log

<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
    <span style="font-size: 0.85em; color:#94a3b8; text-transform: uppercase;">Latest AI Insight</span>
    <span id="last-updated" style="font-size: 0.85em; color:#4ade80; font-family: monospace; font-weight: bold;">Syncing...</span>
</div>
<div id="warden-log" style="background-color: #0f172a; padding: 20px; border-radius: 8px; font-family: monospace; font-size: 0.9em; line-height: 1.6; color: #cbd5e1; border: 1px solid #334155;">
    Waiting for report...
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
            // Append timestamp to break browser cache on photo
            const img = document.getElementById('live-photo');
            if (img) img.src = `media/latest.jpg?t=${Date.now()}`;

            const [telemetry, metrics] = await Promise.all([
                parseCSV("data/telemetry.csv"),
                parseCSV("data/metrics.csv")
            ]);

            if (!telemetry.length || !metrics.length) throw new Error("Missing data in CSVs");

            const lastTel = telemetry[telemetry.length - 1];
            const lastMet = metrics[metrics.length - 1];

            // 1. Update Header & Atmosphere
            document.getElementById('last-updated').textContent = `SYNC: ${new Date(lastTel.timestamp).toLocaleTimeString()}`;
            document.getElementById('val-temp').textContent = lastTel.temp || '--';
            document.getElementById('val-hum').textContent = lastTel.hum || '--';
            document.getElementById('val-vpd').textContent = `${lastMet.vpd || '--'}`;
            document.getElementById('val-light').textContent = lastTel.light || '--';

            // 2. Update Plants
            const updatePlant = (id) => {
                const pct = lastMet[`${id}_pct`];
                const isDry = lastMet[`${id}_is_dry`] === "True";
                
                if (pct !== undefined) {
                    document.getElementById(`${id}-val`).textContent = `${pct}%`;
                    const stat = document.getElementById(`${id}-status`);
                    stat.textContent = isDry ? "DRY" : "NOMINAL";
                    stat.style.color = isDry ? '#fca5a5' : '#86efac';
                    stat.style.backgroundColor = isDry ? '#7f1d1d' : '#14532d';
                    stat.style.padding = '2px 6px';
                    stat.style.borderRadius = '4px';
                    stat.style.fontSize = '0.85em';
                }
            };
            ['p1', 'p2', 'p3'].forEach(updatePlant);

            // 3. Join Telemetry and Metrics for the Chart (72-Hour Window) 
            const chartData = metrics.slice(-216).map(m => {
                const t = telemetry.find(tel => tel.timestamp === m.timestamp);
                return t ? { ...m, temp: t.temp, hum: t.hum, light: t.light } : m;
            });
            drawChart(chartData);

            // 4. Update Log from Public Ledger
            const ledgerRes = await fetch('data/ledger.md');
            if (ledgerRes.ok) {
                const text = await ledgerRes.text();
                const entries = text.split(/^## /m);
                const lastEntry = entries[entries.length - 1];
                if (lastEntry) {
                    // Inject raw HTML rendering of markdown 
                    document.getElementById('warden-log').innerHTML = marked.parse("## " + lastEntry.trim());
                }
            }

        } catch (e) { 
            console.error("Dashboard error:", e);
            document.getElementById('last-updated').textContent = "ERROR LOADING DATA";
            document.getElementById('last-updated').style.color = '#f87171';
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
                    { label: 'Nickels', data: data.map(d => d.p1_pct), borderColor: '#4ade80', bg: '#4ade80', tension: 0.3, pointRadius: 0, borderWidth: 2, z: 10 },
                    { label: 'Mint', data: data.map(d => d.p2_pct), borderColor: '#a3e635', bg: '#a3e635', tension: 0.3, pointRadius: 0, borderWidth: 2, z: 10 },
                    { label: 'Pothos', data: data.map(d => d.p3_pct), borderColor: '#facc15', bg: '#facc15', tension: 0.3, pointRadius: 0, borderWidth: 2, z: 10 },
                    { label: 'Temp (°C)', data: data.map(d => d.temp), borderColor: 'rgba(249, 115, 22, 0.4)', tension: 0.3, pointRadius: 0, borderWidth: 1, fill: false },
                    { label: 'Hum (%)', data: data.map(d => d.hum), borderColor: 'rgba(56, 189, 248, 0.4)', tension: 0.3, pointRadius: 0, borderWidth: 1, fill: false },
                    { label: 'Light (Lux)', data: data.map(d => d.light), borderColor: 'rgba(250, 204, 21, 0.8)', tension: 0.3, pointRadius: 0, borderWidth: 1, yAxisID: 'yLux', fill: false }
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

    // Delay initial load slightly to ensure DOM readiness
    setTimeout(() => {
        updateDashboard();
        setInterval(updateDashboard, 300000); // 5 minute sync
    }, 500);
</script>
