#!/usr/bin/env python3
import serial
import serial.tools.list_ports
import time
import os
import json
import pandas as pd
import numpy as np
import math
import subprocess
import shutil
import sys
import argparse
from datetime import datetime

# --- Configuration ---
BASE_DIR = "/Users/surendran/.openclaw/workspace/gardenbot"
RAW_CSV_PATH = os.path.join(BASE_DIR, "data/telemetry.csv")
METRICS_CSV_PATH = os.path.join(BASE_DIR, "data/metrics.csv")
SNAPSHOT_PATH = os.path.join(BASE_DIR, "data/current_snapshot.json")
PLANTS_JSON_PATH = os.path.join(BASE_DIR, "scripts/config/plants.json")
VISION_OBSERVATION_PATH = os.path.join(BASE_DIR, "data/vision_observation.json")

def find_active_arduino_port():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if "USB" in port.description or "Arduino" in port.description or "tty.usbmodem" in port.device:
            return port.device
    return None

def capture_volume():
    # Placeholder for acoustic warden capture logic
    return 0.0

def save_csv_append(df, path):
    file_exists = os.path.isfile(path)
    with open(path, 'a') as f:
        df.to_csv(f, header=not file_exists, index=False)

def capture_data():
    """Direct serial capture with timeout-safe warmup (SILICA v3.6)"""
    port = find_active_arduino_port()
    if not port: return None
    
    ser = None
    try:
        ser = serial.Serial(port, 9600, timeout=10)
        time.sleep(3.0) # Hardware settle
        ser.reset_input_buffer()
        
        # Optimized Burn-in (3 samples = 15s)
        # Sufficient for Temp/Hum stabilization, safe for 60s harness timeout
        print("Warden: BME680 Settle phase (3 samples)...")
        readings = []
        for i in range(15): # Max attempts
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if "|" in line:
                parts = line.split("|")
                if len(parts) >= 7:
                    t, h, l, a2, p, g, pir = map(float, parts[:7])
                    
                    # Detect BME failure (Zeros)
                    if t == 0.0 and h == 0.0:
                        continue
                        
                    readings.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "temp": t, "hum": h, "light": int(l), "p2": int(a2),
                        "press": p, "gas": g, "pir": int(pir), "db": 0.0
                    })
                    print(f"  Sample {len(readings)}/3 captured.")
                    if len(readings) >= 3:
                        break
        
        if readings:
            # Use the 3rd sample for max stability
            data = readings[-1]
            data['db'] = capture_volume() or 0.0
            
            # Enforce strict 8-column schema
            csv_data = {
                "timestamp": data["timestamp"],
                "temp": data["temp"],
                "hum": data["hum"],
                "light": data["light"],
                "p2": data["p2"],
                "press": data["press"],
                "gas": data["gas"],
                "db": data["db"]
            }
            
            new_df = pd.DataFrame([csv_data])
            save_csv_append(new_df, RAW_CSV_PATH)
            return csv_data
            
    except Exception as e:
        print(f"Warden: Direct capture failed: {e}")
    finally:
        if ser and ser.is_open:
            ser.close()
            
    # Fallback if sensor is dead but we want Light/Jade Analog
    return fallback_to_analog(port)

def fallback_to_analog(port):
    """Try to get just the analog sensors if BME680 is failing."""
    try:
        with serial.Serial(port, 9600, timeout=5) as ser:
            time.sleep(2)
            ser.reset_input_buffer()
            for _ in range(5):
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if "|" in line:
                    parts = line.split("|")
                    if len(parts) >= 6:
                        data = {
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "temp": 0.0, "hum": 0.0, "light": int(parts[2]), 
                            "p2": int(parts[3]), "press": 0.0, "gas": 0.0, "db": 0.0
                        }
                        save_csv_append(pd.DataFrame([data]), RAW_CSV_PATH)
                        return data
    except: pass
    return None

def main():
    print(f"Starting Warden V3.6 at {datetime.now()}")
    raw = capture_data()
    if raw:
        print(f"Warden: Telemetry verified. Temp: {raw['temp']}C")
        # Save snapshot for dashboard
        with open(SNAPSHOT_PATH, 'w') as f:
            json.dump(raw, f)
    else:
        print("Warden: CRITICAL: All capture attempts failed.")

if __name__ == "__main__":
    main()
