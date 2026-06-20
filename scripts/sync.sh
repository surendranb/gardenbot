#!/bin/bash
# 🌐 GardenOS v2 Sync Agent
# Compiles the static database and pushes it to GitHub Pages.

BASE_DIR="/Users/surendran/.openclaw/workspace/gardenbot"
GIT="/usr/bin/git"

# 🔑 SSH Configuration for Cron / Daemons
export GIT_SSH_COMMAND="/usr/bin/ssh -i /Users/surendran/.ssh/id_ed25519 -o IdentitiesOnly=yes"

cd "$BASE_DIR"

log() {
    printf "%s %s\n" "$(date +'%Y-%m-%d %H:%M:%S')" "$*"
}

log "--- Sync Start ---"

# 1. Export Data and Compile React Dashboard
log "Exporting database to JSON..."
/Users/surendran/.openclaw/workspace/gardenbot/.venv/bin/python3 scripts/export_data.py

log "Building React dashboard..."
cd "$BASE_DIR/dashboard"
npm run build >/dev/null 2>&1
cd "$BASE_DIR"

log "Copying dashboard build to docs..."
cp -R dashboard/dist/* docs/

# 2. Rebase onto origin to avoid conflict
log "Pulling latest changes..."
$GIT fetch origin main >/dev/null 2>&1
$GIT pull --rebase origin main >/dev/null 2>&1

# 3. Stage changes
log "Staging assets..."
$GIT add docs/ README.md .gitignore

# 4. Commit and Push
if $GIT diff --cached --quiet; then
    log "No changes to sync."
else
    log "Committing changes..."
    $GIT commit -m "GardenOS Sync: $(date +'%Y-%m-%d %H:%M:%S')"
    
    log "Pushing to GitHub..."
    if $GIT push origin main; then
        log "Sync Successful."
    else
        log "Push failed; pulling remote and retrying..."
        $GIT pull --rebase origin main >/dev/null
        if $GIT push origin main; then
            log "Sync Successful after rebase retry."
        else
            log "Sync Failed."
            exit 1
        fi
    fi
fi
