# 🛠️ GardenOS Project Tracker

## 📋 Overview
This document tracks the active development, refactoring, and roadmap for the GardenOS (Garden Warden) project.

## 🏗️ System Architecture & Operational Rhythm
(See `docs/FLOW.md` for full details)

The system operates on two distinct loops:
1.  **Local Telemetry Loop (Mac Cron)**:
    *   **:25 & :55**: `warden.py` captures sensor data (A0-A5), calculates VPD, and updates CSVs.
    *   **:50**: `vision.py` captures high-res imagery (`latest.jpg`).
    *   **:58**: `prep_observer_context.py` aggregates all data into `observer_context.md`.
2.  **Intelligence Loop (OpenClaw Agent)**:
    *   **05:30**: `weather_scout.py` fetches the day's forecast.
    *   **Every 3 Hours**: Agent wakes up, reads `observer_context.md` + `latest.jpg`, and posts a report to Slack.

## 🚨 Immediate Priorities (Fixes & Refactoring)
- [x] **Disabled Memory**: Turned off `openclaw-mem0` to fix timeouts.
- [x] **Git Sync Fix**: Updated `warden.py` to use `gh auth token`.
- [x] **Create README.md**: Established central documentation.
- [x] **Document Flow**: Created `docs/FLOW.md` to map crons and agents.
- [x] **Document Flow**: Created `docs/FLOW.md` to map crons and agents.
- [ ] **Repo Structure**: Consolidate and clean up `scripts/`.
- [ ] **Dependency Management**: Create `requirements.txt`.

## 🚀 Roadmap status

### Phase 1: Connectivity & Weather (PARTIAL)
- [x] Create `~/.config/openweathermap/credentials.json`.
- [x] Implement `scripts/weather_scout.py`.
- [ ] **Integration**: Ensure `warden.py` reads `weather_context.json`.
- [ ] **Scheduling**: Verify `weather-scout` in `jobs.json`.

### Phase 2: The Logic Engine (PARTIAL)
- [x] **Tetens Equation**: Implemented in `warden.py` (`compute_metrics`).
- [ ] **Linear Regression**: 72h slope analysis is **MISSING** in `warden.py`.
- [ ] **OWM Integration**: `warden.py` needs to use forecasted VPD.

### Phase 3: Continuity & Memory
- [ ] Extend Snapshot to include last 3 `vision_ledger.md` entries.
- [ ] Update `AGENTS.md` with Sunday Auto-Updates.

### Phase 4: The 7-Day Baseline
- [ ] Establish daily "Benchmark" run @ 09:00 AM.
- [ ] Lock in visual landmarks.

## 📝 Technical Notes
- **Tetens Eq**: Used for local VPD calculation.
- **Sensors**: All capacitive (TLC555 based).
- **Platform**: macOS (Darwin), Python 3.14.
