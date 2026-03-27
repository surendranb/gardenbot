# 📝 Garden Observer Context
**Generated:** 2026-03-26 15:58:01

## 1. 🌡️ Recent Telemetry (Last 12 Readings)
```csv
timestamp,temp,hum,light,p1,p2,p3
2026-03-26 09:29:29,31.0,37.0,572,498.0,215.0,454.0
2026-03-26 09:55:28,31.0,36.0,542,502.0,203.0,447.0
2026-03-26 10:25:30,31.0,37.0,554,477.0,225.0,445.0
2026-03-26 10:55:28,32.0,36.0,535,467.0,196.0,435.0
2026-03-26 10:55:56,32.0,36.0,536,466.0,204.0,435.0
2026-03-26 11:55:28,32.0,34.0,534,488.0,195.0,432.0
2026-03-26 12:25:28,32.0,34.0,543,481.0,205.0,435.0
2026-03-26 12:55:28,32.0,34.0,544,476.0,192.0,434.0
2026-03-26 13:25:28,32.0,34.0,550,479.0,199.0,434.0
2026-03-26 13:55:28,32.0,34.0,565,490.0,212.0,443.0
2026-03-26 14:25:29,32.0,34.0,570,484.0,210.0,439.0
2026-03-26 15:55:28,32.0,33.0,740,472.0,177.0,438.0

```

## 2. 🌬️ Atmospheric Pull (Indoor vs. Outdoor)
**Indoor VPD**: 3.186 kPa | **Outdoor VPD**: 0.553 kPa
**Pressure Delta**: -2.633 kPa
🛡️ **INDOOR REFUGE**: Outdoor air is much more humid than indoors. Evaporative stress is low.

## 3. 📊 Computed Metrics (Last 12 Calculations)
```csv
timestamp,vpd,p1_pct,p1_slope,p2_pct,p2_slope,p3_pct,p3_slope,p4_pct,p4_slope,p5_pct,p5_slope,p6_pct,p6_slope,p1_is_dry,p2_is_dry,p3_is_dry
2026-03-26 09:29:29,2.83,70.2,1.59,95.7,-7.58,62.7,-3.0,,,,,,,False,False,False
2026-03-26 09:55:28,2.875,69.0,-2.77,100.0,9.93,64.7,4.62,,,,,,,False,False,False
2026-03-26 10:25:30,2.83,76.7,15.38,91.4,-17.18,65.2,1.0,,,,,,,False,False,False
2026-03-26 10:55:28,3.043,79.8,6.21,100.0,17.22,68.1,5.81,,,,,,,False,False,False
2026-03-26 10:55:56,3.043,80.1,0.0,100.0,0.0,68.1,0.0,,,,,,,False,False,False
2026-03-26 11:55:28,3.138,73.3,-6.85,100.0,0.0,68.9,0.81,,,,,,,False,False,False
2026-03-26 12:25:28,3.138,75.5,4.4,100.0,0.0,68.1,-1.6,,,,,,,False,False,False
2026-03-26 12:55:28,3.138,77.0,3.0,100.0,0.0,68.4,0.6,,,,,,,False,False,False
2026-03-26 13:25:28,3.138,76.1,-1.8,100.0,0.0,68.4,0.0,,,,,,,False,False,False
2026-03-26 13:55:28,3.138,72.7,-6.8,97.0,-6.0,65.8,-5.2,,,,,,,False,False,False
2026-03-26 14:25:29,3.138,74.5,3.6,97.9,1.8,67.0,2.4,,,,,,,False,False,False
2026-03-26 15:55:28,3.186,78.2,2.47,100.0,1.4,67.2,0.13,,,,,,,False,False,False

```

## 4. 🌤️ Weather Forecast
```json
{
  "timestamp": 1774483226,
  "main": {
    "temp": 26.47,
    "feels_like": 26.47,
    "temp_min": null,
    "temp_max": null,
    "pressure": 1010,
    "humidity": 84,
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
    "sunrise": 1774485556,
    "sunset": 1774529398
  },
  "name": "Asia/Kolkata",
  "forecast": {
    "rain_expected": false,
    "max_probability_of_precipitation": 0,
    "hourly_forecast": [
      {
        "time": 1774483200,
        "temp": 26.47,
        "humidity": 84,
        "pop": 0,
        "weather": {
          "id": 801,
          "main": "Clouds",
          "description": "few clouds",
          "icon": "02n"
        }
      },
      {
        "time": 1774486800,
        "temp": 26.18,
        "humidity": 83,
        "pop": 0,
        "weather": {
          "id": 801,
          "main": "Clouds",
          "description": "few clouds",
          "icon": "02d"
        }
      },
      {
        "time": 1774490400,
        "temp": 26.3,
        "humidity": 80,
        "pop": 0,
        "weather": {
          "id": 801,
          "main": "Clouds",
          "description": "few clouds",
          "icon": "02d"
        }
      },
      {
        "time": 1774494000,
        "temp": 26.94,
        "humidity": 75,
        "pop": 0,
        "weather": {
          "id": 800,
          "main": "Clear",
          "description": "clear sky",
          "icon": "01d"
        }
      }
    ]
  }
}
```
[...]