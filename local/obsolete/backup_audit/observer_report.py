#!/usr/bin/env python3
import os
import json
import subprocess
from datetime import datetime
import pandas as pd

# --- Configuration ---
BASE_DIR = "/Users/surendran/.openclaw/workspace/gardenbot"
SNAPSHOT_PATH = os.path.join(BASE_DIR, "data/current_snapshot.json")
PLANTS_CONFIG = os.path.join(BASE_DIR, "config/plants.json")
CHANNEL = "C0AK6A4SJES" # #plantclaw

def load_json(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return {}

def run_observer():
    now = datetime.now()
    print(f"[{now.isoformat()}] Observer: Starting visual and data audit...")

    # 1. Load Latest Context
    snapshot = load_json(SNAPSHOT_PATH)
    plants = load_json(PLANTS_CONFIG)
    plants_map = {p["id"]: p for p in plants}
    
    if not snapshot:
        print("Observer Error: No snapshot available.")
        return

    # 2. Extract Key Metrics
    sensors = snapshot.get("sensors", {})
    moisture = snapshot.get("moisture_analysis", {})
    env = snapshot.get("environment", {})
    vpd = env.get("vpd_kpa", "N/A")
    
    # 3. Formulate the Report
    report = [
        f"🔭 *GARDEN OBSERVER REPORT* ({now.strftime('%H:%M')})",
        f"Environment: {sensors.get('temp', '??')}\u00b0C | {sensors.get('hum', '??')}% Hum | {sensors.get('light', '??')} Lux (VPD: {vpd} kPa)",
        "\n*Biometric Status*:"
    ]

    for pid, stats in moisture.items():
        if pid in ["p4", "p5", "p6"]: continue # Skip virtuals for brevity
        name = plants_map.get(pid, {}).get("name", pid)
        status = "🔴 DRY" if stats.get("is_dry") else "🟢 NOMINAL"
        report.append(f"• {name}: {status} ({stats.get('moisture_pct', '??')}%)")

    # 4. Intelligence Insight
    slopes = snapshot.get("intelligence", {}).get("slopes", {})
    insights = []
    for pid, data in slopes.items():
        if data.get("estimated_hours_to_dryout"):
            name = plants_map.get(pid, {}).get("name", pid)
            insights.append(f"{name} dryout in ~{data['estimated_hours_to_dryout']}h")
    
    if insights:
        report.append("\n*Predictive Insights*:")
        for ins in insights:
            report.append(f"• {ins}")

    # 5. Visual Check (Placeholder for Agent to fill in during live sessions)
    report.append("\n*Visual Check*: Camera snapshot updated. [Agent: Please perform visual audit of latest.jpg]")

    # 6. Send to Slack
    final_message = "\n".join(report)
    print("Observer: Dispatching report to Slack...")
    subprocess.run(["openclaw", "message", "send", "--target", CHANNEL, "--message", final_message], capture_output=True)

if __name__ == "__main__":
    run_observer()
