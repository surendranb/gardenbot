# 📝 Garden Observer Context
**Generated:** 2026-03-26 08:58:01

## 1. 🌡️ Recent Telemetry (Last 12 Readings)
```csv
timestamp,temp,hum,light,p1,p2,p3
2026-03-26 04:25:28,30.0,16.0,910,489.0,188.0,443.0
2026-03-26 04:55:34,30.0,16.0,910,497.0,211.0,443.0
2026-03-26 05:25:28,30.0,16.0,910,486.0,216.0,439.0
2026-03-26 05:55:34,30.0,16.0,909,480.0,208.0,441.0
2026-03-26 06:25:28,30.0,16.0,880,490.0,216.0,434.0
2026-03-26 06:55:28,30.0,16.0,806,488.0,213.0,438.0
2026-03-26 07:25:29,30.0,16.0,715,482.0,209.0,438.0
2026-03-26 07:46:40,30.0,16.0,670,487.0,216.0,447.0
2026-03-26 07:55:28,30.0,16.0,654,479.0,211.0,446.0
2026-03-26 08:25:28,30.0,38.0,604,505.0,211.0,453.0
2026-03-26 08:33:09,30.0,38.0,670,506.0,204.0,451.0
2026-03-26 08:55:28,31.0,37.0,599,501.0,204.0,448.0

```

## 2. 🌬️ Atmospheric Pull (Indoor vs. Outdoor)
**Indoor VPD**: 2.83 kPa | **Outdoor VPD**: 0.553 kPa
**Pressure Delta**: -2.277 kPa
🛡️ **INDOOR REFUGE**: Outdoor air is much more humid than indoors. Evaporative stress is low.

## 3. 📊 Computed Metrics (Last 12 Calculations)
```csv
timestamp,vpd,p1_pct,p1_slope,p2_pct,p2_slope,p3_pct,p3_slope,p4_pct,p4_slope,p5_pct,p5_slope,p6_pct,p6_slope,p1_is_dry,p2_is_dry,p3_is_dry
2026-03-26 04:25:28,3.564,73.0,,100.0,,65.8,,,,,,,,False,False,False
2026-03-26 04:55:34,3.564,70.6,,97.4,,65.8,,,,,,,,False,False,False
2026-03-26 05:25:28,3.564,73.9,,95.3,,67.0,,,,,,,,False,False,False
2026-03-26 05:55:34,3.564,75.8,,98.7,,66.4,,,,,,,,False,False,False
2026-03-26 06:25:28,3.564,72.7,,95.3,,68.4,,,,,,,,False,False,False
2026-03-26 06:55:28,3.564,73.3,,96.6,,67.2,,,,,,,,False,False,False
2026-03-26 07:25:29,3.564,75.2,,98.3,,67.2,,,,,,,,False,False,False
2026-03-26 07:46:40,3.564,73.6,,95.3,,64.7,,,,,,,,False,False,False
2026-03-26 07:55:28,3.564,76.1,,97.4,,65.0,,,,,,,,False,False,False
2026-03-26 08:25:28,2.631,68.1,-16.0,97.4,0.0,63.0,-4.0,,,,,,,False,False,False
2026-03-26 08:33:09,2.631,67.8,-2.34,100.0,20.3,63.5,3.9,,,,,,,False,False,False
2026-03-26 08:55:28,2.83,69.3,4.03,100.0,0.0,64.4,2.42,,,,,,,False,False,False

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