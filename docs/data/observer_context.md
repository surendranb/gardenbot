# 📝 Garden Observer Context
**Generated:** 2026-03-23 15:26:52

## 1. 🌡️ Recent Telemetry (Last 12 Readings)
```csv
timestamp,temp,hum,light,p1,p2,p3
2026-03-23 14:55:28,32.0,15.0,788,435.0,246.0,325.0
2026-03-23 15:24:36,31.0,15.0,807,448.0,230.0,326.0
2026-03-23 15:25:28,32.0,15.0,801,442.0,230.0,326.0

```

## 2. 📊 Computed Metrics (Last 12 Calculations)
```csv
timestamp,vpd,p1_pct,p1_slope,p2_pct,p2_slope,p3_pct,p3_slope,p4_pct,p4_slope,p5_pct,p5_slope,p6_pct,p6_slope,p1_is_dry,p2_is_dry,p3_is_dry
2026-03-23 14:55:28,4.041,89.6,,82.4,,99.4,,,,,,,,False,False,False
2026-03-23 15:24:36,3.819,85.6,,89.3,,99.1,,,,,,,,False,False,False
2026-03-23 15:25:28,4.041,87.4,,89.3,,99.1,,,,,,,,False,False,False

```

## 3. 🌤️ Weather Forecast
```json
{
  "timestamp": 1774224007,
  "main": {
    "temp": 26.29,
    "feels_like": 26.29,
    "temp_min": null,
    "temp_max": null,
    "pressure": 1011,
    "humidity": 86,
    "sea_level": null,
    "grnd_level": null
  },
  "weather": {
    "id": 701,
    "main": "Mist",
    "description": "mist",
    "icon": "50n"
  },
  "wind": null,
  "sys": {
    "sunrise": 1774226479,
    "sunset": 1774270189
  },
  "name": "Asia/Kolkata",
  "forecast": {
    "rain_expected": false,
    "max_probability_of_precipitation": 0,
    "hourly_forecast": [
      {
        "time": 1774224000,
        "temp": 26.29,
        "humidity": 86,
        "pop": 0,
        "weather": {
          "id": 802,
          "main": "Clouds",
          "description": "scattered clouds",
          "icon": "03n"
        }
      },
      {
        "time": 1774227600,
        "temp": 26.17,
        "humidity": 84,
        "pop": 0,
        "weather": {
          "id": 802,
          "main": "Clouds",
          "description": "scattered clouds",
          "icon": "03d"
        }
      },
      {
        "time": 1774231200,
        "temp": 26.45,
        "humidity": 81,
        "pop": 0,
        "weather": {
          "id": 802,
          "main": "Clouds",
          "description": "scattered clouds",
          "icon": "03d"
        }
      },
      {
        "time": 1774234800,
        "temp": 27.2,
        "humidity": 75,
        "pop": 0,
        "weather": {
          "id": 801,
          "main": "Clouds",
          "description": "few clouds",
          "icon": "02d"
        }
      }
    ]
  }
}
```

## 4. ℹ️ Note to Observer
- **Visuals supersede sensors**: Cross-reference CSV data with `docs/media/latest.jpg`.
- **Primary Targets**: p1 (String of Nickels), p2 (Mint), p3 (Pothos), p4 (Silver Guest Alpha).
- **Physical Constants**: White Rabbit figurine is exactly **50 mm**.
- **Special Protocols**: At 06:00 AM, refer to GARDEN_MANIFEST.md for Growth Analysis instructions.
