#!/bin/bash
# 🌐 GardenOS Sync Agent
# This script handles the public presence of the garden.

BASE_DIR="/Users/surendran/.openclaw/workspace/gardenbot"
MKDOCS_VENV="$BASE_DIR/.venv_mkdocs"
cd "$BASE_DIR"

log() {
    printf "%s %s\n" "$(date +'%Y-%m-%d %H:%M:%S')" "$*"
}

ensure_remote() {
    git fetch origin main >/dev/null 2>&1
    counts=$(git rev-list --left-right --count HEAD...origin/main 2>/dev/null || echo "0 0")
    behind=$(echo "$counts" | awk '{print $2}')
    if [ -n "$behind" ] && [ "$behind" -gt 0 ]; then
        log "Remote has $behind unseen commit(s); rebasing onto origin/main."
        git pull --rebase origin main >/dev/null
    fi
}

push_with_retry() {
    log "Pushing to GitHub..."
    if git push origin main; then
        log "Sync Successful."
        return 0
    fi

    log "Push failed; pulling remote and retrying."
    git pull --rebase origin main >/dev/null
    if git push origin main; then
        log "Sync Successful after rebasing."
    else
        log "Sync Failed even after rebasing; please inspect the repo."
        return 1
    fi
}

log "--- Sync Start: $(date +'%Y-%m-%d %H:%M:%S') ---"

log "Generating gallery metadata..."
echo "[" > data/gallery.json
FIRST_ENTRY=true
for dir in $(ls -r archive/ | grep "^202"); do
    img=$(ls "archive/$dir"/*.jpg 2>/dev/null | head -n 1)
    if [ -n "$img" ]; then
        if [ "$FIRST_ENTRY" = false ]; then echo "," >> data/gallery.json; fi
        echo "  {\"date\": \"$dir\", \"path\": \"$img\"}" >> data/gallery.json
        FIRST_ENTRY=false
    fi
done

echo "]" >> data/gallery.json

log "Building site..."
source "$MKDOCS_VENV/bin/activate"
cd src && mkdocs build -d ../docs
cd ..
deactivate

ensure_remote

log "Staging all assets..."
git add data/ media/ logs/ docs/ src/ archive/ PROJECT_MOAT.md

if git diff --cached --quiet; then
    log "No changes to sync."
else
    log "Staging changes..."
    git commit -m "GardenOS Sync: $(date +'%Y-%m-%d %H:%M:%S')"
fi

push_with_retry
