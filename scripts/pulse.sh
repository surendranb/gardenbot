#!/bin/bash
# 🌿 GardenOS Pulse Agent
# This script runs the full data collection and sync sequence.

BASE_DIR="/Users/surendran/.openclaw/workspace/gardenbot"
cd "$BASE_DIR"

log() {
    printf "%s [PULSE] %s\n" "$(date +'%Y-%m-%d %H:%M:%S')" "$*" >> logs/cron.log
}

log "Starting Pulse..."

# 1. Warden (Sensors)
./.venv/bin/python3 scripts/warden.py >> logs/cron.log 2>&1

# 2. Context Prep (Step A: Vision Context)
./.venv/bin/python3 scripts/prep_observer_context.py --vision-only >> logs/cron.log 2>&1

# 3. Vision (Camera)
./.venv/bin/python3 scripts/vision.py >> logs/cron.log 2>&1

# 4. Context Prep (Step B: Full Synthesis)
./.venv/bin/python3 scripts/prep_observer_context.py >> logs/cron.log 2>&1

# 4. Sync to GitHub
bash scripts/sync.sh >> logs/sync.log 2>&1

log "Pulse Complete."
