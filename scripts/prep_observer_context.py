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
VISION_OBSERVATION_PATH = os.path.join(BASE_DIR, "data/vision_observation.json")

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

def load_vision_observation():
    try:
        if not os.path.exists(VISION_OBSERVATION_PATH):
            return {}
        with open(VISION_OBSERVATION_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e)}

def synthesize_facts(telemetry, metrics, weather):
    """Generates high-level semantic observations from raw data (SILICA 2.0)."""
    facts = []
    current_hour = datetime.now().hour
    
    if metrics is not None and len(metrics) >= 6:
        # 1. VPD Analysis & Transpiration Pressure (Slope Calculation)
        recent_vpd = metrics.tail(6)['vpd']
        vpd_slope = round(recent_vpd.iloc[-1] - recent_vpd.iloc[0], 3)
        current_vpd = recent_vpd.iloc[-1]
        
        if current_vpd > 3.0: vpd_state = "EXTREME (Critical Stress)"
        elif current_vpd > 2.0: vpd_state = "HIGH (Transpiration heavy)"
        elif current_vpd > 1.0: vpd_state = "MODERATE (Healthy)"
        else: vpd_state = "LOW (Stagnant/Mist)"
        
        slope_desc = "Rising" if vpd_slope > 0.1 else "Falling" if vpd_slope < -0.1 else "Stable"
        facts.append(f"- **VPD State**: {vpd_state} at {current_vpd} kPa ({slope_desc} trend: {vpd_slope}).")

        # 2. Moisture Velocity Analysis
        for p in ['p1', 'p2', 'p3']:
            col = f"{p}_pct"
            if col in metrics.columns:
                m_series = metrics.tail(6)[col]
                m_velocity = round(m_series.iloc[-1] - m_series.iloc[0], 1)
                
                if m_velocity > 5:
                    facts.append(f"- **Care Event**: {p} is rehydrating (+{m_velocity}%). Action confirmed.")
                elif m_velocity < -2:
                    facts.append(f"- **Dry-down**: {p} moisture velocity is -{abs(m_velocity)}% per window. Metabolic activity is active.")
                else:
                    facts.append(f"- **Hydration Stagnancy**: {p} is flat (Δ{m_velocity}%). Check for root-stasis or sensor drift.")

    # 3. Micro-Climate Inferences (The Indoor Truth)
    if telemetry is not None and not telemetry.empty:
        curr = telemetry.iloc[-1]
        prev = telemetry.iloc[-2] if len(telemetry) > 1 else curr
        
        # Human/AC Synergy
        if (curr['hum'] < prev['hum'] - 3) and (curr['temp'] < prev['temp']):
            facts.append("- **AC Pulse**: Clamped thermal floor (26°C) detected via humidity crash. VPD shock in progress.")
        
        if 9 <= current_hour <= 23:
            facts.append("- **Human Occupancy**: HIGH. Fan S (South) is active; localized air exchange is manual.")

    # 4. Growth Pulse
    if current_hour == 6:
        facts.append("- **DIRECTIVE: Growth Pulse**: Conduct mm-scale analysis of p3/p2 using the White Rabbit anchor.")

    return "\n".join(facts) if facts else "No significant anomalies detected."

def main():
    print("Preparing Project SILICA Observer Context...")
    
    t_df = load_tail_df(TELEMETRY_PATH, 12)
    m_df = load_tail_df(METRICS_PATH, 12)
    weather_json = load_weather()
    world_model = load_world_model()
    ledger = load_ledger(os.path.join(BASE_DIR, "logs/vision_ledger.md"))
    vision_observation = load_vision_observation()
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

## 🎥 7. VISION OBSERVATION (Structured Visual Evidence)
```json
{json.dumps(vision_observation, indent=2)}
```

## ℹ️ FINAL INSTRUCTIONS TO OBSERVER
- **World Awareness**: Use Section 1 to interpret Section 2 & 3. Do not assume sensors are drifting if they diverge from Section 5.
- **Microclimate Priority**: Periodic AC (26°C) and Fans define the physical state.
- **Actionable Insight**: Provide a hypothesis for any "Care Detected" vs. "Dry-down" events.
- **Vision Priority**: Use Section 7 as the structured visual ground truth for current appearance and temporal changes.
"""
    
    with open(OUTPUT_PATH, 'w') as f: f.write(content)
    print(f"Context saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
