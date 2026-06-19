# 🌿 GardenBot v2

An autonomous Jade plant (Crassula ovata) monitoring and diagnostic system in Chennai, adopting the simplified **Thermostat Pattern**.

## 🏗️ Architecture

```
┌───────────────────────────────────────────────┐
│               SQLite: garden.db               │
│  ┌──────────┐ ┌──────────┐ ┌───────────────┐  │
│  │telemetry │ │ weather  │ │ interpretations│  │
│  └────▲─────┘ └────▲─────┘ └───────▲───────┘  │
└───────│────────────│───────────────│──────────┘
        │            │               │
  ┌─────┴────────────┴─────┐   ┌─────┴─────┐
  │   collect.py (every 30m)│   │   Warden  │
  └────────────────────────┘   │   Agent   │
                               └─────┬─────┘
                                     │ delivers
                               ┌─────▼─────┐
                               │   Slack   │
                               └───────────┘
```

- **Database is Ground Truth**: Everything is logged in a single SQLite database (`data/garden.db`).
- **Dumb Collectors**: `collect.py` runs every 30 minutes via launchd to poll the Arduino (BME680, light, soil moisture), scan environmental sound level, fetch OpenWeatherMap parameters, and log them directly.
- **Vision Capture**: `vision.py` captures a camera image and runs Gemini Vision 5 minutes before the Warden wakes. It logs turgidity and soil wetness assessment into the database.
- **Smart Agent**: The Warden agent wakes up every 4 hours, queries `garden_math.py` (which runs a localized physics engine calculating VPD and soil trends), logs its interpretation back to the database, and delivers a status report to Slack.
- **Static Pages Hosting**: A compiler `scripts/build_static.py` dumps the database state to `docs/data.json` and prepares the static index page. This is pushed to GitHub Pages for automated public display.

## 📂 Folder Layout

```
gardenbot/
├── .agents/
│   └── garden_warden/         # OpenClaw agent prompts & preferences
├── docs/                      # Static GitHub Pages directory
│   ├── index.html             # Single-page dashboard UI (ChartJS)
│   ├── data.json              # Public database state JSON
│   └── latest.jpg             # Latest visual feed snapshot
├── scripts/
│   ├── collect.py             # Telemetry aggregator daemon
│   ├── vision.py              # Camera + Gemini visual assessor
│   ├── garden_math.py         # Physics calculation engine
│   ├── init_db.py             # Schema migration utility
│   ├── build_static.py        # Public JSON / page compiler
│   └── log_action.py          # Action log CLI for manual events
├── data/
│   └── garden.db              # SQLite Database (untracked)
└── logs/                      # Activity logs
```

## 🛠️ Automated Sync to GitHub Pages

To keep the GitHub Pages page updated, we run `scripts/sync.sh` which compiles the static page and commits/pushes the updates.

---
*Garden Warden | Chennai Indoor Biome*
