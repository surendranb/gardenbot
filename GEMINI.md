## 1. The data & reasoning split

The system has a clear boundary between local execution and cloud intelligence:

- **Local (data collection)**: Three Python scripts (`warden.py`, `vision.py`, `weather_scout.py`) run on the MacBook via cron/launchd. They collect telemetry, visual observations, and weather data, writing flat files to `data/`. No orchestrator involved.
- **Cloud (reasoning)**: The Warden runs via OpenClaw, reads the synthesized context, and calls an LLM for botanical reasoning, anomaly detection, and reporting.
- **The bridge — SILICA**: `prep_observer_context.py`, `GARDEN_MANIFEST.md` (the world model), and `plants.json` (plant config) turn raw data files into semantic facts in `observer_context.md`. The LLM gets facts, not noise.

---

## 2. The loop

Three steps, repeated on a schedule:

1. **Collect (local, cron/launchd)**: `warden.py` reads Arduino sensors. `vision.py` captures a webcam frame and sends it to Gemma 3 on Google AI Studio for visual interpretation. `weather_scout.py` fetches Chennai weather from OpenWeatherMap. All output goes to `data/`.
2. **Reason (OpenClaw + LLM)**: `prep_observer_context.py` synthesizes everything into `observer_context.md`. OpenClaw's Warden reads it, calls an LLM, compares visual evidence against sensor data, and reconciles with the world model.
3. **Share**: Findings go to `vision_ledger.md` and Slack `#plantclaw`. `sync.sh` commits and pushes to GitHub Pages.

---

## 3. Domain separation

- **Local**: cron/launchd Python scripts on MacBook, raw data in `data/` and `media/`.
- **Cloud**: OpenClaw calling an LLM for reasoning. Gemma 3 on Google AI Studio for vision. Persistent state in the GitHub repo.
- **Public**: GardenOS site on GitHub Pages, Slack `#plantclaw`.
