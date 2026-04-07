## 🌿 Garden Warden Mode (Digital Familiar)

- **Persona**: An expert agricultural statistician with a specialty in tropical meteorology (Chennai context). 
- **Core Philosophy**: "Local Truth over Textbook Guesses." Prioritize visual turgidity, deterministic math (VPD/Slopes), and acoustic ground-truth over raw sensor alarms.
- **Decision Engine**: 
    1. Deterministic Data (Sensors via `warden.py` & Mic acoustics for fan state) 
    2. Visual Delta (Photo comparison via `vision.py`) 
    3. Strategy Alignment (GARDEN_MANIFEST.md & `human_actions.jsonl`) 
    4. Narrative Decision (OpenClaw Agent via 3h jobs.json).

---

## 1. The Decentralized Architecture (v2.1)

The system is fully decoupled into 4 distinct functional layers:

- **1. Collection (`launchd`/Local)**: `pulse.sh` runs every 30m to pull telemetry from the Arduino (`warden.py`) and capture webcam imagery (`vision.py`). Ambient climate variables are checked separately twice daily via `weather_scout.py`.
- **2. The Context Layer (SILICA v2.2)**: `prep_observer_context.py` acts as the pre-frontal cortex. It calculates nested temporal windows (4h, 24h, 72h, 7d) and captures acoustic empirical proof of AC/Fan airflow. It synthesizes all visual logs, telemetry, and manual human interventions into one single source of truth: `data/observer_context.md`.
- **3. Reasoning (OpenClaw/Cloud)**: A dedicated OpenClaw job (`~/.openclaw/cron/jobs.json`) running every 3 hours reads the prepared SILICA context. It reconciles conflicting data (e.g. human actions invalidating sensor drift) and broadcasts targeted action plans to Slack. (Note: Older local reasoning scripts like `warden_reasoning.py` are archived in `local/obsolete/`).
- **4. Publishing (`sync.sh`)**: Generates MkDocs from `src/` and commits data endpoints seamlessly to GitHub Pages for the stateless frontend dashboard.

---

## 2. The Multi-Resolution Verification Loop

1. **Pulse (4h)**: Captures immediate micro-climate shifts (AC pulses, Misting, Transpiration spikes from fans).
2. **Rhythm (72h)**: Tracks the dry-down metabolic curve of the soil.
3. **Motion Picture (7 Days)**: Anchored against a 7-day visual baseline to detect slow growth/decline.
4. **Resolution (HITL)**: Human manual-care interventions inside `human_actions.jsonl` instantly de-poison the visual or sensor context from lingering "failure narratives."

---

## 3. Strict Domain Boundaries

- **State Persistence**: launchd schedules, raw CSVs in `data/`, visual histories in `logs/`. 
- **Agent Context**: `data/observer_context.md`. This is the sole source of intelligence for the Agent execution layer.
- **Public Exposure**: Static web presentation via MkDocs and Slack alerts in `#plantclaw`.