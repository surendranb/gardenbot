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

# 0. Pre-flight Check (Hardware Presence & Lock Cleanup)
ARDUINO_PORT=$(ls /dev/cu.usbmodem* /dev/cu.usbserial* 2>/dev/null | head -n 1)

if [ -z "$ARDUINO_PORT" ]; then
    log "CRITICAL: No Arduino USB port found. Aborting sensor capture."
    # We still run sync to ensure logs are pushed
    run_with_timeout 180 bash scripts/sync.sh >> logs/sync.log 2>&1
    exit 1
fi

log "Found Arduino at $ARDUINO_PORT"

# Cleanup zombie serial handles
ZOMBIE_PID=$(lsof -t "$ARDUINO_PORT" 2>/dev/null)
if [ ! -z "$ZOMBIE_PID" ]; then
    log "WARNING: Port $ARDUINO_PORT held by PID $ZOMBIE_PID. Terminating zombie process."
    kill -9 $ZOMBIE_PID 2>/dev/null
    sleep 2
fi

# 1. Warden (Sensors)
run_with_timeout 120 ./.venv/bin/python3 scripts/warden.py >> logs/cron.log 2>&1

# 2. Context Prep (Step A: Vision Context)
run_with_timeout 60 ./.venv/bin/python3 scripts/prep_observer_context.py --vision-only >> logs/cron.log 2>&1

# 3. Vision (Camera)
run_with_timeout 300 ./.venv/bin/python3 scripts/vision.py >> logs/cron.log 2>&1

# 4. Context Prep (Step B: Full Synthesis)
run_with_timeout 60 ./.venv/bin/python3 scripts/prep_observer_context.py >> logs/cron.log 2>&1

# 5. Agent Audit & Slack Delivery
log "Running Agent Audit..."
# Run the agent and capture the output.
REPORT=$(/Users/surendran/.pnpm-global/openclaw agent --agent main --message "COMMAND_PROTOCOL: AUTONOMOUS_WARDEN_AUDIT

1. PERCEIVE: Read \`/Users/surendran/.openclaw/workspace/gardenbot/data/observer_context.md\` to retrieve the latest synthesized telemetry, weather, visual ground truth, and recent history.
2. AUDIT: Reconcile the data. Are the plants visually turgid? Is the telemetry logically sound? Are there hardware failures or botanical crises? Note any changes from the previous history.
3. REPORT: Deliver a high-signal report. No AI-isms. Just literal, actionable truth. If human action is required, e.g. watering, explicitly state it!")

# Archive the report
./.venv/bin/python3 scripts/archive_report.py "$REPORT"

# Deliver to Slack
/Users/surendran/.pnpm-global/openclaw message send --channel slack --target C0AK6A4SJES --message "$REPORT" --media media/latest.jpg >> logs/cron.log 2>&1

# 6. Sync to GitHub
run_with_timeout 300 bash scripts/sync.sh >> logs/sync.log 2>&1

log "Pulse Complete."
