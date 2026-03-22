#!/usr/bin/env python3
import json
import requests
import os
import sys

# --- Configuration ---
CONFIG_PATH = os.path.expanduser("~/.config/openweathermap/credentials.json")
OUTPUT_PATH = "/Users/surendran/.openclaw/workspace/gardenbot/data/weather_context.json"

def fetch_weather():
    try:
        with open(CONFIG_PATH, 'r') as f:
            creds = json.load(f)
        
        api_key = creds.get("api_key")
        lat = creds.get("lat")
        lon = creds.get("lon")
        
        if not api_key:
            print("Error: OWM API Key missing.")
            return
            
        # Call OpenWeatherMap One Call API (v3.0) to get current + forecast data
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Extract current weather
        current = data.get("current", {})
        
        # Get forecast for next 12 hours (4 entries of 3-hour intervals)
        hourly = data.get("hourly", [])[:4]
        
        # Calculate if rain is expected in the next 12 hours
        rain_expected = False
        max_pop = 0  # Probability of precipitation
        for hour in hourly:
            pop = hour.get("pop", 0)  # Probability of precipitation
            if pop > max_pop:
                max_pop = pop
            if pop > 0.3:  # More than 30% chance of rain
                rain_expected = True
        
        # Structure the context for the agent
        context = {
            "timestamp": current.get("dt"),
            "main": {
                "temp": current.get("temp"),
                "feels_like": current.get("feels_like"),
                "temp_min": current.get("temp_min"),
                "temp_max": current.get("temp_max"),
                "pressure": current.get("pressure"),
                "humidity": current.get("humidity"),
                "sea_level": current.get("sea_level"),
                "grnd_level": current.get("grnd_level")
            },
            "weather": current.get("weather", [{}])[0] if current.get("weather") else {},
            "wind": current.get("wind"),
            "sys": {
                "sunrise": data.get("current", {}).get("sunrise", 0),
                "sunset": data.get("current", {}).get("sunset", 0)
            },
            "name": data.get("timezone", "Unknown"),
            # Forecast information
            "forecast": {
                "rain_expected": rain_expected,
                "max_probability_of_precipitation": max_pop,
                "hourly_forecast": [
                    {
                        "time": hour.get("dt"),
                        "temp": hour.get("temp"),
                        "humidity": hour.get("humidity"),
                        "pop": hour.get("pop", 0),
                        "weather": hour.get("weather", [{}])[0] if hour.get("weather") else {}
                    }
                    for hour in hourly
                ]
            }
        }
        
        with open(OUTPUT_PATH, 'w') as f:
            json.dump(context, f, indent=2)
            
        print(f"Weather context saved to {OUTPUT_PATH}")
        print(f"Rain expected in next 12h: {rain_expected} (max POP: {max_pop:.0%})")
        
    except Exception as e:
        print(f"Error fetching weather: {e}", file=sys.stderr)

if __name__ == "__main__":
    fetch_weather()