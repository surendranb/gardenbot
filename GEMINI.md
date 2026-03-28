## 1. THE DATA & REASONING SPLIT
The system operates across a clear boundary between Local Execution and Cloud Intelligence:

- **⚙️ LOCAL (Data Collection)**: Three Python scripts (`warden.py`, `vision.py`, `weather_scout.py`) run independently on the MacBook via **cron/launchd**. They gather raw telemetry, visual observations, and weather data, writing flat files to `data/`. These scripts have no dependency on OpenClaw or any orchestrator.
- **🛰️ CLOUD (Reasoning & Synthesis)**: The **Warden/Observer** (running via OpenClaw) receives synthesized context and calls an LLM to perform high-level botanical reasoning, anomaly detection, and narrative generation.
- **🧠 THE BRIDGE: SILICA (Context Layer)**: A collection of scripts and artifacts — `prep_observer_context.py`, `GARDEN_MANIFEST.md` (the World Model), and `plants.json` (plant config) — that synthesize raw data files into semantic facts in `observer_context.md`. SILICA ensures the LLM receives high-value "Facts" rather than low-value "Noise."

---

## 2. THE WARDEN'S PROTOCOL (3-STEP LOOP)
The Warden executes a rigorous audit loop across the Local/Cloud boundary:

1.  **📊 STEP 1: COLLECT (Local / cron/launchd)**
    System-level scripts run on the MacBook independently. `warden.py` reads Arduino sensors and writes telemetry. `vision.py` captures a webcam frame and sends it to **Gemma 3 via Google AI Studio** for visual interpretation (perception, not reasoning). `weather_scout.py` fetches Chennai weather from OpenWeatherMap. All data is stored in `data/`.
2.  **🔍 STEP 2: REASON (OpenClaw / LLM)**
    `prep_observer_context.py` (SILICA) synthesizes all data files plus the World Model into `observer_context.md`. OpenClaw's Warden agent reads this context and calls an LLM to perform **Cross-Verification** (comparing visual evidence vs. sensor telemetry) and reconcile observations with the World Model.
3.  **📢 STEP 3: SHARE (Public / GardenOS)**
    The Warden's findings are written to `vision_ledger.md` and posted to Slack `#plantclaw`. `sync.sh` commits everything and pushes to GitHub Pages.

---

## 3. DOMAIN SEPARATION
- **💻 LOCAL (Device)**: cron/launchd-scheduled Python scripts on MacBook, raw data storage (`data/`, `media/`).
- **☁️ CLOUD (Intelligence)**: OpenClaw's Warden agent calling an LLM for reasoning; Gemma 3 on Google AI Studio for vision interpretation. Persistent state in GitHub repo.
- **📢 PUBLIC (Presentation)**: GardenOS Website (GitHub Pages) and Slack (#plantclaw).
