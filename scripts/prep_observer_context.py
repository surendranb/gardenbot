#!/usr/bin/env python3
import os
import json
import pandas as pd
import numpy as np
import subprocess
import re
import argparse
from datetime import datetime, timedelta

# --- Configuration ---
BASE_DIR = "/Users/surendran/.openclaw/workspace/gardenbot"
TELEMETRY_PATH = os.path.join(BASE_DIR, "data/telemetry.csv")
METRICS_PATH = os.path.join(BASE_DIR, "data/metrics.csv")
WEATHER_PATH = os.path.join(BASE_DIR, "data/weather_context.json")
VISION_OBSERVATION_PATH = os.path.join(BASE_DIR, "data/vision_observation.json")

VISION_HISTORY_PATH = os.path.join(BASE_DIR, "logs/vision_history.jsonl")
HUMAN_ACTIONS_PATH = os.path.join(BASE_DIR, "data/human_actions.jsonl")
VISION_LEDGER_MD_PATH = os.path.join(BASE_DIR, "logs/vision_ledger.md")
VISION_CONTEXT_PATH = os.path.join(BASE_DIR, "data/vision_context.json")
CALIBRATION_PATH = os.path.join(BASE_DIR, "logs/agent_calibration.md")
OUTPUT_PATH = os.path.join(BASE_DIR, "data/observer_context.md")

# Acoustic Hardware Signatures (Deterministic DB Bins)
MIC_INDEX = "2"
SIG_LEVEL_1 = -35.0  # Transition to 1 Fan
SIG_LEVEL_2 = -27.0  # Transition to 2 Fans

def load_df(path):
    try:
        if not os.path.exists(path): return None
        return pd.read_csv(path)
    except: return None

def load_json(path):
    try:
        if not os.path.exists(path): return {}
        with open(path, 'r') as f: return json.load(f)
    except: return {}

def get_acoustic_fan_status(db_val):
    """Determines fan state based on deterministic hardware dB clusters."""
    if db_val is None or db_val == 0.0: return "UNKNOWN", "N/A"
    
    if db_val < SIG_LEVEL_1:
        return "OFF (Silent)", f"{db_val} dB (Baseline Floor)"
    elif db_val < SIG_LEVEL_2:
        return "ON (Level 1: Single)", f"{db_val} dB (Mid-range Convection)"
    else:
        return "ON (Level 2: High/Dual)", f"{db_val} dB (Maximum Convection)"

def get_world_model_ledger():
    """Extracts the permanent world model from the SILICA master ledger."""
    path = os.path.join(BASE_DIR, "PROJECT_SILICA.md")
    if not os.path.exists(path): return "Error: Project SILICA ledger missing."
    try:
        with open(path, 'r') as f:
            content = f.read()
            # Extract everything between 'THE WORLD MODEL' and the next header
            # Uses a lookahead to stop exactly before the next section begins
            pattern = r"## 2\. THE WORLD MODEL(.*?)(?=\n##|$)"
            match = re.search(pattern, content, re.DOTALL)
            if match:
                return f"## 2. THE WORLD MODEL\n" + match.group(1).strip()
            return "World model section not found in SILICA ledger."

    except Exception as e:
        return f"Error reading ledger: {str(e)}"

def get_dynamic_world_model(t_df):
    now = datetime.now()
    hour = now.hour
    occupancy = "HIGH" if 9 <= hour <= 23 else "LOW"
    
    db_val = None
    if t_df is not None and not t_df.empty and 'db' in t_df.columns:
        db_val = t_df['db'].iloc[-1]
    
    fan_status, empirical_proof = get_acoustic_fan_status(db_val)
    
    # ... BME680 Logic ...
    air_quality_inference = "UNKNOWN (Insufficient Data)"
    if t_df is not None and not t_df.empty:
        try:
            t_df['timestamp'] = pd.to_datetime(t_df['timestamp'])
            recent = t_df[t_df['timestamp'] > (now - timedelta(hours=4))]
            if not recent.empty and 'gas' in recent.columns:
                curr_gas = recent['gas'].iloc[-1]
                gas_avg = recent['gas'].mean()
                delta = curr_gas - gas_avg
                
                is_fan_on = "ON" in fan_status
                if is_fan_on:
                    if delta > 0.5: air_quality_inference = f"OPTIMAL - Fans clearing VOCs (+{round(delta, 2)} kOhms)"
                    elif delta < -0.5: air_quality_inference = f"CRITICAL - VOCs failing to clear. Delta: {round(delta, 2)} kOhms"
                    else: air_quality_inference = f"EFFICIENT - VOC baseline maintained. Delta: {round(delta, 2)} kOhms"
                else:
                    if delta < -1.0: air_quality_inference = f"STAGNANT - VOCs accumulating ({round(delta, 2)} kOhms). ACTIVATE FANS."
                    else: air_quality_inference = "STABLE - Passive clearing sufficient."
        except: pass

    biome_mode = 'ACTIVE (Photosynthetic/Transpiration heavy)' if "ON" in fan_status else 'REST (Night/Stagnant Recovery)'
    
    # Permanent Context (from Ledger)
    ledger_context = get_world_model_ledger()

    res = f"### 🎭 1A. THE PERMANENT MODEL (SILICA Ledger)\n{ledger_context}\n\n"
    res += f"### 🕒 1B. THE DYNAMIC SNAPSHOT\n"
    res += f"- **TIME OF AUDIT**: {now.strftime('%H:%M')}\n"
    res += f"- **HUMAN OCCUPANCY**: {occupancy}\n"
    res += f"- **FANS STATUS (Acoustic Registry)**: {fan_status}\n"
    res += f"- **EMPIRICAL PROOF**: {empirical_proof}\n"
    res += f"- **BIOME STATE**: {biome_mode}\n"
    return res


def get_human_context():
    actions = []
    try:
        if os.path.exists(HUMAN_ACTIONS_PATH):
            with open(HUMAN_ACTIONS_PATH, "r") as f:
                for line in f:
                    try: actions.append(json.loads(line.strip()))
                    except: continue
    except: pass
    recent = actions[-5:]
    if not recent: return "No recent actions."
    res = ""
    for a in recent:
        ts = a.get('timestamp', 'Unknown')
        act = a.get('action', 'Unknown')
        note = a.get('note', '')
        status = a.get('status', 'applied')
        res += f"- **[{ts}]**: {act} -> {note} (Status: {status})\n"
    return res

def get_temporal_insights(n=3):
    insights = []
    try:
        if os.path.exists(VISION_LEDGER_MD_PATH):
            with open(VISION_LEDGER_MD_PATH, 'r') as f:
                content = f.read()
                entries = [e.strip() for e in content.split("## ") if e.strip()]
                for e in entries[-n:]:
                    lines = e.split("\n")
                    header = lines[0]
                    advice = [l for l in lines if "Advice:" in l or "Verdict:" in l or "Next Steps" in l]
                    insights.append(f"### Report: {header}\n" + "\n".join(advice[:3]))
    except: pass
    return "\n\n".join(insights) if insights else "No historical insights."

def get_agent_calibration():
    try:
        if os.path.exists(CALIBRATION_PATH):
            with open(CALIBRATION_PATH, 'r') as f:
                return f.read()
    except: pass
    return "No calibration data available."

def get_biological_deltas(m_df):
    if m_df is None or m_df.empty: return "No metric data."
    m_df['timestamp'] = pd.to_datetime(m_df['timestamp'])
    now = m_df['timestamp'].iloc[-1]
    
    def get_stats(window_hours):
        df = m_df[m_df['timestamp'] > (now - timedelta(hours=window_hours))]
        if df.empty: return None
        return {
            "vpd": round(df['vpd'].mean(), 3),
            "p1": round(df['p1_pct'].mean(), 1),
            "p2": round(df['p2_pct'].mean(), 1),
            "p3": round(df['p3_pct'].mean(), 1)
        }

    pulse = get_stats(4)
    day = get_stats(24)
    rhythm = get_stats(72)
    baseline_df = m_df[(m_df['timestamp'] > (now - timedelta(days=7, minutes=30))) & (m_df['timestamp'] <= (now - timedelta(days=7)))]
    
    facts = []
    if pulse and day and rhythm:
        facts.append(f"#### 🌡️ VPD WINDOWS\n- **4h Pulse**: {pulse['vpd']} kPa | **24h Cycle**: {day['vpd']} kPa | **72h Rhythm**: {rhythm['vpd']} kPa")
        facts.append("\n#### 💧 HYDRATION & GROWTH MARKERS")
        for p in ['p1', 'p2', 'p3']:
            curr, d_avg = pulse[p], day[p]
            b_text = ""
            if not baseline_df.empty:
                b_val = baseline_df[f"{p}_pct"].iloc[-1]
                b_delta = round(curr - b_val, 1)
                tag = '📈 GROWTH/WET' if b_delta > 5 else '📉 DECLINE/DRY' if b_delta < -10 else '⚖️ STABLE'
                b_text = f" | **7d Baseline Delta**: {b_delta}% ({tag})"
            facts.append(f"- **{p.upper()}**: {curr}% (Current) vs {d_avg}% (24h Avg){b_text}")
    else:
        facts.append("Insufficient data for windows.")
    return "\n".join(facts)

def export_vision_context():
    """Exports a lightweight JSON for the vision model to understand recent human/system state."""
    actions = []
    try:
        if os.path.exists(HUMAN_ACTIONS_PATH):
            with open(HUMAN_ACTIONS_PATH, "r") as f:
                for line in f:
                    try: actions.append(json.loads(line.strip()))
                    except: continue
    except: pass
    
    # Filter for last 24h
    now = datetime.now()
    recent_actions = []
    for a in actions:
        try:
            ts = pd.to_datetime(a.get('timestamp'))
            if (now - ts.to_pydatetime().replace(tzinfo=None)) < timedelta(hours=24):
                recent_actions.append(a)
        except: continue

    insights = get_temporal_insights(3).split("\n\n")
    
    payload = {
        "timestamp": now.isoformat(),
        "recent_human_actions": recent_actions[-3:],
        "last_recommendations": [i.strip() for i in insights if i.strip()]
    }
    
    with open(VISION_CONTEXT_PATH, 'w') as f:
        json.dump(payload, f, indent=2)
    print(f"Vision context exported to {VISION_CONTEXT_PATH}")

def main():
    parser = argparse.ArgumentParser(description="SILICA Context Synthesizer")
    parser.add_argument("--vision-only", action="store_true", help="Only export light context for vision model")
    args = parser.parse_args()

    if args.vision_only:
        export_vision_context()
        return

    print("Synthesizing SILICA v2.2 (Corrected Logic)...")
    t_df, m_df = load_df(TELEMETRY_PATH), load_df(METRICS_PATH)
    vision = load_json(VISION_OBSERVATION_PATH)
    
    dynamic_world = get_dynamic_world_model(t_df)
    human_actions = get_human_context()
    prior_insights = get_temporal_insights(3)
    calibration = get_agent_calibration()
    deltas = get_biological_deltas(m_df)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    content = "# 📝 SILICA v3.0: High-Fidelity Biological Context\n"
    content += f"**Generated:** {timestamp}\n\n"
    content += "## 🏛️ 1. IDENTITY & WORLD CONSTRAINTS\n"
    content += f"{dynamic_world}\n\n"
    content += "## 🧠 2. AGENT CALIBRATION & LEARNED HEURISTICS\n"
    content += f"{calibration}\n\n"
    content += "## 📖 3. PRIOR INSIGHTS & RECOMMENDATIONS\n"
    content += f"{prior_insights}\n\n"
    content += "## 🛠️ 3. HUMAN FEEDBACK LOOP (Recent Actions)\n"
    content += f"{human_actions}\n\n"
    content += "## 🧠 4. BIOLOGICAL TEMPO (Tiered Telemetry)\n"
    content += f"{deltas}\n\n"
    content += "## 🎥 5. VISUAL GROUND-TRUTH (Latest Gemini Audit)\n"
    content += "```json\n"
    content += json.dumps(vision.get('vision_report', {}), indent=2)
    content += "\n```\n\n"
    content += "## 🌡️ 6. RAW TELEMETRY (4h Window)\n"
    content += "```csv\n"
    content += t_df.tail(8).to_csv(index=False) if t_df is not None else "No telemetry."
    content += "```\n\n"
    content += "## ℹ️ FINAL CONTEXT CHECK\n"
    content += "- **Acoustic Truth**: The Fan Status in Section 1 is EMPIRICAL. Use it to judge transpiration pressure.\n"
    content += "- **Action Tracking**: Reconcile Section 3 with Section 4 to see if care is working.\n"
    content += "- **Growth Velocity**: If delta in Section 4 is negative but Vision in Section 5 looks good, interpret as 'Peak Metabolism'.\n"

    with open(OUTPUT_PATH, 'w') as f: f.write(content)
    print(f"Context saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()