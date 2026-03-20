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
        
        # View Window (Last 48h)
        start_time = datetime.now() - timedelta(hours=48)
        df = df[df['timestamp'] > start_time]
        if len(df) < 2: return {"error": "Insufficient data"}

        # Setup Plot
        plt.style.use('dark_background')
        fig, ax1 = plt.subplots(figsize=(15, 10))
        fig.patch.set_facecolor('#000000'); ax1.set_facecolor('#000000')
        ax2 = ax1.twinx(); ax2.grid(False)
        
        # Plot Environment
        ax1.fill_between(df['timestamp'], 0, df['light'], color='#FFD700', alpha=0.1, label='Light')
        ax2.plot(df['timestamp'], df['temp'], color='#FF3131', label='Temp', linewidth=1.5)
        ax2.plot(df['timestamp'], df['hum'], color='#00FFFF', label='Humidity', linewidth=1.5)
        
        # Plot Plants
        for plant in plants:
            pid = plant["id"]
            if pid in df.columns:
                # Plot line
                ax1.plot(df['timestamp'], df[pid], color=plant["color"], linewidth=3, label=plant["name"])
                
                # Add Threshold Dashes
                ax1.axhline(y=plant["dry_threshold"], color=plant["color"], linestyle=':', alpha=0.5)

        # Formatting
        ax1.set_ylim(0, 1024); ax1.set_ylabel("Moisture Index")
        ax2.set_ylim(10, 50); ax2.set_ylabel("Env (°C / %)")
        ax1.set_title("GARDENOS: LIVE MONITORING", fontsize=18, pad=20)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%I%p\n%d'))
        ax1.legend(loc='upper left', facecolor='#111111')
        ax2.legend(loc='upper right', facecolor='#111111')
        
        plt.tight_layout()
        plt.savefig(CHART_PATH, facecolor='#000000')
        plt.close()
        return {"chart_path": CHART_PATH}
    except Exception as e: return {"error": str(e)}

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