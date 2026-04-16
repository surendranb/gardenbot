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
from datetime import datetime, timedelta
from acoustic_warden import capture_volume

# --- Configuration ---
BASE_DIR = "/Users/surendran/.openclaw/workspace/gardenbot"
CONFIG_PATH = os.path.join(BASE_DIR, "scripts/config/plants.json")
RAW_CSV_PATH = os.path.join(BASE_DIR, "data/telemetry.csv")
METRICS_CSV_PATH = os.path.join(BASE_DIR, "data/metrics.csv")
SNAPSHOT_PATH = os.path.join(BASE_DIR, "data/current_snapshot.json")
STATE_PATH = os.path.join(BASE_DIR, "data/warden_state.json")
WEATHER_PATH = os.path.join(BASE_DIR, "data/weather_context.json")
VISION_OBSERVATION_PATH = os.path.join(BASE_DIR, "data/vision_observation.json")
PHOTO_PATH = os.path.join(BASE_DIR, "media/latest.jpg")
ARCHIVE_DIR = os.path.join(BASE_DIR, "archive")

def load_plants():
    if not os.path.exists(CONFIG_PATH): return []
    with open(CONFIG_PATH, 'r') as f: return json.load(f)

def load_warden_state():
    """Loads the persistent reasoning state (Hypothesis Engine)."""
    state = {"last_hypothesis": "Initial Observation", "active_concerns": [], "consecutive_drops": 0}
    if os.path.exists(STATE_PATH):
        try:
            with open(STATE_PATH, 'r') as f:
                loaded = json.load(f)
                state.update(loaded)
        except: pass
    return state

def save_warden_state(state):
    with open(STATE_PATH, 'w') as f: json.dump(state, f, indent=2)

def execute_hardware_reset(port):
    """Bypasses normal flow to force a DTR reset on the Arduino."""
    print(f"Warden: Triggering HARDWARE DTR RESET on {port} due to consecutive drops.")
    try:
        ser = serial.Serial(port, 9600)
        ser.setDTR(False)
        time.sleep(0.5)
        ser.setDTR(True)
        ser.close()
        print("Warden: DTR Reset successful. Waiting 4.0s for Arduino boot sequence...")
        time.sleep(4.0)
    except Exception as e:
        print(f"Warden: Failed to trigger DTR reset: {e}")

def get_temporal_vision_stack():
    """Retrieves paths for Anchor (6AM), Previous (T-3h), and Current photos."""
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    day_dir = os.path.join(ARCHIVE_DIR, today_str)
    
    stack = {"anchor": None, "previous": None, "current": PHOTO_PATH}
    
    if os.path.exists(day_dir):
        files = sorted([f for f in os.listdir(day_dir) if f.endswith(".jpg")])
        if files:
            # Anchor: prefer the first 06:xx capture, then 07:xx, then oldest available.
            for prefix in ("garden_06", "garden_07"):
                for f in files:
                    if f.startswith(prefix):
                        stack["anchor"] = os.path.join(day_dir, f)
                        break
                if stack["anchor"]:
                    break
            if not stack["anchor"]:
                stack["anchor"] = os.path.join(day_dir, files[0])

            # Previous: most recent archived image before the current capture.
            if len(files) >= 2:
                stack["previous"] = os.path.join(day_dir, files[-2])
                
    return stack

def load_vision_observation():
    """Loads the structured visual interpretation produced by vision.py."""
    if not os.path.exists(VISION_OBSERVATION_PATH):
        return {}
    try:
        with open(VISION_OBSERVATION_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Warden: Failed to load vision observation: {e}")
        return {"error": str(e)}

def derive_hypothesis(raw, metrics, plants):
    """Produces a compact state update for the next run."""
    if not raw or not metrics:
        return {
            "last_hypothesis": "Insufficient telemetry; awaiting next valid capture.",
            "active_concerns": ["missing-telemetry"]
        }

    concerns = []
    dry_plants = []
    for p in plants:
        pid = p["id"]
        pct = metrics.get(f"{pid}_pct")
        if pct is not None and metrics.get(f"{pid}_is_dry"):
            dry_plants.append(pid)

    vpd = metrics.get("vpd")
    if dry_plants:
        concerns.append(f"dry:{','.join(dry_plants)}")
    if vpd is not None and vpd >= 3.0:
        concerns.append("high-vpd")

    if dry_plants and vpd is not None and vpd >= 3.0:
        hypothesis = f"Plants {', '.join(dry_plants)} are under dry-down pressure with elevated VPD."
    elif dry_plants:
        hypothesis = f"Dry-down detected in {', '.join(dry_plants)}; moisture needs follow-up."
    elif vpd is not None and vpd >= 3.0:
        hypothesis = "Soil moisture is adequate, but atmospheric demand remains high."
    else:
        hypothesis = "Telemetry stable; no immediate stress signal."

    return {
        "last_hypothesis": hypothesis,
        "active_concerns": concerns
    }

def find_active_arduino_port():
    """Scans for a port without opening it (to prevent DTR resets)."""
    STABLE_PORT = "/dev/cu.usbmodem1201"
    if os.path.exists(STABLE_PORT):
        print(f"Warden: Stable port {STABLE_PORT} found natively.")
        return STABLE_PORT

    all_p = list(serial.tools.list_ports.comports())
    keywords = ["usbmodem", "usbserial", "arduino", "ch340", "cp210x", "ftdi"]
    for p in all_p:
        if any(k in p.device.lower() or k in p.description.lower() for k in keywords):
            return p.device

    print("Warden: No candidate ports found.")
    return None

def capture_data():
    port = find_active_arduino_port()
    if not port: return None
    
    try:
        # Timeout 10s safely outlasts the 5.0s hardware loop
        ser = serial.Serial(port, 9600, timeout=10)
        time.sleep(3.1) # BME680 Boot Protocol: 3.0s settle delay (SILICA v3.3)
        ser.reset_input_buffer()
        
        # Read up to 3 times to find a complete loop packet without discarding
        for _ in range(3):
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if "|" in line:
                parts = line.split("|")
                if len(parts) >= 8:
                    data = {
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "temp": float(parts[0]), 
                        "hum": float(parts[1]), 
                        "light": int(parts[2]),
                        "p1": int(parts[3]), # A0
                        "p2": int(parts[5]), # A3 (formerly A5)
                        "p3": int(parts[4]), # A2
                        "press": float(parts[6]),
                        "gas": float(parts[7]),
                        "db": capture_volume() or 0.0
                    }
                    
                    # Garbage Detection Logic (BME680 Saturation Signature or Dead Bus)
                    if data["press"] == 652.01 and data["hum"] == 100.0:
                        print("Warden: REJECTING DATA: HARDWARE INTERFERENCE DETECTED (BME680 Saturation 652/100).")
                        ser.close()
                        return None
                    elif data["temp"] == 0.0 and data["hum"] == 0.0 and data["press"] == 0.0:
                        print("Warden: REJECTING DATA: BME680 I2C BUS DEAD (Reading absolute 0s).")
                        ser.close()
                        return None
                    
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

def save_snapshot(raw, metrics, plants, state):
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

    vision_stack = get_temporal_vision_stack()
    vision_observation = load_vision_observation()
    snapshot = {
        "timestamp": datetime.now().isoformat(), 
        "sensors": raw or {}, 
        "moisture_analysis": {}, 
        "environment": {"vpd_kpa": metrics.get("vpd") if metrics else None}, 
        "intelligence": {
            "hypothesis": state.get("last_hypothesis"),
            "active_concerns": state.get("active_concerns", []),
            "temporal_stack": vision_stack,
            "vision_observation": vision_observation,
            "recent_visual_ledger": []
        }
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
    save_warden_state(state)
    print(f"Warden: Snapshot saved to {SNAPSHOT_PATH}")

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
        ser = serial.Serial(port, 9600, timeout=10)
        time.sleep(3.1) # BME680 Boot Protocol: 3.0s settle delay (SILICA v3.3)
        ser.reset_input_buffer()
        
        # Wait up to 3 cycles (15s) for a valid response
        for _ in range(3):
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if "|" in line:
                parts = line.split("|")
                if len(parts) >= 8:
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
    state = load_warden_state()
    
    # Antifragile Hardware Reset check
    if state.get("consecutive_drops", 0) >= 3:
        target_port = find_active_arduino_port()
        if target_port:
            execute_hardware_reset(target_port)

    raw = capture_data()
    metrics = compute_metrics(raw, plants)
    
    # Update drops state
    if raw is None:
        state["consecutive_drops"] = state.get("consecutive_drops", 0) + 1
    else:
        state["consecutive_drops"] = 0

    state_update = derive_hypothesis(raw, metrics, plants)
    state.update(state_update)
    save_snapshot(raw, metrics, plants, state)
    print("Warden: Run complete.")
