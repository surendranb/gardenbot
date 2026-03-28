#!/usr/bin/env python3
import json
import requests
import os
import sys
import csv
from datetime import datetime

# --- Configuration ---
CONFIG_PATH = os.path.expanduser("~/.config/openweathermap/credentials.json")
BASE_DIR = "/Users/surendran/.openclaw/workspace/gardenbot"
JSON_OUTPUT_PATH = os.path.join(BASE_DIR, "data/weather_context.json")
CSV_OUTPUT_PATH = os.path.join(BASE_DIR, "data/weather.csv")

def fetch_weather():
    try:
        if not os.path.exists(CONFIG_PATH):
            print(f"Error: Config not found at {CONFIG_PATH}")
            return

        with open(CONFIG_PATH, 'r') as f:
            creds = json.load(f)
        
        api_key = creds.get("api_key")
        lat = creds.get("lat")
        lon = creds.get("lon")
        
        if not api_key:
            print("Error: OWM API Key missing.")
            return
            
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        current = data.get("current", {})
        hourly = data.get("hourly", [])[:4]
        
        rain_expected = False
        max_pop = 0 
        for hour in hourly:
            pop = hour.get("pop", 0)
            if pop > max_pop: max_pop = pop
            if pop > 0.3: rain_expected = True
        
        # 1. Prepare JSON (Legacy/Full Context)
        context = {
            "timestamp": datetime.fromtimestamp(current.get("dt", 0)).strftime("%Y-%m-%d %H:%M:%S"),
            "main": {
                "temp": current.get("temp"),
                "humidity": current.get("humidity"),
                "pressure": current.get("pressure")
            },
            "weather": current.get("weather", [{}])[0] if current.get("weather") else {},
            "forecast": {
                "rain_expected": rain_expected,
                "max_pop": max_pop
            }
        }
        
        os.makedirs(os.path.dirname(JSON_OUTPUT_PATH), exist_ok=True)
        with open(JSON_OUTPUT_PATH, 'w') as f:
            json.dump(context, f, indent=2)

        # 2. Prepare CSV Row (Historical Tracking)
        row = {
            "timestamp": context["timestamp"],
            "temp": current.get("temp"),
            "humidity": current.get("humidity"),
            "pressure": current.get("pressure"),
            "pop": max_pop,
            "description": context["weather"].get("description", "clear")
        }

        file_exists = os.path.isfile(CSV_OUTPUT_PATH)
        with open(CSV_OUTPUT_PATH, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=row.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(row)
            
        print(f"Weather context saved to {JSON_OUTPUT_PATH} and {CSV_OUTPUT_PATH}")
        
    except Exception as e:
        print(f"Error fetching weather: {e}", file=sys.stderr)

if __name__ == "__main__":
    fetch_weather()