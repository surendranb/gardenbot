#!/usr/bin/env python3
import os
import json
import pandas as pd
from datetime import datetime

# --- Configuration ---
BASE_DIR = "/Users/surendran/.openclaw/workspace/gardenbot"
TELEMETRY_PATH = os.path.join(BASE_DIR, "data/telemetry.csv")
METRICS_PATH = os.path.join(BASE_DIR, "data/metrics.csv")
WEATHER_PATH = os.path.join(BASE_DIR, "data/weather_context.json")
MANIFEST_PATH = os.path.join(BASE_DIR, "GARDEN_MANIFEST.md")
OUTPUT_PATH = os.path.join(BASE_DIR, "data/observer_context.md")

def load_tail_df(path, n=6):
    try:
        if not os.path.exists(path): return None
        return pd.read_csv(path).tail(n)
    except: return None

def load_weather():
    try:
        if not os.path.exists(WEATHER_PATH): return {}
        with open(WEATHER_PATH, 'r') as f: return json.load(f)
    except: return {}

def load_world_model():
    """Extracts Section 6 from GARDEN_MANIFEST.md"""
    try:
        if not os.path.exists(MANIFEST_PATH): return "No manifest found."
        with open(MANIFEST_PATH, 'r') as f:
            content = f.read()
            if "## 6. WORLD MODEL" in content:
                return content.split("## 6. WORLD MODEL")[1].strip()
        return "World Model section not found in manifest."
    except Exception as e: return f"Error reading manifest: {e}"

def load_ledger(path, n=3):
    try:
        if not os.path.exists(path): return "No ledger file found."
        with open(path, 'r') as f:
            content = f.read()
            entries = content.split("## ")
            valid_entries = [e.strip() for e in entries if e.strip()]
            return "\n\n---\n\n".join([f"## {e}" for e in valid_entries[-n:]])
    except: return "Error reading ledger."

def synthesize_facts(telemetry, metrics, weather):
    """Generates high-level semantic observations from raw data."""
    facts = []
    current_hour = datetime.now().hour
    
    if metrics is not None and not metrics.empty:
        # 1. VPD Analysis & Transpiration Pressure
        current_vpd = metrics.iloc[-1].get('vpd', 0)
        if current_vpd > 3.0: vpd_state = "EXTREME (Critical Stress)"
        elif current_vpd > 2.0: vpd_state = "HIGH (Transpiration heavy)"
        elif current_vpd > 1.0: vpd_state = "MODERATE (Healthy)"
        else: vpd_state = "LOW (Stagnant/Mist)"
        facts.append(f"- **VPD State**: {vpd_state} at {current_vpd} kPa. Fans are likely scouring leaf boundary layers.")

        # 2. Moisture Trend / Spikes
        if len(metrics) > 1:
            for p in ['p1', 'p2', 'p3']:
                col = f"{p}_pct"
                if col in metrics.columns:
                    diff = metrics.iloc[-1][col] - metrics.iloc[-2][col]
                    if diff > 5:
                        facts.append(f"- **Care Event**: Sudden moisture spike in {p} (+{round(diff,1)}%). Likely misting or human watering.")
                    elif diff < -2:
                        facts.append(f"- **Dry-down**: {p} is drying at {abs(round(diff,1))}% per interval. High metabolic activity.")

    # 3. Micro-Climate Inferences (SILICA Logic)
    if telemetry is not None and not telemetry.empty:
        curr = telemetry.iloc[-1]
        prev = telemetry.iloc[-2] if len(telemetry) > 1 else curr
        
        # Human Presence Inference (Based on Fan S Logic)
        if 9 <= current_hour <= 23:
            facts.append("- **Human Presence**: HIGH. Fan S (South) is active; human-gated air exchange is the current baseline.")
        
        # AC Pulse Detection
        if (curr['hum'] < prev['hum'] - 3) and (curr['temp'] < prev['temp']):
            facts.append("- **AC Pulse**: Rapid humidity drop + temperature cooling detected. AC is active; monitor p1 for VPD shock.")
            
        # Thermal Peak (12:00-15:00)
        if 12 <= current_hour <= 15:
            facts.append("- **Thermal Gain**: Ceiling terrace is absorbing peak solar radiation. Internal temp rise expected.")

    # 4. Growth Pulse Directive
    if current_hour == 6:
        facts.append("- **DIRECTIVE: Growth Pulse**: Conduct mm-scale analysis of p3 and p2 using the White Rabbit (50mm) anchor.")

    if not facts: return "No significant anomalies or trends detected in the current window."
    return "\n".join(facts)

def main():
    print("Preparing Project SILICA Observer Context...")
    
    t_df = load_tail_df(TELEMETRY_PATH, 12)
    m_df = load_tail_df(METRICS_PATH, 12)
    weather_json = load_weather()
    world_model = load_world_model()
    ledger = load_ledger(os.path.join(BASE_DIR, "logs/vision_ledger.md"))
    facts = synthesize_facts(t_df, m_df, weather_json)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    content = f"""# 📝 Project SILICA: Garden Observer Context
**Generated:** {timestamp}

## 🏛️ 1. WORLD MODEL CONSTRAINTS (The Indoor Truth)
{world_model}

## 🧠 2. SEMANTIC FACT SYNTHESIS (The Warden's Logic)
{facts}

## 🌡️ 3. RECENT TELEMETRY (Verifier Data)
```csv
{t_df.to_csv(index=False) if t_df is not None else "No telemetry."}
```

## 📊 4. COMPUTED METRICS (Verifier Data)
```csv
{m_df.to_csv(index=False) if m_df is not None else "No metrics."}
```

## 🌤️ 5. WEATHER FORECAST (Macro-Context)
```json
{json.dumps(weather_json, indent=2)}
```

## 📖 6. PREVIOUS LEDGER ENTRIES (Last 3)
{ledger}

## ℹ️ FINAL INSTRUCTIONS TO OBSERVER
- **World Awareness**: Use Section 1 to interpret Section 2 & 3. Do not assume sensors are drifting if they diverge from Section 5.
- **Microclimate Priority**: Periodic AC (26°C) and Fans define the physical state.
- **Actionable Insight**: Provide a hypothesis for any "Care Detected" vs. "Dry-down" events.
"""
    
    with open(OUTPUT_PATH, 'w') as f: f.write(content)
    print(f"Context saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()