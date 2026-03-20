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

# --- Configuration ---
BASE_DIR = "/Users/surendran/.openclaw/workspace/gardenbot"
CONFIG_PATH = os.path.join(BASE_DIR, "config/plants.json")
CSV_PATH = os.path.join(BASE_DIR, "data/telemetry.csv")
MEDIA_DIR = os.path.join(BASE_DIR, "media")
ARCHIVE_DIR = os.path.join(BASE_DIR, "archive")
CHART_PATH = os.path.join(MEDIA_DIR, "dashboard.png")
PHOTO_PATH = os.path.join(MEDIA_DIR, "latest.jpg")
CAM_NAME = "USB2.0 PC CAMERA"

# Ensure directories exist
for d in [MEDIA_DIR, ARCHIVE_DIR, os.path.dirname(CSV_PATH)]:
    os.makedirs(d, exist_ok=True)

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
        # Flush buffer
        for _ in range(3): ser.readline()
        
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        ser.close()
        
        if not "|" in line: return {"error": "Invalid data format"}
        
        # Format: TEMP|HUM|LIGHT|A0|A2|A3|A4|A5
        parts = line.split("|")
        
        row = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "temp": float(parts[0]),
            "hum": float(parts[1]),
            "light": int(parts[2])
        }
        
        # Map raw analog values (A0..A5) to Plant IDs
        # The firmware sends: A0, A2, A3, A4, A5 at indices 3, 4, 5, 6, 7
        raw_values = {
            "A0": int(parts[3]),
            "A2": int(parts[4]),
            "A3": int(parts[5]),
            "A4": int(parts[6]),
            "A5": int(parts[7])
        }
        
        for plant in plants:
            pin = plant["sensor_pin"]
            if pin in raw_values:
                row[plant["id"]] = raw_values[pin]
        
        # Save to CSV
        df = pd.DataFrame([row])
        if not os.path.isfile(CSV_PATH) or os.stat(CSV_PATH).st_size == 0:
            df.to_csv(CSV_PATH, index=False)
        else:
            df.to_csv(CSV_PATH, mode='a', header=False, index=False)
            
        return row
    except Exception as e: return {"error": str(e)}

def capture_vision():
    try:
        # 1. Archive Path (organized by date)
        today = datetime.now().strftime("%Y-%m-%d")
        day_dir = os.path.join(ARCHIVE_DIR, today)
        os.makedirs(day_dir, exist_ok=True)
        
        ts = datetime.now().strftime("%H%M%S")
        archive_path = os.path.join(day_dir, f"garden_{ts}.jpg")
        
        # 2. Capture directly to archive
        cmd = ["imagesnap", "-d", CAM_NAME, "-q", archive_path]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # 3. Copy to "latest" for the agent
        subprocess.run(["cp", archive_path, PHOTO_PATH], check=True)
        
        return {"photo_path": PHOTO_PATH, "archive_path": archive_path}
    except Exception as e:
        return {"error": f"Vision failed: {str(e)}"}

def render_dashboard():
    try:
        if not os.path.exists(CSV_PATH): return {"error": "No data"}
        plants = load_plants()
        df = pd.read_csv(CSV_PATH)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        
        # Current time and view window: ALWAYS 4 days total
        now = datetime.now()
        start_view = now - timedelta(hours=48)
        end_view = now + timedelta(hours=48) # Fixed 48h future
        
        # Filter for history
        df_hist = df[df['timestamp'] > start_view].copy()
        if len(df_hist) < 2: return {"error": "Insufficient data for historical view"}

        # Setup Plot
        plt.style.use('dark_background')
        fig, ax1 = plt.subplots(figsize=(15, 10), dpi=100)
        fig.patch.set_facecolor('#000000'); ax1.set_facecolor('#000000')
        ax2 = ax1.twinx(); ax2.grid(False)
        
        # Colors
        C_LIGHT = '#FFD700'; C_TEMP = '#FF3131'; C_HUM = '#00FFFF'; C_PROJ = '#F0FF00'
        
        # 1. Environment
        ax1.fill_between(df_hist['timestamp'], 0, df_hist['light'], color=C_LIGHT, alpha=0.1, label='Light')
        ax2.plot(df_hist['timestamp'], df_hist['temp'], color=C_TEMP, label='Temp °C', linewidth=1.5, alpha=0.8)
        ax2.plot(df_hist['timestamp'], df_hist['hum'], color=C_HUM, label='Humidity %', linewidth=1.5, alpha=0.8)
        
        # 2. Plants & Projections
        for plant in plants:
            pid = plant["id"]
            if pid in df_hist.columns:
                color = plant.get("color", "#00FF41")
                ax1.plot(df_hist['timestamp'], df_hist[pid], color=color, linewidth=4, label=plant["name"], zorder=10)
                
                thresh = plant["dry_threshold"]
                ax1.axhline(y=thresh, color=color, linestyle=':', alpha=0.3)
                
                # Projection Logic
                recent = df_hist[df_hist['timestamp'] > (now - timedelta(hours=24))].copy()
                if len(recent) >= 3:
                    import numpy as np
                    x_reg = (recent['timestamp'] - recent['timestamp'].min()).dt.total_seconds().values
                    y_reg = recent[pid].values
                    slope, intercept = np.polyfit(x_reg, y_reg, 1)
                    
                    if slope > 0.00001: 
                        seconds_to_cross = (thresh - y_reg[-1]) / slope
                        if seconds_to_cross > 0:
                            cross_time = now + timedelta(seconds=seconds_to_cross)
                            # Only plot if within the 48h future window
                            if cross_time < end_view:
                                proj_time = [recent['timestamp'].max(), cross_time]
                                proj_vals = [y_reg[-1], thresh]
                                ax1.plot(proj_time, proj_vals, color=C_PROJ, linestyle='--', linewidth=2, alpha=0.7)
                                ax1.scatter([cross_time], [thresh], color=C_PROJ, s=200, marker='*', edgecolors='white', zorder=20)
                                ax1.text(cross_time, thresh + 20, f" {plant['name']} Dryout\n {cross_time.strftime('%m/%d %I%p')}", color=C_PROJ, fontsize=9)

        # 3. Final Formatting
        ax1.set_xlim(start_view, end_view)
        ax1.set_ylim(0, 1024)
        ax2.set_ylim(10, 60)
        
        # Align Grid
        ax1.yaxis.set_major_locator(ticker.LinearLocator(6))
        ax2.yaxis.set_major_locator(ticker.LinearLocator(6))
        ax1.grid(True, which='major', linestyle='--', alpha=0.2)
        
        # Shade Future
        ax1.axvspan(now, end_view, color='#ffffff', alpha=0.05)
        ax1.axvline(x=now, color='#ffffff', linestyle='-', alpha=0.5)
        ax1.text(now, 1000, " PRESENT", color='#ffffff', alpha=0.8, fontsize=10, fontweight='bold')

        ax1.set_ylabel("Moisture Index / Light")
        ax2.set_ylabel("Environment (Temp / Hum)")
        ax1.set_title("GARDENOS: 4-DAY BIOMETRIC ANALYSIS (48H HISTORY + 48H PROJECTION)", fontsize=18, pad=30)
        
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d\n%I%p'))
        plt.xticks(rotation=0)
        
        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        ax1.legend(h1+h2, l1+l2, loc='upper left', facecolor='#111111', frameon=True, edgecolor='#333333')
        
        plt.tight_layout()
        fig.subplots_adjust(bottom=0.15, right=0.9) # Ensure labels fit
        plt.savefig(CHART_PATH, facecolor='#000000')
        plt.close()
        return {"chart_path": CHART_PATH}
    except Exception as e: 
        import traceback
        return {"error": f"{str(e)}\n{traceback.format_exc()}"}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--capture", action="store_true")
    parser.add_argument("--dashboard", action="store_true")
    parser.add_argument("--vision", action="store_true")
    args = parser.parse_args()
    
    res = {}
    if args.capture: res["capture"] = capture_data()
    if args.vision: res["vision"] = capture_vision()
    if args.dashboard: res["dashboard"] = render_dashboard()
    print(json.dumps(res, indent=2))