---
hide:
  - navigation
  - toc
---

# 🏗️ The Architecture of GardenOS

<style>
/* Full Width Overrides */
.md-content__inner { max-width: none !important; margin: 0 !important; padding: 1rem 2rem !important; }
.md-main__inner { max-width: none !important; }
.md-sidebar { display: none !important; }
</style>

GardenOS is a digital twin of a desk-top biome. It's built as decoupled layers — sensing, context, reasoning, and publishing each run independently, so if one breaks the others keep going.

## 📡 System Data Flow

```mermaid
graph TD
    %% Layer 1: Data Collection
    subgraph Collection["1. DATA COLLECTION (cron / launchd on MacBook)"]
        AR[Arduino Uno: Temp, Humidity, Light, Soil] -->|Serial| WPY[warden.py]
        WPY --> CSV[telemetry.csv]
        WPY --> MET[metrics.csv]
        WPY --> SNS[current_snapshot.json]
        WPY --> STS[warden_state.json]

        CAM[USB Webcam] -->|OpenCV| VPY[vision.py]
        VPY -->|Frames sent to Gemma 3 via Google AI Studio| VJS[vision_observation.json]
        VPY --> VMD[vision_observation.md]

        OWM[OpenWeatherMap API] --> WSC[weather_scout.py]
        WSC --> WTH[weather_context.json]
    end

    %% Layer 2: SILICA Context Layer
    subgraph SILICA["2. SILICA (Context Layer)"]
        CSV & MET & SNS & STS & VJS & WTH --> POC[prep_observer_context.py]
        GM[GARDEN_MANIFEST.md — World Model] --> POC
        PC[plants.json — Plant Config] --> POC
        POC --> CTX[observer_context.md]
    end

    %% Layer 3: The Warden / Observer
    subgraph Warden["3. THE WARDEN (OpenClaw)"]
        CTX --> OC[OpenClaw Agent]
        OC <-->|Reasoning| LLM[LLM via OpenRouter]
        OC --> LDG[vision_ledger.md]
        OC --> SLK[Slack #plantclaw]
    end

    %% Layer 4: Public Presence
    subgraph Public["4. PUBLIC PRESENCE (Sync & Publish)"]
        LDG --> SYNC[sync.sh]
        CSV & VJS & VMD --> SYNC
        SYNC --> GH[GitHub Repo]
        GH --> WEB[GitHub Pages — Live Dashboard & Blog]
    end

    %% Styling
    style Collection fill:#1e293b,stroke:#334155,color:#fff
    style SILICA fill:#0f172a,stroke:#4ade80,color:#fff
    style Warden fill:#1e1b4b,stroke:#a855f7,color:#fff
    style Public fill:#064e3b,stroke:#4ade80,color:#fff
    style LLM fill:#4338ca,stroke:#818cf8,color:#fff
```

---

## 🌎 The Environment

The biome sits in Chennai, but the outdoor climate has almost nothing to do with what happens on the desk. That disconnect is the whole reason the context layer exists.

### The outdoors
The room is on the 1st floor with an open terrace above. That terrace soaks up Chennai sun all day and radiates heat into the room between noon and 3pm. Outside it's typically 30°C+ with high humidity. That's the drift state when cooling is off.

### The room
The north window (2m from the desk) gives only indirect diffuse light — no UV spikes, no scorch. The east wall blocks morning sun entirely. So the plants never see direct sunlight.

### Cooling
The room climate follows a human-comfort hierarchy:

* Fan S (south): baseline air exchange, always on when I'm at the desk
* Fan N (north): extra airflow when it's hot
* The AC: last resort. Clamps temp at 26°C but tanks humidity and pushes VPD up

### The desk
Wooden surface, acts as a thermal insulator. The pots are decoupled from the desk mass. There's a white rabbit figurine (50mm) that serves as a mm-scale reference for the camera.

---

## 🛠️ Layer Breakdown

### 1. Data collection

Three Python scripts run on the MacBook via cron/launchd. No orchestrator, no framework — they just run at the OS level and write flat files to `data/`.

`warden.py` connects to the Arduino over serial and reads temp, humidity, light, and soil moisture. It writes `telemetry.csv`, `metrics.csv`, `current_snapshot.json`, and `warden_state.json`.

`vision.py` grabs a frame from the webcam via OpenCV, then sends it to Gemma 3 on Google AI Studio for visual interpretation. Gemma 3 describes what it sees — leaf color, posture, soil surface — and the output goes to `vision_observation.json` and `vision_observation.md`. This is perception only, not reasoning.

`weather_scout.py` fetches current Chennai weather from OpenWeatherMap for the outdoor macro-context. Output goes to `weather_context.json`.

OpenClaw has nothing to do with this layer. These scripts run whether or not the reasoning layer is alive.

### 2. SILICA (context layer)

SILICA is a collection of scripts and config files that sit between raw data and the LLM. The job is to turn CSV rows into something the model can actually reason about, and to stop it from hallucinating based on outdoor Chennai weather.

`prep_observer_context.py` reads all the data files from layer 1, merges them with `GARDEN_MANIFEST.md` (the world model — physical constants of the biome) and `scripts/config/plants.json` (species, calibration, thresholds), and produces one file: `observer_context.md`.

The LLM never sees raw telemetry. It gets things like "VPD: 3.5 kPa, rising trend" and "Soil p1 (Nickels): dry, below threshold." That's the whole point.

### 3. The Warden (OpenClaw)

OpenClaw reads `observer_context.md` and sends it to an LLM. The model reasons about plant health — cross-checking sensors against visual evidence, comparing against recent history, flagging anything that needs attention. Output goes to `logs/vision_ledger.md` and gets posted to Slack `#plantclaw`.

### 4. Publishing

`sync.sh` builds the MkDocs site, commits everything to GitHub, and pushes to GitHub Pages. The dashboard reads CSVs straight from the repo. No database, no backend.

---

## 🛡️ Resilience

* If reasoning fails, data still collects. If weather fails, sensors still log. Each layer is independent.
* The dashboard is stateless — it reads repo artifacts directly, no database.
* Data syncs via git commits, so every push is an atomic checkpoint.
