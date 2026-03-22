#!/bin/bash

# Configuration
REPO_ROOT="/Users/surendran/.openclaw/workspace/gardenbot"
DOCS_DIR="$REPO_ROOT/docs"
WEB_DIR="$REPO_ROOT/web"
MEDIA_DIR="$REPO_ROOT/media"
DATA_DIR="$REPO_ROOT/data"

# Ensure docs structure exists
mkdir -p "$DOCS_DIR/media"
mkdir -p "$DOCS_DIR/data"

# 1. Copy Assets
cp "$MEDIA_DIR/latest.jpg" "$DOCS_DIR/media/"
cp "$MEDIA_DIR/dashboard.png" "$DOCS_DIR/media/"
cp "$DATA_DIR/current_snapshot.json" "$DOCS_DIR/data/"
cp "$DATA_DIR/telemetry.csv" "$DOCS_DIR/data/"

# 2. Process HTML (Fix paths for GitHub Pages structure)
# Changes "../media" to "./media" and "../data" to "./data"
sed 's|\.\./media|./media|g' "$WEB_DIR/index.html" > "$DOCS_DIR/index.html.tmp"
sed 's|\.\./data|./data|g' "$DOCS_DIR/index.html.tmp" > "$DOCS_DIR/index.html"
rm "$DOCS_DIR/index.html.tmp"

# 3. Commit and Push
cd "$REPO_ROOT"
git add docs/
git commit -m "GardenOS Auto-Publish: $(date)"
git push origin main
