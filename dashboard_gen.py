import sqlite3
import os
import glob
import time
from datetime import datetime

def generate_dashboard():
    conn = sqlite3.connect('data/garden.db')
    c = conn.cursor()
    
    # Get latest sensor reading
    c.execute("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 1")
    latest = c.fetchone()
    
    # Get last 48 readings for the chart (approx 2 days of pulses)
    c.execute("SELECT timestamp, soil, temp, hum, water_vol FROM sensor_data ORDER BY timestamp DESC LIMIT 48")
    history = c.fetchall()[::-1]
    
    # Get latest photo
    photo_list = glob.glob('photos/*.jpg') + glob.glob('photos/*.jpeg') + glob.glob('photos/*.png')
    latest_photo = max(photo_list, key=os.path.getctime) if photo_list else None
    
    conn.close()

    if not latest:
        return "Waiting for first pulse..."

    # Prepare data for Chart.js
    labels = [row[0].split()[1][:5] for row in history]
    soil_data = [row[1] for row in history]
    temp_data = [row[2] for row in history]
    water_data = [row[4] for row in history]

    # Arid Architect Logic
    soil_val = int(latest[4])
    water_ml = float(latest[7])
    temp_val = float(latest[2])
    
    # Determine Health Status
    if soil_val < 400:
        status = "DRENCHED"
        status_color = "#38bdf8" # Sky Blue
        advice = "Soil is very wet. Avoid watering to prevent root rot."
    elif soil_val < 750:
        status = "HEALTHY"
        status_color = "#0d9488" # Teal
        advice = "Optimal moisture for a String of Nickels."
    else:
        status = "THIRSTY"
        status_color = "#f59e0b" # Amber
        advice = "Soil is dry. Monitor for 2 days before watering."

    if water_ml < 100:
        status = "TANK LOW"
        status_color = "#ef4444" # Red
        advice = "Refill the coffee sipper immediately to protect the pump."

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Arid Architect | Terminal Dashboard</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            :root {{
                --bg: #030712;
                --card-bg: rgba(17, 24, 39, 0.8);
                --text-main: #f9fafb;
                --text-dim: #9ca3af;
                --accent-mind: #6366f1;
                --accent-build: #14b8a6;
                --accent-soul: #f59e0b;
            }}
            body {{ 
                background: var(--bg); 
                color: var(--text-main); 
                font-family: 'JetBrains Mono', 'SF Mono', monospace;
                margin: 0; padding: 40px;
                background-image: radial-gradient(circle at 2px 2px, rgba(255,255,255,0.05) 1px, transparent 0);
                background-size: 40px 40px;
            }}
            .container {{ max-width: 1100px; margin: auto; }}
            
            /* Glassmorphism Header */
            header {{
                display: flex; justify-content: space-between; align-items: center;
                margin-bottom: 40px; border-bottom: 1px solid rgba(255,255,255,0.1);
                padding-bottom: 20px;
            }}
            .status-badge {{
                background: {status_color}; color: #000;
                padding: 4px 12px; border-radius: 4px; font-weight: 800; font-size: 0.8rem;
            }}

            /* Grid Layout */
            .grid {{ display: grid; grid-template-columns: repeat(12, 1fr); gap: 24px; }}
            .card {{ 
                background: var(--card-bg); 
                backdrop-filter: blur(12px); 
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 16px; padding: 24px;
            }}
            
            /* Components */
            .col-4 {{ grid-column: span 4; }}
            .col-8 {{ grid-column: span 8; }}
            .col-12 {{ grid-column: span 12; }}

            .stat-label {{ color: var(--text-dim); font-size: 0.7rem; text-transform: uppercase; letter-spacing: 2px; }}
            .stat-value {{ font-size: 2.4rem; font-weight: 700; margin: 10px 0; color: var(--accent-build); }}
            
            .architect-log {{ 
                border-left: 2px solid var(--accent-mind); 
                padding-left: 20px; font-style: italic; color: var(--text-dim);
                line-height: 1.6; font-size: 0.95rem;
            }}
            
            .plant-photo {{ width: 100%; border-radius: 12px; object-fit: cover; height: 300px; border: 1px solid rgba(255,255,255,0.1); }}
            canvas {{ margin-top: 20px; }}

            @media (max-width: 900px) {{ .col-4, .col-8 {{ grid-column: span 12; }} }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <div>
                    <span class="stat-label">System Active // Chennai, IN</span>
                    <h1 style="margin: 0; font-size: 1.5rem;">ARID ARCHITECT v1.0</h1>
                </div>
                <div style="text-align: right;">
                    <div class="status-badge">{status}</div>
                    <div class="stat-label" style="margin-top: 8px;">{latest[1]}</div>
                </div>
            </header>

            <div class="grid">
                <!-- Architect's Assessment -->
                <div class="card col-8">
                    <div class="stat-label">Architect's Internal Log</div>
                    <p class="architect-log">
                        "Initial pulse detected for the String of Nickels. {advice} 
                        The ambient temperature is {temp_val}°C with {latest[3]}% humidity. 
                        Water level in the coffee sipper is at {water_ml}ml."
                    </p>
                </div>

                <!-- Environment Stats -->
                <div class="card col-4">
                    <div class="stat-label">Soil Moisture</div>
                    <div class="stat-value" style="color: var(--accent-soul);">{soil_val}</div>
                    <div class="stat-label">Target: 400 - 750</div>
                </div>

                <!-- Photo Gallery -->
                <div class="card col-4">
                    <div class="stat-label">Visual Growth Tracking</div>
                    {f'<img src="{latest_photo}" class="plant-photo">' if latest_photo else '<div class="plant-photo" style="display:flex; align-items:center; justify-content:center; background:#111;">Awaiting Photo</div>'}
                </div>

                <!-- Charts -->
                <div class="card col-8">
                    <div class="stat-label">Pulse History (48h)</div>
                    <div style="height: 250px;"><canvas id="historyChart"></canvas></div>
                </div>

                <div class="card col-12" style="text-align: center; border: none; background: transparent;">
                    <span class="stat-label">Designed for The Infinite Game // Surendran's Workspace</span>
                </div>
            </div>
        </div>

        <script>
            const ctx = document.getElementById('historyChart').getContext('2d');
            new Chart(ctx, {{
                type: 'line',
                data: {{
                    labels: {labels},
                    datasets: [{{
                        label: 'Soil', data: {soil_data}, borderColor: '#14b8a6', borderWidth: 2, tension: 0.4, pointRadius: 0
                    }}, {{
                        label: 'Water (ml)', data: {water_data}, borderColor: '#6366f1', borderWidth: 2, tension: 0.4, pointRadius: 0, borderDash: [5, 5]
                    }}]
                }},
                options: {{ 
                    responsive: true, maintainAspectRatio: false,
                    plugins: {{ legend: {{ display: true, labels: {{ color: '#9ca3af', font: {{ family: 'JetBrains Mono' }} }} }} }},
                    scales: {{ 
                        x: {{ grid: {{ display: false }}, ticks: {{ color: '#4b5563' }} }},
                        y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#4b5563' }} }}
                    }}
                }}
            }});
        </script>
    </body>
    </html>
    """
    
    with open('dashboard.html', 'w') as f:
        f.write(html_content)
    print("Architect Dashboard Generated.")

if __name__ == "__main__":
    generate_dashboard()
