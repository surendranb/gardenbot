# 🌊 GardenOS: System Flow & Architecture

This document outlines the data pipeline, automation triggers, and intelligence loops that power GardenOS.

## 1. The Core Loop (Local Telemetry)
*Managed by macOS `crontab`*

The system runs a tight loop to gather ground-truth data before the AI Agent is ever invoked.

| Time (Min) | Script | Purpose |
| :--- | :--- | :--- |
| **:25, :55** | `warden.py` | **Telemetry**: Reads sensors (A0-A5) -> `telemetry.csv`, `metrics.csv`. Updates dashboard. |
| **:50** | `vision.py` | **Eyes**: Captures high-res `latest.jpg`. Archives strictly. |
| **:58** | `prep_observer_context.py` | **Briefing**: Aggregates Telemetry + Weather + Vision Ledger into `observer_context.md`. |

**Why this order?**
1.  **Sensors first**: Get the raw numbers.
2.  **Vision second**: Capture the visual state (potentially correlated with sensor readings).
3.  **Prep last**: Package everything so the Agent has a single, static "Truth File" to read at the top of the hour.

## 2. The Intelligence Loop (Agentic)
*Managed by OpenClaw (`jobs.json`)*

The AI Agent (Gemini) wakes up on a schedule to interpret the pre-packaged data.

### A. The Weather Scout (05:30 AM)
*   **Trigger**: `jobs.json` (Daily)
*   **Action**: Runs `weather_scout.py`.
*   **Output**: Updates `data/weather_context.json` with today's forecast (Rain/Heat/VPD).
*   **Purpose**: Gives the "Observer" context on *future* stress (e.g., "It's going to be 38°C today, warn the human").

### B. The Garden Observer (Every 3 Hours)
*   **Trigger**: `jobs.json` (06, 09, 12, 15, 18, 21:00)
*   **Persona**: Agricultural Statistician (Chennai Specialist).
*   **Input**:
    *   `GARDEN_MANIFEST.md`: The "Rulebook" (Plant IDs, Thresholds).
    *   `observer_context.md`: The "Situation Report" (Live Data + Weather + History).
    *   `latest.jpg`: The "Visual Proof".
*   **Process**:
    1.  **Synthesize**: Compare Sensor % vs. Visual Turgidity.
    2.  **Decide**: Is the sensor drifting? Is the plant thirsty?
    3.  **Log**: Write to `logs/vision_ledger.md` (Long-term memory).
    4.  **Report**: Post to Slack (`#plantclaw`) with `latest.jpg`.

## 3. Data Flow Diagram

```mermaid
graph TD
    subgraph "Hardware (Mac Mini + Gardenbot)"
        Sensors[Sensors (A0, A2, A5)] -->|Serial| Warden(warden.py)
        Cam[Webcam] -->|USB| Vision(vision.py)
        OWM[OpenWeatherMap] -->|API| Scout(weather_scout.py)
    end

    subgraph "Data Layer (Files)"
        Warden -->|Writes| Telemetry[telemetry.csv]
        Warden -->|Writes| Dashboard[dashboard.png]
        Vision -->|Writes| Jpg[latest.jpg]
        Scout -->|Writes| Weather[weather_context.json]
        
        Telemetry & Weather & Jpg --> Prep(prep_observer_context.py)
        Prep -->|Generates| Context[observer_context.md]
    end

    subgraph "Intelligence (OpenClaw)"
        Context -->|Reads| Observer[Observer Agent]
        Manifest[GARDEN_MANIFEST.md] -->|Reads| Observer
        Observer -->|Writes| Ledger[vision_ledger.md]
        Observer -->|Posts| Slack[#plantclaw]
    end
```

## 4. Key File Locations
*   **Scripts**: `/Users/surendran/.openclaw/workspace/gardenbot/scripts/`
*   **Data**: `/Users/surendran/.openclaw/workspace/gardenbot/docs/data/`
*   **Logs**: `/Users/surendran/.openclaw/workspace/gardenbot/logs/`
*   **Config**: `/Users/surendran/.openclaw/workspace/gardenbot/config/`
