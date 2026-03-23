#!/usr/bin/env python3
import os
import json
import pandas as pd
from datetime import datetime

# --- Configuration ---
BASE_DIR = "/Users/surendran/.openclaw/workspace/gardenbot"
TELEMETRY_PATH = os.path.join(BASE_DIR, "docs/data/telemetry.csv")
METRICS_PATH = os.path.join(BASE_DIR, "docs/data/metrics.csv")
WEATHER_PATH = os.path.join(BASE_DIR, "docs/data/weather_context.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "docs/data/observer_context.md")

def load_tail(path, n=12):
    try:
        if not os.path.exists(path): return "No data file found."
        df = pd.read_csv(path).tail(n)
        return df.to_csv(index=False)
    except Exception as e: return f"Error reading {path}: {e}"

def load_weather():
    try:
        if not os.path.exists(WEATHER_PATH): return "No weather data."
        with open(WEATHER_PATH, 'r') as f: return json.dumps(json.load(f), indent=2)
    except Exception as e: return f"Error reading weather: {e}"

def main():
    print("Preparing Observer Context...")
    
    telemetry = load_tail(TELEMETRY_PATH)
    metrics = load_tail(METRICS_PATH)
    weather = load_weather()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    content = f"""# 📝 Garden Observer Context
**Generated:** {timestamp}

## 1. 🌡️ Recent Telemetry (Last 12 Readings)
```csv
{telemetry}
```

## 2. 📊 Computed Metrics (Last 12 Calculations)
```csv
{metrics}
```

## 3. 🌤️ Weather Forecast
```json
{weather}
```

## 4. ℹ️ Note to Observer
- **Visuals supersede sensors**: Cross-reference CSV data with `docs/media/latest.jpg`.
- **Primary Targets**: p1 (String of Nickels), p2 (Mint), p3 (Pothos), p4 (Silver Guest Alpha).
- **Physical Constants**: White Rabbit figurine is exactly **50 mm**.
- **Special Protocols**: At 06:00 AM, refer to GARDEN_MANIFEST.md for Growth Analysis instructions.
"""
    
    with open(OUTPUT_PATH, 'w') as f: f.write(content)
    print(f"Context saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()