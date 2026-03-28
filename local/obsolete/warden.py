#!/usr/bin/env python3
import serial
import serial.tools.list_ports
import time
import os
import json
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from datetime import datetime, timedelta
import hashlib
import shutil
import numpy as np
import math

# --- Configuration ---
BASE_DIR = "/Users/surendran/.openclaw/workspace/gardenbot"
CONFIG_PATH = os.path.join(BASE_DIR, "config/plants.json")
CSV_PATH = os.path.join(BASE_DIR, "data/telemetry.csv")
MEDIA_DIR = os.path.join(BASE_DIR, "media")
CHART_PATH = os.path.join(MEDIA_DIR, "dashboard.png")
SNAPSHOT_PATH = os.path.join(BASE_DIR, "data/current_snapshot.json")
PHOTO_PATH = os.path.join(MEDIA_DIR, "latest.jpg")
WEATHER_PATH = os.path.join(BASE_DIR, "data/weather_context.json")
LEDGER_PATH = os.path.join(BASE_DIR, "logs/vision_ledger.md")
MILESTONES_PATH = os.path.join(BASE_DIR, "logs/growth_milestones.md")
LAST_HASH_FILE = os.path.join(BASE_DIR, "docs/.last_push_hash")

# Ensure directories exist
os.makedirs(MEDIA_DIR, exist_ok=True)

def load_plants():
    if not os.path.exists(CONFIG_PATH): return []
    with open(CONFIG_PATH, 'r') as f: return json.load(f)

def get_arduino_port():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if "usbmodem" in p.device: return p.device
    return None

def capture_data():
    plants = load_plants()
    port = get_arduino_port()
    if not port: return {"error": "Arduino not found"}
    try:
        ser = serial.Serial(port, 9600, timeout=5)
        time.sleep(2)
        ser.reset_input_buffer()
        for _ in range(5): ser.readline()
        line = ""
        for _ in range(10):
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if "|" in line: break
        ser.close()
        if not "|" in line: return {"error": "Invalid data format"}
        parts = line.split("|")
        row = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "temp": float(parts[0]), "hum": float(parts[1]), "light": int(parts[2])
        }
        if len(parts) >= 6:
            raw_values = {"A0": int(parts[3]), "A2": int(parts[4]), "A5": int(parts[5])}
            for plant in plants:
                if plant["id"] in ["p1", "p2", "p3"]:
                    pin = plant.get("sensor_pin")
                    if pin in raw_values: row[plant["id"]] = raw_values[pin]
        df = pd.DataFrame([row])
        header = not os.path.isfile(CSV_PATH) or os.stat(CSV_PATH).st_size == 0
        df.to_csv(CSV_PATH, mode='a', header=header, index=False)
        return row
    except Exception as e: return {"error": str(e)}

def calculate_vpd(temp_c, hum_rh):
    svp = 0.61078 * math.exp((17.27 * temp_c) / (temp_c + 237.3))
    avp = svp * (hum_rh / 100.0)
    return round(svp - avp, 3)

def compute_slopes(df, plants, weather):
    now = datetime.now()
    cutoff = now - timedelta(hours=72)
    df_recent = df[df['timestamp'] >= cutoff].copy()
    slopes = {}
    if len(df_recent) < 5: return slopes
    forecast_hum = weather.get("main", {}).get("humidity", 50)
    weight = 0.8 if forecast_hum > 70 else 1.2 if forecast_hum < 30 else 1.0
    for plant in plants:
        pid = plant["id"]
        if pid in df_recent.columns:
            y = df_recent[pid].values
            x = (df_recent['timestamp'] - df_recent['timestamp'].min()).dt.total_seconds().values / 3600.0
            m, b = np.polyfit(x, y, 1)
            weighted_m = min(5.0, m * weight)
            thresh = plant["raw_dry"]
            ttcd = round((thresh - y[-1]) / weighted_m, 1) if weighted_m > 0.001 else None
            slopes[pid] = {"slope_per_hour": round(weighted_m, 4), "estimated_hours_to_dryout": ttcd}
    return slopes

def compute_moisture_stats(row, plants):
    stats = {}
    raw_data_map = {p["id"]: row[p["id"]] for p in plants if p["id"] in row}
    for plant in plants:
        pid = plant["id"]
        raw = raw_data_map.get(plant.get("linked_to", pid))
        if raw is None: continue
        wet, dry = plant["raw_wet"], plant["raw_dry"]
        if raw <= 0: stats[pid] = {"error": "Short Circuit", "raw": raw}; continue
        moisture_pct = max(0, min(100, round(100 - ((raw - wet) / (dry - wet) * 100), 1)))
        stats[pid] = {"moisture_pct": moisture_pct, "raw": raw, "is_dry": moisture_pct < plant["dry_threshold_pct"]}
    return stats

def check_alerts(snapshot):
    moisture_analysis = snapshot.get("moisture_analysis", {})
    plants_info = {p["id"]: p for p in load_plants()}
    current_alerts = []
    for pid, stats in moisture_analysis.items():
        name = plants_info.get(pid, {}).get("name", pid)
        if stats.get("is_dry"):
            current_alerts.append(f"🚨 *EMERGENCY ALERT*: {name} is DRY ({stats.get('moisture_pct')}%).")
    if not current_alerts: return
    alert_state_path = os.path.join(BASE_DIR, "data/alert_state.json")
    last_state = {}
    if os.path.exists(alert_state_path):
        try:
            with open(alert_state_path, 'r') as f: last_state = json.load(f)
        except: pass
    now_ts = datetime.now().timestamp()
    if set(current_alerts) != set(last_state.get("alerts", [])) or (now_ts - last_state.get("timestamp", 0)) > 14400:
        subprocess.run(["/Users/surendran/.pnpm-global/openclaw", "message", "send", "--target", "C0AK6A4SJES", "--message", "\n".join(current_alerts)], capture_output=True)
        with open(alert_state_path, 'w') as f: json.dump({"timestamp": now_ts, "alerts": current_alerts}, f)

def render_dashboard():
    try:
        plants = load_plants()
        df = pd.read_csv(CSV_PATH)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        
        now = datetime.now()
        start_view = now - timedelta(hours=48)
        end_view = now + timedelta(hours=48)
        
        df_hist = df[df['timestamp'] > start_view].copy()
        if len(df_hist) < 3: return
        
        plt.style.use('dark_background')
        fig, ax1 = plt.subplots(figsize=(15, 10), dpi=100)
        fig.patch.set_facecolor('#000000'); ax1.set_facecolor('#000000')
        ax2 = ax1.twinx(); ax2.grid(False)
        
        # 1. Environment
        ax1.fill_between(df_hist['timestamp'], 0, df_hist['light'], color='#FFD700', alpha=0.1, label='Light')
        ax2.plot(df_hist['timestamp'], df_hist['temp'], color='#FF3131', label='Temp °C', linewidth=1, alpha=0.7)
        ax2.plot(df_hist['timestamp'], df_hist['hum'], color='#00FFFF', label='Hum %', linewidth=1, alpha=0.7)
        
        # 2. Plants & Projections
        for plant in plants:
            pid = plant["id"]
            if pid in ["p5", "p6"]: continue
            sid = plant.get("linked_to", pid)
            if sid in df_hist.columns:
                color = plant.get("color", "#00FF41")
                ax1.plot(df_hist['timestamp'], df_hist[sid], color=color, linewidth=2, label=plant["name"])
                
                # Simple linear projection for the dashboard screenshot
                y = df_hist[sid].values
                x = (df_hist['timestamp'] - df_hist['timestamp'].min()).dt.total_seconds().values
                m, b = np.polyfit(x, y, 1)
                
                if m > 0.00001:
                    thresh = plant["raw_dry"]
                    seconds_to_cross = (thresh - y[-1]) / m
                    if 0 < seconds_to_cross < (48 * 3600):
                        cross_time = now + timedelta(seconds=seconds_to_cross)
                        ax1.plot([now, cross_time], [y[-1], thresh], color='#F0FF00', linestyle='--', alpha=0.6)
                        ax1.scatter([cross_time], [thresh], color='#F0FF00', s=100, marker='*')

        # 3. Present Marker
        ax1.axvline(x=now, color='#ffffff', linestyle='-', alpha=0.5)
        ax1.text(now, 1000, " PRESENT", color='#ffffff', fontsize=10, fontweight='bold')
        ax1.axvspan(now, end_view, color='#ffffff', alpha=0.03) # Shade the future
        
        ax1.set_xlim(start_view, end_view)
        ax1.set_ylim(0, 1024)
        ax1.set_title("GARDENOS: 4-DAY PREDICTIVE DASHBOARD", fontsize=18, pad=20)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
        
        plt.tight_layout()
        plt.savefig(CHART_PATH, facecolor='#000000')
        plt.close()
    except Exception as e:
        print(f"Dashboard Failure: {e}")

def generate_snapshot(capture_res=None):
    plants = load_plants()
    df = pd.read_csv(CSV_PATH, on_bad_lines='skip'); df['timestamp'] = pd.to_datetime(df['timestamp'])
    # If no fresh data, grab the latest row from CSV
    if capture_res is None:
        latest_row = df.iloc[-1].to_dict()
        # Ensure timestamp is string for JSON
        if 'timestamp' in latest_row and not isinstance(latest_row['timestamp'], str):
            latest_row['timestamp'] = latest_row['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        capture_res = latest_row
    weather = json.load(open(WEATHER_PATH)) if os.path.exists(WEATHER_PATH) else {}
    snapshot = {
        "timestamp": datetime.now().isoformat(), "sensors": capture_res,
        "moisture_analysis": compute_moisture_stats(capture_res, plants),
        "environment": {"vpd_kpa": calculate_vpd(capture_res["temp"], capture_res["hum"]), "weather_forecast": weather},
        "intelligence": {"slopes": compute_slopes(df, plants, weather)}
    }
    check_alerts(snapshot)
    with open(SNAPSHOT_PATH, 'w') as f: json.dump(snapshot, f, indent=2)
    try:
        # Sync snapshot, telemetry, photo, AND dashboard to GitHub Pages
        h = hashlib.sha256(open(SNAPSHOT_PATH, 'rb').read() + open(PHOTO_PATH, 'rb').read()).hexdigest()
        if h != (open(LAST_HASH_FILE).read().strip() if os.path.exists(LAST_HASH_FILE) else ""):
            for f in [SNAPSHOT_PATH, CSV_PATH, PHOTO_PATH, CHART_PATH]: 
                target = os.path.join(BASE_DIR, "docs/data/" if "data" in f or ".csv" in f else "docs/media/" if "media" in f else "docs/")
                os.makedirs(os.path.dirname(target), exist_ok=True)
                shutil.copy2(f, target)
            subprocess.run(["git", "add", "."], cwd=BASE_DIR); subprocess.run(["git", "commit", "-m", "Auto-update"], cwd=BASE_DIR); subprocess.run(["git", "push"], cwd=BASE_DIR)
            open(LAST_HASH_FILE, 'w').write(h)
    except Exception as e:
        print(f"Sync Failure: {e}")
    return snapshot

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--capture", action="store_true")
    parser.add_argument("--snapshot", action="store_true")
    parser.add_argument("--dashboard", action="store_true")
    args = parser.parse_args()
    res = {}
    if args.capture: res["capture"] = capture_data()
    if args.dashboard: render_dashboard()
    if args.snapshot or args.capture: res["snapshot"] = generate_snapshot(res.get("capture"))
    print(json.dumps(res, indent=2))