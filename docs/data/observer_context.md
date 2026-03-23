# 📝 Garden Observer Context
**Generated:** 2026-03-23 07:58:01

## 1. 🌡️ Recent Telemetry (Last 12 Readings)
```csv
timestamp,temp,hum,light,p1,p2,p3
2026-03-23 01:55:21,31.0,20.0,892,883.0,356.0,281.0
2026-03-23 02:25:26,31.0,19.0,897,901.0,354.0,283.0
2026-03-23 02:55:39,31.0,19.0,889,876.0,359.0,280.0
2026-03-23 03:25:16,31.0,20.0,890,879.0,356.0,278.0
2026-03-23 03:55:15,31.0,19.0,888,874.0,355.0,274.0
2026-03-23 04:25:20,31.0,19.0,888,877.0,356.0,274.0
2026-03-23 04:55:21,31.0,19.0,888,878.0,356.0,275.0
2026-03-23 05:25:27,31.0,19.0,888,879.0,356.0,275.0
2026-03-23 05:55:20,30.0,20.0,888,869.0,357.0,274.0
2026-03-23 06:26:03,30.0,19.0,878,871.0,360.0,271.0
2026-03-23 06:55:15,31.0,19.0,788,881.0,360.0,268.0
2026-03-23 07:55:50,31.0,19.0,726,872.0,255.0,367.0

```

## 2. 📊 Computed Metrics (Last 12 Calculations)
```csv
timestamp,vpd,p1_pct,p1_slope,p2_pct,p2_slope,p3_pct,p3_slope,p4_pct,p4_slope,p5_pct,p5_slope,p6_pct,p6_slope
2026-03-23 02:25:26,3.639,7.5,True,86.2,False,74.3,False,83.4,False,,,,
2026-03-23 02:55:39,3.639,11.4,True,86.7,False,73.5,False,84.0,False,,,,
2026-03-23 03:25:16,3.594,10.9,True,87.0,False,74.0,False,84.4,False,,,,
2026-03-23 03:55:15,3.639,11.7,True,87.7,False,74.2,False,85.2,False,,,,
2026-03-23 04:25:20,3.639,11.2,True,87.7,False,74.0,False,85.2,False,,,,
2026-03-23 04:55:21,3.639,11.1,True,87.5,False,74.0,False,85.0,False,,,,
2026-03-23 05:25:27,3.639,10.9,True,87.5,False,74.0,False,85.0,False,,,,
2026-03-23 05:55:20,3.394,12.5,True,87.7,False,73.8,False,85.2,False,,,,
2026-03-23 06:26:03,3.437,12.2,True,88.2,False,73.3,False,85.8,False,,,,
2026-03-23 06:55:15,3.639,10.6,True,88.7,False,73.3,False,86.4,False,,,,
2026-03-23 06:55:15,3.639,10.6,True,73.3,False,88.7,False,,,,,,
2026-03-23 07:55:50,3.639,12.0,True,90.8,False,72.2,False,,,,,,

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
