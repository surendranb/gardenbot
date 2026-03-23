# 📝 Garden Observer Context
**Generated:** 2026-03-23 14:58:01

## 1. 🌡️ Recent Telemetry (Last 12 Readings)
```csv
timestamp,temp,hum,light,p1,p2,p3
2026-03-23 05:55:20,30.0,20.0,888,869.0,357.0,274.0
2026-03-23 06:26:03,30.0,19.0,878,871.0,360.0,271.0
2026-03-23 06:55:15,31.0,19.0,788,881.0,360.0,268.0
2026-03-23 07:55:50,31.0,19.0,726,872.0,255.0,367.0
2026-03-23 08:25:45,31.0,19.0,704,877.0,249.0,375.0
2026-03-23 11:56:08,31.0,21.0,702,386.0,160.0,278.0
2026-03-23 13:22:46,32.0,21.0,753,379.0,196.0,323.0
2026-03-23 13:25:28,32.0,21.0,754,381.0,211.0,322.0
2026-03-23 13:55:28,32.0,18.0,752,487.0,202.0,326.0
2026-03-23 14:25:29,32.0,16.0,764,477.0,249.0,325.0
2026-03-23 14:40:15,31.0,15.0,780,452.0,240.0,325.0
2026-03-23 14:55:28,32.0,15.0,788,435.0,246.0,325.0

```

## 2. 📊 Computed Metrics (Last 12 Calculations)
```csv
timestamp,vpd,p1_pct,p1_slope,p2_pct,p2_slope,p3_pct,p3_slope,p4_pct,p4_slope,p5_pct,p5_slope,p6_pct,p6_slope,p1_is_dry,p2_is_dry,p3_is_dry
2026-03-23 08:25:45,3.639,11.2,True,91.8,False,70.8,False,,,,,,,,,
2026-03-23 08:25:45,3.639,11.2,True,91.8,False,70.8,False,,,,,,,,,
2026-03-23 08:25:45,3.639,11.2,True,91.8,False,70.8,False,,,,,,,,,
2026-03-23 11:56:08,3.549,86.8,False,100.0,False,87.0,False,,,,,,,,,
2026-03-23 11:56:08,3.549,86.8,False,100.0,False,87.0,False,,,,,,,,,
2026-03-23 11:56:08,3.549,86.8,False,100.0,False,87.0,False,,,,,,,,,
2026-03-23 13:22:46,3.756,100.0,False,100.0,False,100.0,False,,,,,,,,,
2026-03-23 13:25:28,3.756,100.0,False,97.4,False,100.0,False,,,,,,,,,
2026-03-23 13:55:28,3.899,73.6,False,100.0,False,99.1,False,,,,,,,,,
2026-03-23 14:25:29,3.994,76.7,,81.1,,99.4,,,,,,,,False,False,False
2026-03-23 14:40:15,3.819,84.4,,85.0,,99.4,,,,,,,,False,False,False
2026-03-23 14:55:28,4.041,89.6,,82.4,,99.4,,,,,,,,False,False,False

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
