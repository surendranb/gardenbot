# 🌿 Gardenbot: Master State Ledger

## 🎯 Global Vision
Project SILICA. A centralized, self-learning biological and technical intelligence framework for an indoor garden in Chennai. Prioritizes "Local Truth" (visual turgidity, Vapor Pressure Deficit, acoustic confirmation) over textbook guesses.

## 🛠 Active Technical Stack
- **Hardware**: ESP/Arduino for Moisture (A0-A3), BME680 (Address 0x76 DHT/VPD), Dual Fans (South/North).
- **Data Pipeline**: `launchd` triggers `pulse.sh` (30m intervals), executing `scripts/warden.py`.
- **Reasoning**: Context built via `prep_observer_context.py` into `observer_context.md`, then reasoned upon by the OpenClaw agent (`jobs.json`).
- **Publishing**: `sync.sh` deployed into an MkDocs site via regular GH Pages commits.

## 🚦 Current Development State
- **Status**: Self-learning agent enabled, active VPD and ambient transpiration auditing.
- **Current Issue**: Deep troubleshooting active. BME680 I2C bus hangs, telemetry timeouts, and possible acoustic capture hangs.
- **Immediate Goal**: Validate hardware constraints (3.0s settle delay, 5.0s loop cycle) and stabilize sensor readings into the telemetry pulse.

---
*Status: Ontology Tier 1 Active | Auto-Synthesized per L-1 Rules*
