#!/bin/bash
# 🌿 GardenOS Pulse Agent
# This script runs the full data collection and sync sequence.

BASE_DIR="/Users/surendran/.openclaw/workspace/gardenbot"
cd "$BASE_DIR"

log() {
    printf "%s [PULSE] %s\n" "$(date +'%Y-%m-%d %H:%M:%S')" "$*" >> logs/cron.log
}

run_with_timeout() {
    local timeout=$1
    shift
    "$@" &
    local pid=$!
    ( sleep $timeout && kill -9 $pid 2>/dev/null && log "CRITICAL TIMEOUT: command '$1' exceeded ${timeout}s and was externally terminated" ) &
    local watchdog=$!
    wait $pid 2>/dev/null
    local exit_status=$?
    kill -9 $watchdog 2>/dev/null
    return $exit_status
}

log "Starting Pulse..."

# 0. Pre-flight Check (Hardware Presence)
if [ ! -e "/dev/cu.usbmodem1201" ]; then
    log "CRITICAL: Arduino port /dev/cu.usbmodem1201 not found. Aborting sensor capture."
    # We still run sync to ensure logs are pushed
    run_with_timeout 180 bash scripts/sync.sh >> logs/sync.log 2>&1
    exit 1
fi

# 1. Warden (Sensors)
run_with_timeout 120 ./.venv/bin/python3 scripts/warden.py >> logs/cron.log 2>&1

# 2. Context Prep (Step A: Vision Context)
run_with_timeout 60 ./.venv/bin/python3 scripts/prep_observer_context.py --vision-only >> logs/cron.log 2>&1

# 3. Vision (Camera)
run_with_timeout 300 ./.venv/bin/python3 scripts/vision.py >> logs/cron.log 2>&1

# 4. Context Prep (Step B: Full Synthesis)
run_with_timeout 60 ./.venv/bin/python3 scripts/prep_observer_context.py >> logs/cron.log 2>&1

# 5. Sync to GitHub
run_with_timeout 300 bash scripts/sync.sh >> logs/sync.log 2>&1

log "Pulse Complete."
