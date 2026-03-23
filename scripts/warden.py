#!/usr/bin/env python3
import serial
import serial.tools.list_ports
import time
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import numpy as np
import math
import subprocess
import shutil
import sys
import argparse
from datetime import datetime, timedelta

# --- Configuration ---
BASE_DIR = "/Users/surendran/.openclaw/workspace/gardenbot"
CONFIG_PATH = os.path.join(BASE_DIR, "config/plants.json")
RAW_CSV_PATH = os.path.join(BASE_DIR, "docs/data/telemetry.csv")
METRICS_CSV_PATH = os.path.join(BASE_DIR, "docs/data/metrics.csv")
SNAPSHOT_PATH = os.path.join(BASE_DIR, "docs/data/current_snapshot.json")
WEATHER_PATH = os.path.join(BASE_DIR, "docs/data/weather_context.json")
CHART_PATH = os.path.join(BASE_DIR, "docs/media/dashboard.png")
PHOTO_PATH = os.path.join(BASE_DIR, "docs/media/latest.jpg")

def load_plants():
    if not os.path.exists(CONFIG_PATH): return []
    with open(CONFIG_PATH, 'r') as f: return json.load(f)

def find_active_arduino_port():
    """Scans for a port streaming valid gardenbot data (pipe-delimited)."""
    candidates = [p.device for p in serial.tools.list_ports.comports() 
                 if "usbmodem" in p.device or "usbserial" in p.device]
    
    if not candidates:
        print("Warden: No candidate ports found (usbmodem/usbserial).")
        return None

    print(f"Warden: Scanning ports: {candidates}...")
    
    for port in candidates:
        try:
            print(f"  Checking {port}...")
            ser = serial.Serial(port, 9600, timeout=3)
            time.sleep(2) # Wait for Arduino reset
            ser.reset_input_buffer()
            
            # Read a few lines to check for valid data format
            for _ in range(10):
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if "|" in line and len(line.split("|")) >= 6:
                    print(f"Warden: Valid stream found on {port}")
                    ser.close()
                    return port
            ser.close()
        except Exception as e:
            print(f"  Skipping {port}: {e}")
            
    print("Warden: No active Gardenbot found.")
    return None

def capture_data():
    port = find_active_arduino_port()
    if not port: return None
    
    try:
        ser = serial.Serial(port, 9600, timeout=5)
        time.sleep(2)
        ser.reset_input_buffer()
        for _ in range(5): ser.readline() # Flush
        
        # Try capturing valid line
        for _ in range(5):
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if "|" in line:
                parts = line.split("|")
                if len(parts) >= 6:
                    data = {
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "temp": float(parts[0]), 
                        "hum": float(parts[1]), 
                        "light": int(parts[2]),
                        "p1": int(parts[3]), # A0
                        "p2": int(parts[5]), # A5
                        "p3": int(parts[4])  # A2
                    }
                    ser.close()
                    
                    new_df = pd.DataFrame([data])
                    if os.path.exists(RAW_CSV_PATH):
                        try:
                            existing_df = pd.read_csv(RAW_CSV_PATH)
                            final_df = pd.concat([existing_df, new_df], ignore_index=True)
                        except pd.errors.EmptyDataError:
                            final_df = new_df
                    else:
                        final_df = new_df
                        
                    final_df.to_csv(RAW_CSV_PATH, index=False)
                    return data
        ser.close()
    except Exception as e:
        print(f"Warden: Capture failed on {port}: {e}")
    return None

def compute_metrics(raw_row, plants):
    if not raw_row or not isinstance(raw_row, dict): return None
    try:
        t, h = raw_row.get("temp", 25), raw_row.get("hum", 50)
        svp = 0.61078 * math.exp((17.27 * t) / (t + 237.3))
        vpd = round(svp - (svp * (h / 100.0)), 3)
        metrics = {"timestamp": raw_row.get("timestamp"), "vpd": vpd}
        for p in plants:
            pid = p["id"]
            raw_val = raw_row.get(pid)
            if raw_val is not None:
                wet, dry = p["raw_wet"], p["raw_dry"]
                if dry != wet:
                    pct = 100 - ((float(raw_val) - wet) / (dry - wet) * 100)
                    metrics[f"{pid}_pct"] = max(0, min(100, round(pct, 1)))
                    metrics[f"{pid}_is_dry"] = metrics[f"{pid}_pct"] < p["dry_threshold_pct"]
        
        new_df = pd.DataFrame([metrics])
        if os.path.exists(METRICS_CSV_PATH):
            try:
                existing_df = pd.read_csv(METRICS_CSV_PATH)
                final_df = pd.concat([existing_df, new_df], ignore_index=True)
            except pd.errors.EmptyDataError:
                final_df = new_df
        else:
            final_df = new_df
            
        final_df.to_csv(METRICS_CSV_PATH, index=False)
        return metrics
    except Exception as e:
        print(f"Warden: Metrics error: {e}")
        return None

def render_dashboard(plants):
    try:
        if not os.path.exists(RAW_CSV_PATH): return
        df = pd.read_csv(RAW_CSV_PATH)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        now = datetime.now()
        df_view = df[df['timestamp'] > (now - timedelta(hours=48))].copy()
        if len(df_view) < 2: return
        
        plt.style.use('dark_background')
        fig, ax1 = plt.subplots(figsize=(15, 10), dpi=100)
        fig.patch.set_facecolor('#000000'); ax1.set_facecolor('#000000')
        ax2 = ax1.twinx()
        
        for p in plants:
            pid = p["id"]
            if pid in df_view.columns:
                ax1.plot(df_view['timestamp'], df_view[pid], color=p["color"], label=p["name"], linewidth=2)
        
        ax2.plot(df_view['timestamp'], df_view['temp'], color='red', alpha=0.3, label='Temp')
        ax2.plot(df_view['timestamp'], df_view['hum'], color='cyan', alpha=0.3, label='Hum')
        
        ax1.set_xlim(now - timedelta(hours=48), now + timedelta(hours=48))
        ax1.set_ylim(0, 1024); ax2.set_ylim(10, 60)
        ax1.legend(loc='upper left'); ax1.grid(alpha=0.1)
        plt.title("GARDENOS BIOMETRIC TRENDS (48H HISTORY)")
        plt.savefig(CHART_PATH); plt.close()
    except Exception as e: print(f"Warden: Dashboard error: {e}")

def save_snapshot(raw, metrics, plants):
    # FALLBACK: If fresh capture failed, read last row from CSV
    if not raw:
        print("Warden: Capture failed, attempting CSV fallback...")
        try:
            df_raw = pd.read_csv(RAW_CSV_PATH).tail(1)
            if not df_raw.empty:
                raw = df_raw.iloc[0].to_dict()
                print(f"Warden: Fallback raw data found: {raw}")
                if not metrics:
                    metrics = compute_metrics(raw, plants)
        except Exception as e:
            print(f"Warden: Fallback failed: {e}")

    snapshot = {
        "timestamp": datetime.now().isoformat(), 
        "sensors": raw or {}, 
        "moisture_analysis": {}, 
        "environment": {"vpd_kpa": metrics.get("vpd") if metrics else None}, 
        "intelligence": {"recent_visual_ledger": []}
    }
    
    if metrics:
        for p in plants:
            pid = p["id"]
            if f"{pid}_pct" in metrics:
                snapshot["moisture_analysis"][pid] = {
                    "moisture_pct": metrics.get(f"{pid}_pct"),
                    "is_dry": metrics.get(f"{pid}_is_dry")
                }
    
    ledger_path = os.path.join(BASE_DIR, "logs/vision_ledger.md")
    if os.path.exists(ledger_path):
        try:
            with open(ledger_path, 'r') as f:
                content = f.read()
                sections = content.split("## ")
                snapshot["intelligence"]["recent_visual_ledger"] = [s.strip() for s in sections[-3:] if s.strip()]
        except: pass

    with open(SNAPSHOT_PATH, 'w') as f: json.dump(snapshot, f, indent=2)
    print(f"Warden: Snapshot saved to {SNAPSHOT_PATH}")

def git_sync():
    print("Warden: Syncing to GitHub...")
    try:
        subprocess.run(["git", "add", "docs/"], cwd=BASE_DIR, check=True)
        status_res = subprocess.run(["git", "status", "--porcelain"], cwd=BASE_DIR, capture_output=True, text=True).stdout
        if status_res:
            msg = f"Warden Cycle: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            subprocess.run(["git", "commit", "-m", msg], cwd=BASE_DIR, check=True)
            subprocess.run(["git", "push", "origin", "main"], cwd=BASE_DIR, check=True)
            print("Warden: GitHub Sync Successful.")
        else:
            print("Warden: Nothing to sync.")
    except Exception as e:
        print(f"Warden: GitHub Sync Failed: {e}")

# --- Calibration Helpers ---

def collect_once():
    """Reads a single line from the Arduino, parses sensor values, and returns them."""
    # Uses the new scanning function to find the correct port
    port = find_active_arduino_port() 
    
    if not port:
        print("Warden: No active Arduino found for calibration.")
        return None
    
    print(f"Connecting to {port} for calibration capture...")
    try:
        ser = serial.Serial(port, 9600, timeout=5)
        time.sleep(2) # Wait for reset
        ser.reset_input_buffer()
        
        # Flush a few lines to get fresh data
        for _ in range(5): 
            ser.readline()
            
        # Read valid line
        for _ in range(5):
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if "|" in line:
                parts = line.split("|")
                if len(parts) >= 6:
                    # Parsing logic matches capture_data
                    # parts[3] -> p1 (A0)
                    # parts[5] -> p2 (A5)
                    # parts[4] -> p3 (A2)
                    data = {
                        "p1": int(parts[3]),
                        "p2": int(parts[5]),
                        "p3": int(parts[4])
                    }
                    ser.close()
                    return data
        ser.close()
        print("Warden: timeout waiting for valid data format during calibration.")
        return None
    except Exception as e:
        print(f"Warden: Calibration connection error: {e}")
        return None

def write_baseline_file(data):
    """Serializes data to JSON with timestamp and writes to docs/data/baseline_....json"""
    ts_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"baseline_{ts_str}.json"
    filepath = os.path.join(BASE_DIR, "docs/data", filename)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Baseline data saved to: {filepath}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gardenbot Warden Script")
    parser.add_argument("--baseline", action="store_true", help="Run sensor baseline calibration mode")
    args = parser.parse_args()

    if args.baseline:
        print("=== Sensor Baseline Calibration Mode ===")
        
        input("1. Place sensors in WET condition (dunked in water). Press Enter to capture...")
        wet_data = collect_once()
        if not wet_data:
            print("Failed to capture wet data. Aborting.")
            sys.exit(1)
        print(f"Wet data captured: {wet_data}")
        
        input("2. Place sensors in DRY condition (air). Press Enter to capture...")
        dry_data = collect_once()
        if not dry_data:
            print("Failed to capture dry data. Aborting.")
            sys.exit(1)
        print(f"Dry data captured: {dry_data}")
        
        full_data = {
            "timestamp": datetime.now().isoformat(),
            "wet": wet_data,
            "dry": dry_data
        }
        
        write_baseline_file(full_data)
        sys.exit(0)

    plants = load_plants()
    raw = capture_data()
    metrics = compute_metrics(raw, plants)
    render_dashboard(plants)
    save_snapshot(raw, metrics, plants)
    git_sync()
    print("Warden: Run complete.")
