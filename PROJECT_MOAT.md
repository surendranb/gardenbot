# 🏰 Project MOAT: GardenOS Resilience Architecture

## 1. MISSION
To transform GardenOS from a fragile collection of scripts into a robust, "local-first" botanical intelligence system that gracefully handles hardware, network, and permission failures while maintaining a high-fidelity public narrative.

## 2. THE THREE PILLARS (COLLECT -> REASON -> SHARE)

### 🟢 PILLAR 1: THE COLLECTOR (Hardware Interface)
*   **Role**: Reliable polling of Arduino (Serial) and USB Webcam.
*   **Mechanism**: macOS `launchd` Service (replaces `cron` for better TCC/Camera permissions).
*   **Data Target**: 
    *   `data/telemetry.csv` (Raw sensor values)
    *   `data/weather.csv` (Historical forecast/actuals)
    *   `media/latest.jpg` (Fresh visual ground-truth)
*   **Resilience**: Implements a 3-frame camera warmup and serial retry logic. No internet dependency.

### 🧠 PILLAR 2: THE REASONER (Intelligence/OpenClaw)
*   **Role**: Outlier detection and botanical narrative.
*   **Mechanism**: OpenClaw Agent (The Warden).
*   **Mechanism**: OpenClaw Agent (The Warden) + Semantic Synthesis Layer.
*   **Intelligence**: 
    *   **World Model**: Uses codified physical constants (Indoor truth) to interpret sensors.
    *   **Semantic Synthesis**: Converts telemetry into high-level botanical facts.
    *   **Temporal Memory**: Compares current state vs. historical baselines.
*   **Output**: Appends findings to `docs/blog/posts/[date].md` and Slack `#plantclaw`.

### 🌐 PILLAR 3: THE SHARER (Public Presence)
*   **Role**: Atomic synchronization of state to GitHub.
*   **Mechanism**: `scripts/sync.sh` via SSH (replaces HTTPS to fix "Device not configured" errors).
*   **Site Engine**: **MkDocs-Material**. 
    *   **Dashboard**: A stateless JS-driven page fetching raw CSVs from the GitHub Repo.
    *   **Blog**: Automated AI-generated posts from the Reasoner.

---

## 3. DATA ARCHITECTURE (Single Source of Truth)

| File | Type | Purpose |
| :--- | :--- | :--- |
| `data/telemetry.csv` | CSV | Historical raw sensor data. |
| `data/metrics.csv` | CSV | Computed values (VPD, Soil %, Vigor Scores). |
| `data/weather.csv` | CSV | Historical weather (Temp, Hum, Forecast Pop, VPD_expected). |
| `data/observer_context.md` | MD | Synthesized "Daily Facts" for the Warden. |
| `media/latest.jpg` | JPG | Most recent visual ground-truth. |
| `docs/blog/` | MD | The "Warden's Ledger" - AI-generated historical narrative. |
| `PROJECT_SILICA.md` | MD | The Cognitive Architecture blueprint. |

---

## 4. EXECUTION ROADMAP

### Phase 1: Structural Consolidation [x]
1.  **Consolidate Paths**: Move all fragmented data from `docs/data/` to root `data/`.
2.  **SSH Implementation**: Generate local SSH key and update GitHub remote.
3.  **World Model**: Codify physical constants in `GARDEN_MANIFEST.md`.

### Phase 2: Cognitive Intelligence [/]
1.  **Semantic Synthesis**: Upgrade `prep_observer_context.py` to fact-based synthesis.
2.  **Baseline Completion**: Finalize 7-day visual history.
3.  **Memory Core**: Implement SQLite-based phenological tracking (Phase 3).

### Phase 3: Hardware Stabilization
1.  **Launchd Migration**: Move capture loops from `cron` to `launchd`.
2.  **Camera Logic**: Implement exposure warmup in `scripts/vision.py`.

## 5. VERIFICATION CHECKLIST
- [x] Weather Scout: `data/weather.csv` updated.
- [x] Warden: `data/telemetry.csv` and `data/metrics.csv` updated.
- [x] Vision: `media/latest.jpg` capture successful.
- [x] Prep Context: `data/observer_context.md` generated with new paths.
- [x] Sync Agent: `scripts/sync.sh` commits and pushes successfully.

## 7. BLOGGING SOP
To write a new blog post:
1. Create a file in `src/docs/blog/posts/YYYY-MM-DD-title.md`.
2. Ensure it has the standard frontmatter (Date, Description).
3. Use the `<!-- more -->` tag to define the snippet for the index page.
4. Run `./scripts/sync.sh` (or wait for the cron) to publish.
